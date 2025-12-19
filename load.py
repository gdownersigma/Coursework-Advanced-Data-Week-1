# load.py
import psycopg2


def get_db_connection(config: dict) -> psycopg2.extensions.connection:
    """Establish and return a database connection using provided configuration"""
    conn = psycopg2.connect(
        dbname=config['DB_NAME'],
        user=config['DB_USER'],
        password=config['DB_PASSWORD'],
        host=config['DB_HOST'],
        port=config['DB_PORT']
    )
    cursor = conn.cursor()
    cursor.execute("SET datestyle TO 'DMY'")
    cursor.close()

    return conn


def load_schema_file() -> str:
    """Load the schema SQL file and return its contents as a string"""
    with open('schema.sql', 'r') as file:
        return file.read()


def execute_schema(cursor, logger=None) -> None:
    """Execute the schema SQL using the provided cursor"""
    schema_sql = load_schema_file()
    if logger:
        logger.info('Executing schema...')
    cursor.execute(schema_sql)


def create_staging_tables(cursor, logger=None) -> None:
    """Create staging tables in the database."""
    if logger:
        logger.info('Creating staging tables...')
    cursor.execute("""
    CREATE TEMP TABLE staging_exhibition(
        exhibition_name VARCHAR(100),
        exhibition_code VARCHAR(20),
        floor_name VARCHAR(50),
        department_name VARCHAR(100),
        start_date DATE,
        description TEXT
        );
    """)

    cursor.execute("""
        CREATE TEMP TABLE staging_kiosk(
            at TIMESTAMP,
            site INT,
            val SMALLINT,
            type TEXT
        );
    """)


def load_exhibition_csv(cursor, logger=None) -> None:
    """Load exhibition CSV into the staging table"""
    if logger:
        logger.info('Loading exhibition CSV into staging table...')
    with open('combined_data/combined_exhibition_data.csv', 'r') as f:
        cursor.copy_expert("""
            COPY staging_exhibition FROM STDIN WITH (FORMAT csv, HEADER true)""", f)


def load_kiosk_csv(cursor, logger=None) -> None:
    """Load kiosk CSV into the staging table"""
    if logger:
        logger.info('Loading kiosk CSV into staging table...')
    with open('combined_data/combined_museum_data.csv', 'r') as f:
        cursor.copy_expert("""
            COPY staging_kiosk FROM STDIN WITH (FORMAT csv, HEADER true)""", f)


def populate_reference_tables(cursor, logger=None):
    """Populate department, floor, rating_desc, incident_type tables"""
    if logger:
        logger.info('Populating reference tables...')

    # Departments
    cursor.execute("""
        INSERT INTO department(department_name)
        SELECT DISTINCT department_name
        FROM staging_exhibition
        ON CONFLICT (department_name) DO NOTHING;
    """)

    # Floors
    cursor.execute("""
        INSERT INTO floor(floor_name)
        SELECT DISTINCT floor_name 
        FROM staging_exhibition
        ON CONFLICT (floor_name) DO NOTHING;
    """)

    # Rating descriptions
    cursor.execute("""
        INSERT INTO rating_desc(rating_id,description) VALUES
        (0, 'Very Poor'),
        (1, 'Poor'),
        (2, 'Average'),
        (3, 'Good'),
        (4, 'Excellent')
        ON CONFLICT (rating_id) DO NOTHING;
    """)

    # Incident types
    cursor.execute("""
        INSERT INTO incident_type(incident_type_id,description) VALUES
        (0,'Help Requested'),
        (1,'Emergency')
        ON CONFLICT (incident_type_id) DO NOTHING;
    """)


def populate_exhibitions(cursor, logger=None):
    """Populate exhibition and floor_assignment tables"""
    if logger:
        logger.info('Inserting exhibitions...')

    cursor.execute("""
        INSERT INTO exhibition(exhibition_name,exhibition_code,department_id,start_date,description)
        SELECT
            se.exhibition_name,
            se.exhibition_code,
            d.department_id,
            se.start_date,
            se.description
        FROM staging_exhibition se
        JOIN department d ON se.department_name = d.department_name
        ON CONFLICT (exhibition_code) DO NOTHING;
    """)

    if logger:
        logger.info('Inserting floor assignments...')

    cursor.execute("""
        INSERT INTO floor_assignment(exhibition_id,floor_id)
        SELECT
            e.exhibition_id,
            f.floor_id
        FROM staging_exhibition se
        JOIN exhibition e ON se.exhibition_code = e.exhibition_code
        JOIN floor f ON se.floor_name = f.floor_name
        ON CONFLICT DO NOTHING;
    """)


def populate_reviews_and_incidents(cursor, logger=None):
    """Populate review and incident tables from kiosk data"""
    if logger:
        logger.info('Inserting reviews...')

    cursor.execute("""
        INSERT INTO review(exhibition_id,at,rating_id)
        SELECT
            site+1,
            at,
            CAST(val AS INTEGER) 
        FROM staging_kiosk
        WHERE val != -1;
    """)

    if logger:
        logger.info('Inserting incidents...')

    cursor.execute("""
        INSERT INTO incident(exhibition_id, at, incident_type_id)
        SELECT
            site +1,
            at,
            CAST(type AS DECIMAL)
        FROM staging_kiosk
        WHERE CAST(val AS INTEGER) = -1;
    """)


def load_data_to_db(data_creds: dict, logger=None) -> None:  # Add logger parameter
    """Load data from a CSV file into the specified database table"""
    if logger:
        logger.info('Connecting to database...')

    try:
        conn = get_db_connection(data_creds)
        cursor = conn.cursor()

        execute_schema(cursor, logger)
        conn.commit()

        create_staging_tables(cursor, logger)

        load_exhibition_csv(cursor, logger)
        load_kiosk_csv(cursor, logger)

        populate_reference_tables(cursor, logger)
        populate_exhibitions(cursor, logger)
        populate_reviews_and_incidents(cursor, logger)
        conn.commit()

        if logger:
            logger.info('Data loading complete.')

        cursor.close()
        conn.close()

        if logger:
            logger.info('Schema executed and connection closed')
    except Exception as e:
        if logger:
            logger.error(f'Error loading data to DB: {e}')
        if conn:
            conn.rollback()
            conn.close()
        raise e
