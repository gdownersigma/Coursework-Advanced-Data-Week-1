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


def insert_kiosk_data(connection, data, logger):
    """Insert a single kiosk interaction as either a review or incident."""
    cursor = connection.cursor()

    # site maps to exhibition_id (site + 1 based on your existing logic)
    exhibition_id = data["site"] + 1

    try:
        if data["val"] == -1:
            # It's an incident
            cursor.execute("""
                INSERT INTO incident (exhibition_id, at, incident_type_id)
                VALUES (%s, %s, %s)
            """, (exhibition_id, data["at"], data["type"]))
            logger.debug(f"Inserted incident for exhibition {exhibition_id}")
        else:
            # It's a review
            cursor.execute("""
                INSERT INTO review (exhibition_id, at, rating_id)
                VALUES (%s, %s, %s)
            """, (exhibition_id, data["at"], data["val"]))
            logger.debug(f"Inserted review for exhibition {exhibition_id}")

        connection.commit()

    except Exception as e:
        connection.rollback()
        logger.error(f"Failed to insert record: {e}")
    finally:
        cursor.close()
