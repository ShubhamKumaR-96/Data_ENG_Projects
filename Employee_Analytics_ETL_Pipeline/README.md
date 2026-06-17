# Employee Data ETL Pipeline

A production-ready ETL (Extract, Transform, Load) pipeline for processing employee data using Python and SQLite.

## Overview

This project automates the extraction, cleaning, validation, enrichment, and loading of employee data from CSV files into a SQLite database, with automated report generation.

## Tech Stack

- **Language**: Python 3.11
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite3
- **Testing**: Pytest
- **Version Control**: Git

## Features

- **Data Extraction** - Read CSV files with file validation (existence, format, size)
- **Data Cleaning** - Remove duplicates, handle null values, normalize strings
- **Data Validation** - Filter invalid age (18-65), positive salaries, valid email formats
- **Data Enrichment** - Compute annual salary, tax (30%), net salary, salary categories
- **Database Storage** - Load data into SQLite with proper schema design
- **Report Generation** - Department analysis, monthly reports, high-salary employees
- **Error Handling** - Comprehensive try-catch blocks with logging
- **Unit Testing** - 31 automated tests covering all modules

## Project Structure

```
Employee_Analytics_ETL_Pipeline/
├── data/
│   ├── generate_data.py       # Synthetic data generator
│   └── raw/
│       └── employee.csv       # Source data
├── src/
│   ├── __init__.py
│   ├── extract.py             # Data extraction module
│   ├── transform.py           # Data transformation module
│   ├── load.py                # Data loading module
│   └── utils.py               # Utility functions
├── tests/
│   └── test_etl.py            # Unit tests (31 tests)
├── output/
│   ├── database/
│   │   └── company.db         # SQLite database
│   └── reports/
│       ├── department_analysis.csv
│       ├── monthly_report.csv
│       └── high_salary_employees.csv
├── logs/
│   └── etl.log                # Pipeline logs
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .gitignore
└── README.md
```

## Installation

```bash
# Clone the repository
git clone https://github.com/ShubhamKumaR-96/Data_ENG_Projects.git
cd Data_ENG_Projects/Employee_Analytics_ETL_Pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the full ETL pipeline
python main.py

# Run with custom input file
python main.py data/raw/employee.csv

# Run tests
python -m pytest tests/test_etl.py -v
```

## Pipeline Flow

```
┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│   CSV    │───▶│  Extract  │───▶│Transform │───▶│   Load   │
│  File    │    │           │    │          │    │          │
└──────────┘    └───────────┘    └──────────┘    └──────────┘
                     │               │                │
                     ▼               ▼                ▼
                Read CSV      Clean + Validate    SQLite DB
                              + Enrich            + Reports
```

## ETL Modules

### Extract (`src/extract.py`)
- Validates file existence, format, and size
- Reads CSV into Pandas DataFrame
- Returns extraction summary (rows, columns, dtypes)

### Transform (`src/transform.py`)
- **Cleaning**: Removes duplicates, fills nulls, normalizes strings
- **Validation**: Filters invalid age, negative salaries, bad emails
- **Enrichment**: Adds annual_salary, tax, net_salary, salary_category, year, month

### Load (`src/load.py`)
- Creates SQLite database and tables
- Loads employee data, department summary, and monthly reports
- Exports CSV reports for analysis

## Database Schema

### employee table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Employee name |
| age | INTEGER | Age (18-65) |
| department | TEXT | Department name |
| salary | REAL | Monthly salary |
| annual_salary | REAL | salary * 12 |
| tax | REAL | 30% of salary |
| net_salary | REAL | salary - tax |
| salary_category | TEXT | Low/Medium/High |
| join_date | DATE | Date of joining |
| city | TEXT | City name |
| email | TEXT | Email address |
| year | INTEGER | Join year |
| month | INTEGER | Join month |

### department_summary table
| Column | Type | Description |
|--------|------|-------------|
| department | TEXT | Primary key |
| emp_count | INTEGER | Total employees |
| avg_salary | REAL | Average salary |
| total_salary | REAL | Total salary expense |
| min_salary | REAL | Minimum salary |
| max_salary | REAL | Maximum salary |

### monthly_report table
| Column | Type | Description |
|--------|------|-------------|
| year | INTEGER | Primary key |
| month | INTEGER | Primary key |
| total_employee | INTEGER | Total employees |
| avg_salary | REAL | Average salary |
| total_salary | REAL | Total salary expense |
| new_joins | INTEGER | New employees joined |

## Generated Reports

| Report | Description |
|--------|-------------|
| `department_analysis.csv` | Department-wise salary statistics |
| `monthly_report.csv` | Month-wise employee and salary data |
| `high_salary_employees.csv` | Employees with high salary category |

## Testing

```bash
# Run all tests
python -m pytest tests/test_etl.py -v

# Run specific test class
python -m pytest tests/test_etl.py::TestExtract -v
python -m pytest tests/test_etl.py::TestTransform -v
python -m pytest tests/test_etl.py::TestLoad -v
python -m pytest tests/test_etl.py::TestUtils -v
```

### Test Coverage

| Module | Tests | Coverage |
|--------|-------|----------|
| Extract | 6 | File validation, CSV read, summary |
| Transform | 12 | Clean, validate, enrich, pipeline |
| Load | 4 | DB connection, tables, data loading |
| Utils | 9 | DataFrame validation, formatting |
| **Total** | **31** | **All modules covered** |

## Sample Output

```
============================================================
Employee Data ETL Pipeline
============================================================
Started at: 2026-06-16 19:49:33.255525
============================================================

Step-1 EXTRACT: 1050 rows extracted
Step-2 TRANSFORM: 996 rows (cleaned + validated + enriched)
Step-3 LOAD: 996 records loaded to SQLite
Step-4 REPORTS: 3 CSV reports generated

Pipeline Completed!
Duration: 0.05 sec
============================================================
```

