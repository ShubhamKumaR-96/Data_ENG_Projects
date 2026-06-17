import sys
import os
import pytest
import pandas as pd
import numpy as np
import sqlite3
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from extract import extract_data, validate_file, get_extraction_summary
from transform import clean_data, validate_data, enrich_data, transform_data, get_transformation_summary
from load import create_database_connection, create_table, load_employees, load_data
from utils import validate_dataframe, format_file_size


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['  alice  ', 'BOB', 'charlie', 'david', None],
        'age': [25, 30, 35, 40, 28],
        'department': ['HR', 'IT', 'IT', 'Finance', None],
        'salary': [50000, 60000, 70000, 80000, 55000],
        'join_date': ['2023-01-15', '2022-06-20', '2021-09-10', '2020-03-05', '2023-07-25'],
        'city': ['Delhi', 'Mumbai', '  PUNE  ', 'Kolkata', 'Chennai'],
        'email': ['alice@test.com', 'bob@test.com', 'charlie@test.com', 'david@test.com', 'noemail']
    })


@pytest.fixture
def dirty_df():
    return pd.DataFrame({
        'id': [1, 1, 2, 3, 4],
        'name': ['Alice', 'Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 25, 30, 10, 70],
        'department': ['HR', 'HR', 'IT', 'IT', 'Finance'],
        'salary': [50000, 50000, 60000, -5000, 80000],
        'join_date': ['2023-01-15', '2023-01-15', '2022-06-20', '2021-09-10', '2020-03-05'],
        'city': ['Delhi', 'Delhi', 'Mumbai', 'Pune', 'Kolkata'],
        'email': ['alice@test.com', 'alice@test.com', 'bob@test.com', 'invalid-email', 'david@test.com']
    })


# ==========================================
# EXTRACT TESTS
# ==========================================

class TestExtract:

    def test_validate_file_exists(self, tmp_path):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("id,name\n1,Alice")
        assert validate_file(str(csv_file)) is True

    def test_validate_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            validate_file("nonexistent.csv")

    def test_validate_file_not_csv(self, tmp_path):
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("hello")
        with pytest.raises(ValueError):
            validate_file(str(txt_file))

    def test_validate_file_empty(self, tmp_path):
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("")
        with pytest.raises(ValueError):
            validate_file(str(csv_file))

    def test_extract_data(self, tmp_path):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("id,name,salary\n1,Alice,50000\n2,Bob,60000")
        df = extract_data(str(csv_file))
        assert len(df) == 2
        assert list(df.columns) == ['id', 'name', 'salary']

    def test_get_extraction_summary(self, sample_df):
        summary = get_extraction_summary(sample_df)
        assert summary['total_rows'] == 5
        assert summary['total_columns'] == 8
        assert 'name' in summary['columns']


# ==========================================
# TRANSFORM TESTS
# ==========================================

class TestTransform:

    def test_clean_data_removes_duplicates(self, dirty_df):
        result = clean_data(dirty_df)
        assert len(result) < len(dirty_df)
        assert not result.duplicated().any()

    def test_clean_data_fills_null_salary(self):
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'department': ['HR', 'IT'],
            'salary': [50000, np.nan],
            'city': ['Delhi', 'Mumbai'],
            'email': ['a@test.com', 'b@test.com']
        })
        result = clean_data(df)
        assert result['salary'].isnull().sum() == 0

    def test_clean_data_drops_null_name(self):
        df = pd.DataFrame({
            'name': [None, 'Bob'],
            'department': ['HR', 'IT'],
            'salary': [50000, 60000],
            'city': ['Delhi', 'Mumbai'],
            'email': ['a@test.com', 'b@test.com']
        })
        result = clean_data(df)
        assert len(result) == 1

    def test_clean_data_strips_whitespace(self, sample_df):
        result = clean_data(sample_df)
        for val in result['name']:
            assert val == val.strip()

    def test_validate_data_age_filter(self):
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'department': ['HR', 'IT', 'Finance'],
            'salary': [50000, 60000, 70000],
            'age': [15, 30, 70],
            'email': ['a@test.com', 'b@test.com', 'c@test.com']
        })
        result = validate_data(df)
        assert len(result) == 1
        assert result['age'].values[0] == 30

    def test_validate_data_salary_positive(self):
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'department': ['HR', 'IT'],
            'salary': [-5000, 60000],
            'age': [25, 30],
            'email': ['a@test.com', 'b@test.com']
        })
        result = validate_data(df)
        assert len(result) == 1
        assert result['salary'].values[0] == 60000

    def test_validate_data_email_format(self):
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'department': ['HR', 'IT'],
            'salary': [50000, 60000],
            'age': [25, 30],
            'email': ['valid@test.com', 'invalid-email']
        })
        result = validate_data(df)
        assert len(result) == 1

    def test_enrich_data_adds_columns(self, sample_df):
        cleaned = clean_data(sample_df)
        result = enrich_data(cleaned)
        assert 'annual_salary' in result.columns
        assert 'tax' in result.columns
        assert 'net_salary' in result.columns
        assert 'salary_category' in result.columns
        assert 'year' in result.columns
        assert 'month' in result.columns

    def test_enrich_data_annual_salary(self, sample_df):
        cleaned = clean_data(sample_df)
        result = enrich_data(cleaned)
        assert (result['annual_salary'] == result['salary'] * 12).all()

    def test_enrich_data_tax(self, sample_df):
        cleaned = clean_data(sample_df)
        result = enrich_data(cleaned)
        assert (result['tax'] == result['salary'] * 0.3).all()

    def test_transform_data_full_pipeline(self, sample_df):
        result = transform_data(sample_df)
        assert len(result) > 0
        assert 'annual_salary' in result.columns
        assert not result.duplicated().any()

    def test_get_transformation_summary(self, sample_df):
        transformed = transform_data(sample_df)
        summary = get_transformation_summary(transformed)
        assert 'total_rows' in summary
        assert 'salary_stats' in summary
        assert summary['salary_stats']['mean'] is not None


# ==========================================
# LOAD TESTS
# ==========================================

class TestLoad:

    def test_create_database_connection(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        conn = create_database_connection(db_path)
        assert conn is not None
        conn.close()
        assert os.path.exists(db_path)

    def test_create_tables(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        conn = create_database_connection(db_path)
        create_table(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert 'employee' in tables
        assert 'department_summary' in tables
        assert 'monthly_report' in tables
        conn.close()

    def test_load_employees(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        conn = create_database_connection(db_path)
        create_table(conn)
        df = pd.DataFrame({
            'id': [1, 2],
            'name': ['Alice', 'Bob'],
            'age': [25, 30],
            'department': ['HR', 'IT'],
            'salary': [50000, 60000],
            'join_date': ['2023-01-15', '2022-06-20'],
            'city': ['Delhi', 'Mumbai'],
            'email': ['alice@test.com', 'bob@test.com']
        })
        load_employees(df, conn)
        result = pd.read_sql_query("SELECT * FROM employee", conn)
        assert len(result) == 2
        conn.close()

    def test_load_data_full(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'department': ['HR', 'IT', 'IT'],
            'salary': [50000, 60000, 70000],
            'join_date': ['2023-01-15', '2022-06-20', '2021-09-10'],
            'city': ['Delhi', 'Mumbai', 'Pune'],
            'email': ['alice@test.com', 'bob@test.com', 'charlie@test.com'],
            'annual_salary': [600000, 720000, 840000],
            'tax': [15000, 18000, 21000],
            'net_salary': [35000, 42000, 49000],
            'salary_category': ['Low', 'Medium', 'Medium'],
            'year': [2023, 2022, 2021],
            'month': [1, 6, 9]
        })
        load_data(df, db_path)
        conn = sqlite3.connect(db_path)
        result = pd.read_sql_query("SELECT * FROM employee", conn)
        assert len(result) == 3
        conn.close()


# ==========================================
# UTILS TESTS
# ==========================================

class TestUtils:

    def test_validate_dataframe_valid(self, sample_df):
        is_valid, msg = validate_dataframe(sample_df)
        assert is_valid is True

    def test_validate_dataframe_empty(self):
        is_valid, msg = validate_dataframe(pd.DataFrame())
        assert is_valid is False

    def test_validate_dataframe_none(self):
        is_valid, msg = validate_dataframe(None)
        assert is_valid is False

    def test_validate_dataframe_missing_columns(self, sample_df):
        is_valid, msg = validate_dataframe(sample_df, ['salary', 'bonus'])
        assert is_valid is False
        assert 'bonus' in msg

    def test_validate_dataframe_has_columns(self, sample_df):
        is_valid, msg = validate_dataframe(sample_df, ['name', 'salary'])
        assert is_valid is True

    def test_format_file_size_bytes(self):
        assert format_file_size(500) == '500.00 B'

    def test_format_file_size_kb(self):
        assert format_file_size(1500) == '1.46 KB'

    def test_format_file_size_mb(self):
        assert format_file_size(1500000) == '1.43 MB'

    def test_format_file_size_gb(self):
        assert format_file_size(1500000000) == '1.40 GB'
