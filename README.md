# LMNH Museum Data Pipeline

A complete ETL (Extract, Transform, Load) pipeline for processing museum exhibition data and visitor feedback from the Liverpool Museum of Natural History (LMNH). This project extracts data from AWS S3, transforms it into a structured format, and loads it into a PostgreSQL database for analysis.

## 📋 Project Overview

This pipeline processes two main types of data:
- **Exhibition Information**: Details about museum exhibitions including names, departments, floors, and descriptions
- **Visitor Feedback**: Kiosk data capturing visitor ratings and incident reports across different exhibitions

The processed data is stored in a normalized PostgreSQL database with proper relationships between exhibitions, departments, floors, ratings, and incidents.

## 🏗️ Architecture

```
S3 Bucket → Extract → Transform → Load → PostgreSQL Database
                                           ↓
                                    Terraform (AWS RDS)
```

### Data Flow
1. **Extract**: Downloads JSON and CSV files from AWS S3 bucket (`sigma-resources-museum`)
2. **Transform**: Combines and cleans data files, normalizes column names, removes duplicates
3. **Load**: Inserts transformed data into existing database tables (uses `ON CONFLICT` to handle duplicates)

## 🗂️ Project Structure

```
.
├── pipeline.py                    # Main ETL orchestration script
├── extract.py                     # S3 data extraction module
├── transform.py                   # Data transformation and cleaning
├── load.py                        # Database loading operations
├── schema.sql                     # PostgreSQL database schema
├── requirements.txt               # Python dependencies
├── data_exploration.ipynb         # Jupyter notebook for data analysis
│
├── bucket_data/                   # Raw data from S3 bucket
│   ├── lmnh_exhibition*.json      # Exhibition information files
│   └── lmnh_hist_data*.csv        # Historical kiosk data files
│
├── combined_data/                 # Processed data files
│   ├── combined_exhibition_data.csv
│   └── combined_museum_data.csv
│
├── terraform_db/                  # Infrastructure as Code
│   ├── main.tf                    # Terraform configuration for AWS RDS
│   ├── variables.tf               # Variable definitions
│   └── terraform.tfvars           # Variable values (gitignored)
│
└── coding_problems/               # Additional coding challenges
    ├── challenge/
    ├── challenge_2/
    └── day_1/
```

## 🗄️ Database Schema

The database consists of the following tables:

### Core Tables
- **exhibition**: Exhibition details (name, code, start date, description)
- **department**: Museum departments (e.g., Natural History, Archaeology)
- **floor**: Museum floors where exhibitions are located
- **floor_assignment**: Many-to-many relationship between exhibitions and floors

### Feedback Tables
- **review**: Visitor ratings for exhibitions
- **rating_desc**: Rating descriptions (0=Very Poor to 4=Excellent)
- **incident**: Incident reports from kiosks
- **incident_type**: Types of incidents (Help Requested, Emergency)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- AWS Account (for S3 access and RDS deployment)
- Terraform (for infrastructure deployment)

### Installation

1. **Clone the repository**
   ```bash
   cd Coursework-Advanced-Data-Week-1
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # AWS Credentials
   AWS_ACCESS_KEY=your_access_key
   AWS_SECRET_KEY=your_secret_key
   
   # Database Configuration
   DB_NAME=museum
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=5432
   ```

### Infrastructure Setup (Optional)

To deploy a PostgreSQL database on AWS RDS using Terraform:

1. Navigate to the terraform directory:
   ```bash
   cd terraform_db
   ```

2. Create a `terraform.tfvars` file with your AWS credentials:
   ```hcl
   AWS_REGION = "eu-west-2"
   AWS_ID = "your_aws_access_key"
   AWS_SECRET = "your_aws_secret_key"
   VPC_ID = "your_vpc_id"
   DB_USERNAME = "your_db_username"
   DB_PASSWORD = "your_db_password"
   ```

3. Initialize and apply Terraform:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. **Initialize the database schema (one-time setup)**:
   
   After creating your database, run the schema file to create all tables:
   ```bash
   psql -h your_db_host -U your_db_user -d museum -f schema.sql
   ```
   
   Or connect via any PostgreSQL client and execute the contents of [`schema.sql`](schema.sql).

> **Note**: The database schema only needs to be created once. Subsequent pipeline runs will insert data into the existing tables without recreating them.

## 🎯 Usage

### First-Time Setup

**Before running the pipeline for the first time**, ensure your database schema is initialized (see step 4 in Installation above).

### Running the Pipeline

Execute the complete ETL pipeline to load new data:

```bash
python3 pipeline.py --push
```

The pipeline will:
- Extract fresh data from S3 (or use local files if `--skip-extract` is used)
- Transform and combine the data
- Load data into the existing database tables
- Handle duplicates automatically using `ON CONFLICT` clauses

### Command-Line Options

```bash
python3 pipeline.py [OPTIONS]

Options:
  --secret-key TEXT      AWS Secret Key (default: from .env)
  --access-key TEXT      AWS Access Key (default: from .env)
  -p, --push            Push data to the database after processing
  -se, --skip-extract   Skip extraction - use local files
  -bucket TEXT          S3 bucket name (default: sigma-resources-museum)
  --db-name TEXT        Database name (default: museum)
  --db-user TEXT        Database user
  --db-password TEXT    Database password
  --db-host TEXT        Database host (default: localhost)
  --db-port TEXT        Database port (default: 5432)
```

### Examples

**Extract and transform only (no database load):**
```bash
python3 pipeline.py
```

**Skip extraction and use local data:**
```bash
python3 pipeline.py --skip-extract --push
```

**Full pipeline with custom database:**
```bash
python3 pipeline.py --push --db-host mydb.example.com --db-user admin
```

## 📊 Data Exploration

Use the included Jupyter notebook for data analysis:

```bash
jupyter notebook data_exploration.ipynb
```

The notebook provides:
- Data quality checks
- Statistical summaries
- Visualization of ratings and incidents
- Exhibition performance analysis

## 🔍 Module Descriptions

### pipeline.py
Main orchestration script that:
- Configures logging
- Parses command-line arguments
- Coordinates the ETL process
- Handles error logging and recovery

### extract.py
Handles data extraction:
- Connects to AWS S3 using boto3
- Lists available buckets and objects
- Downloads museum data files (JSON and CSV)

### transform.py
Data transformation operations:
- Combines multiple JSON files into a single DataFrame
- Merges CSV files
- Normalizes column names
- Removes duplicates
- Outputs cleaned CSV files

### load.py
Database operations:
- Establishes PostgreSQL connections
- Creates temporary staging tables for data processing
- Loads data using efficient COPY operations
- Populates normalized tables with proper relationships
- Uses `ON CONFLICT` clauses to handle duplicate entries gracefully

## 🧪 Testing

The `coding_problems/` directory contains additional coding challenges with unit tests:

```bash
cd coding_problems/challenge
pytest test_main.py
```

## 📝 Logging

The pipeline creates a `pipeline.log` file that records:
- Extraction progress
- Transformation steps
- Database operations
- Errors and exceptions

## 🛠️ Technologies Used

- **Python 3**: Core programming language
- **Pandas**: Data manipulation and transformation
- **boto3**: AWS S3 integration
- **psycopg2**: PostgreSQL database adapter
- **PostgreSQL**: Relational database
- **Terraform**: Infrastructure as Code
- **AWS S3**: Data storage
- **AWS RDS**: Managed database service
- **Jupyter**: Data exploration and analysis

## 📈 Future Enhancements

- [ ] Add data validation and quality checks
- [ ] Implement incremental data loading
- [ ] Add automated testing for ETL pipeline
- [ ] Create dashboard for real-time analytics
- [ ] Implement data archival strategy
- [ ] Add support for multiple data sources

## ⚠️ Important Notes

- **Database schema must be initialized once** before running the pipeline (see Installation step 4)
- The pipeline is designed for **incremental data loading** - it won't recreate tables on each run
- Duplicate entries are handled automatically using `ON CONFLICT` clauses
- Ensure AWS credentials have appropriate permissions for S3 access
- Database credentials should never be committed to version control
- The pipeline expects specific file naming conventions (`lmnh_*`)
- Date format is set to DMY for compatibility with UK date formats

## 🤝 Contributing

This is a coursework project for Sigma Labs Advanced Data Week 1.

## 📄 License

This project is part of academic coursework.

## 👤 Author

George Downer - Sigma Labs Cohort 21

---

**Last Updated**: December 2025
