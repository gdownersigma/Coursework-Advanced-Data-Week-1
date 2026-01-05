# LMNH Museum Data Pipeline - AI Agent Instructions

## Project Overview
This is an ETL (Extract, Transform, Load) pipeline processing museum exhibition data and visitor feedback from AWS S3 into a normalized PostgreSQL database. The pipeline handles JSON exhibition info and CSV kiosk data (ratings/incidents), combining them into structured tables.

## Critical Architecture Decisions

### ETL Workflow
The pipeline follows a strict sequence: `extract.py` → `transform.py` → `load.py`, orchestrated by `pipeline.py`. Each module is independent but relies on output from the previous stage:
- **Extract**: Downloads files from S3 bucket `sigma-resources-museum` to `./bucket_data/`
- **Transform**: Combines JSON → CSV (`combined_exhibition_data.csv`) and merges CSVs → single file (`combined_museum_data.csv`) in `./combined_data/`
- **Load**: Uses temporary staging tables, then populates normalized tables with `ON CONFLICT DO NOTHING` to handle duplicates

### Staging Table Pattern
`load.py` creates **TEMP** staging tables (`staging_exhibition`, `staging_kiosk`) for each run. This allows bulk COPY operations followed by INSERT...SELECT queries with proper foreign key resolution. Never modify permanent tables directly from CSVs.

### Database Schema Key Points
- **Schema execution is ONE-TIME**: The `execute_schema()` function in `load.py` is commented out after initial setup. Do not recreate tables on every run.
- **Date format**: Connection sets `datestyle TO 'DMY'` for UK date compatibility
- **Exhibition site mapping**: `site` column in CSV maps to `exhibition_id` via `site+1` (exhibition IDs are 1-indexed, sites are 0-indexed)
- **Incident detection**: `val = -1` indicates an incident, not a rating
- **Duplicate handling**: All INSERT statements use `ON CONFLICT` clauses to safely handle re-runs

## Developer Workflows

### Running the Pipeline
```bash
# Full ETL with database load
python3 pipeline.py --push

# Skip S3 extraction, use local files
python3 pipeline.py --skip-extract --push

# Transform only (no DB push)
python3 pipeline.py
```

### Database Setup (First Time Only)
```bash
# After creating database with Terraform or manually
psql -h $DB_HOST -U $DB_USER -d museum -f schema.sql
```
Then run pipeline normally. Schema execution is disabled in code after first setup.

### Terraform Database Provisioning
```bash
cd terraform_db
terraform init
terraform apply
# Creates AWS RDS PostgreSQL with public access, security group for port 5432
```

### Testing
```bash
cd coding_problems/challenge
pytest test_main.py
```

## Project-Specific Conventions

### File Naming & Discovery
- All museum files in S3 start with `lmnh` prefix (enforced in `extract.py:download_objects()`)
- `transform.py` functions explicitly filter for `lmnh*.json` and `*.csv` patterns
- Output files have fixed paths: `./combined_data/combined_exhibition_data.csv` and `./combined_data/combined_museum_data.csv`

### Column Name Normalization
- `transform.py` lowercases all column names after JSON normalization
- Special rename: `exhibition_id` → `exhibition_code` (exhibitions have codes, not IDs in source data)

### Logging Pattern
- `pipeline.py` uses dual handlers: file (`pipeline.log`) and console (stdout)
- All major functions accept optional `logger` parameter
- Log levels: DEBUG to file, INFO to console (configurable via `setup_logging()`)

### Environment Variables
Uses `python-dotenv`. Required `.env` variables:
```
AWS_ACCESS_KEY, AWS_SECRET_KEY
DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
BOOTSTRAP_SERVERS, SECURITY_PROTOCOL, SASL_MECHANISM, USERNAME, PASSWORD (for consumer.py)
```
Command-line args in `pipeline.py` override `.env` defaults.

## Integration Points

### AWS S3
- Default bucket: `sigma-resources-museum`
- boto3 client configured in `extract.py:get_s3_client()`
- Files stored locally in `./bucket_data/` mirror S3 structure

### PostgreSQL Connection
- `psycopg2` with connection pooling not used (creates new connection per `load_data_to_db()` call)
- Cursor uses `COPY` for bulk inserts from CSV (fastest method)
- Connection always commits or rollbacks explicitly

### Kafka Consumer (consumer.py)
- Separate script using `confluent-kafka` library
- Configuration from environment variables with SASL authentication
- Not integrated into main pipeline flow

## Data Flow Details

### Exhibition Data Flow
1. JSON files → DataFrame → lowercase columns → rename `exhibition_id` to `exhibition_code`
2. Save to `combined_exhibition_data.csv`
3. Load into `staging_exhibition` (temp table)
4. Populate `department`, `floor` reference tables via INSERT...SELECT DISTINCT
5. Populate `exhibition` table joining back to reference tables
6. Populate `floor_assignment` (many-to-many) joining exhibition + floor

### Kiosk Data Flow  
1. CSV files → concatenate → sort by `at` timestamp → save to `combined_museum_data.csv`
2. Load into `staging_kiosk` (temp table with columns: at, site, val, type)
3. Split into reviews (`WHERE val != -1`) and incidents (`WHERE val = -1`)
4. Map `site+1` → `exhibition_id` (zero-indexed to one-indexed conversion)

## Common Pitfalls

1. **Never recreate schema in pipeline runs** - `execute_schema()` is commented out intentionally
2. **Don't forget `site+1` mapping** - Site numbers are zero-based, exhibition IDs are one-based
3. **CSV column order matters** - COPY expects exact header match with staging table columns
4. **Temporal tables are TEMP** - Staging tables are session-scoped, recreated each run
5. **Transform runs require local files** - If using `--skip-extract`, ensure `./bucket_data/` is populated
6. **Date parsing** - Timestamp column `at` uses DMY format, requires `SET datestyle`

## Key Files Reference

- [pipeline.py](pipeline.py) - Main orchestrator with CLI args
- [extract.py](extract.py) - S3 download logic with `lmnh` prefix filter
- [transform.py](transform.py) - Pandas-based JSON/CSV combining
- [load.py](load.py) - Staging pattern, bulk COPY, reference table population
- [schema.sql](schema.sql) - Complete normalized schema with constraints
- [terraform_db/main.tf](terraform_db/main.tf) - AWS RDS provisioning (db.t3.micro, public access)

## Good code Quality Practices
- All functions should have typehints and docstrings
- Docstrings should only be one line
- Follow PEP8 styling conventions
- Code must have clear variable names
- Modularize code into smaller functions where possible
- function names should be clear and descriptive
