# Employee Data ETL Pipeline

A complete ETL (Extract, Transform, Load) pipeline for processing employee data using Python and SQLite.

## Project Overview

This project demonstrates a real-world ETL pipeline that:
- Extracts employee data from CSV files
- Cleans and transforms the data
- Loads it into a SQLite database
- Generates analysis reports

## Features

- **Data Extraction**: Read CSV files with validation
- **Data Cleaning**: Handle null values, duplicates, and invalid data
- **Data Enrichment**: Add calculated columns (annual salary, tax, etc.)
- **Database Storage**: Store processed data in SQLite
- **Report Generation**: Create department-wise and monthly reports
- **Error Handling**: Comprehensive error handling and logging
- **Testing**: Unit tests for all modules

## Project Structure

```
shubh_project/
├── data/
│   ├── raw/          # Original CSV files
│   ├── staging/      # Intermediate files
│   └── processed/    # Cleaned files
├── src/
│   ├── __init__.py
│   ├── extract.py    # Extract functions
│   ├── transform.py  # Transform functions
│   ├── load.py       # Load functions
│   └── utils.py      # Utility functions
├── output/
│   ├── database/     # SQLite database
│   └── reports/      # CSV reports
├── tests/
│   └── test_etl.py   # Unit tests
├── logs/
│   └── etl.log       # Log files
├── main.py           # Entry point
├── requirements.txt  # Dependencies
├── README.md         # This file
└── .gitignore        # Git ignore rules
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)




