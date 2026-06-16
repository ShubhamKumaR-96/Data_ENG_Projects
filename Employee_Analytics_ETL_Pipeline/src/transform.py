"""
Transform.py - Data Transformation Module

This module contains functions to transfrom and clean data
it handles data cleaning, validate, and enrichment
"""

import pandas as pd
import numpy as np
from datetime import datetime

def clean_data(df):

    try:
        print(f"[TRANSFORM] Starting data cleaning")

        # Store initial row count
        initial_rows = len(df)

        # Remove duplicate
        df = df.drop_duplicates()
        duplicate_removed = initial_rows - len(df)
        print(f"[TRANSFORM] Removed {duplicate_removed} duplicate rows")

        # Handle null value in salary (fill with mean)
        if 'salary' in df.columns:
            null_salary = df['salary'].isnull().sum()
            df['salary'] = df['salary'].fillna(df['salary'].mean())
            print(f"[TRANSFORM] filled {null_salary} null salary values with mean")

        # Handle null value in email (fill with 'unknown')
        if 'email' in df.columns:
            null_email = df['email'].isnull().sum()
            df['email'] = df['email'].fillna('unknown@example.com')
            print(f"[TRANSFORM] filled {null_email} null email values ")

        # Remove rows with null name and department

        df = df.dropna(subset=['name','department'])
        print(f"[TRANSFORM] Removed rows with null name/department")

        # Clean string columns
        for col in ['name','department','city']:
            if col in df.columns:
                df[col] = df[col].str.strip()
                df[col] = df[col].str.title()

        print(f"[TRASFROM] Data cleaning completed")
        print(f"[TRANSFORMED] final row count: {len(df)}")

        return df 

    except Exception as e:
        print(f"[TRANSFORM] Error: Data cleaning failed - {str(e)}")
        raise

def validate_data(df):
    try:
        print(f"[TRANSFROM] Starting data validation:" )

        initial_rows = len(df)

        # if validate age (18-65)

        if 'age' in df.columns:
            invalid_age = df[(df['age'] < 18 ) | (df['age'] > 65 )].shape[0]
            df = df[(df['age'] >= 18 & (df['age'] <= 65))]
            print(f"[TRANSFORM] Removed {invalid_age} rows with invalid salary")

        # Validate salary (must be positive)
        if 'salary' in df.columns:
            invalid_salary = df[df['salary'] <= 0].shape[0]
            df =  df[df['salary'] > 0]
            print(f"[TRANSFORM] Removed {invalid_salary} rows with invalid salary")

        # Validate email format
        if 'email' in df.columns:
            email_pattern = r'[^\w\._]+@[\w\._-]+\.\w+$'
            valid_email = df['email'].str_match(email_pattern,na=False)
            invalid_email = (~valid_email).sum()
            df = df[valid_email]
            print(f"[TRANSFORM] Removed {invalid_email} rows with invalid emails")

        removed_rows = initial_rows - len(df)
        print(f"[TRANSFORM] Validation completed. Removed {removed_rows} invalid rows")

        return df
    except Exception as e:
        print(f"[TRANSFORM] ERROR : Data validation failed -{str(e)}")
        raise


def enrich_data(df):
    try:
        print(f"[TRANSFORM] Starting data enrichment...")

        # Add annual salary
        if 'salary' in df.columns:
            df['annual_salary'] = df['salary'] * 12
            print("[TRANSFORM] Added 'annual_salary' column")

        # Add tax deduction (30% of salary)
        if 'salary' in df.columns:
            df['tax'] = df['salary'] * 0.3
            print("[TRANSFORM] Added 'tax' column")

        # Add net salary
        if 'salary' in df.columns:
            df['net_salary'] = df['salary'] - df['tax']
            print(f"[TRANSFORM] Added 'net_salary' column")

        # Add salary category
        if 'salary' in df.columns:
            df['salary_category'] = pd.cut(
                df['salary'],bins=[0,40000,80000,150000],
                labels=['Low','Medium','High']
            )    
            print(f"[TRANSFORM] Added 'salary_category' column")

        # Add year and month from join date
        if 'join_date' in df.columns:
            df['join_date'] = pd.to_datetime(df['join_date'])
            df['year'] = df['join_date'].dt.year
            df['month'] = df['join_date'].dt.month
            print("[TRANSFORM] Added 'year' and 'month' columns")

        print("[TRANSFORM] Data enrichment completed")

        return df

    except Exception as e:
        print(f"[TRANSFORM] Data enrichement failed {str(e)}")  
        raise  


def transform_data(df):

    try:
        print("[TRANSFORM] Starting transformation pipeline")
        print(f"[TRANSFORM] Input rows: {len(df)}")

        # Step -1 clean data
        df = clean_data(df)
        print(f"[TRANSFORM] After clearning: {len(df)} rows")
        
        # Step -2 Validate data
        df =  validate_data(df)
        print(f"[TRANSFORM] After validation : {len(df)} rows")

        # Step -3 Enrich Data
        df = enrich_data(df)
        print(f"[TRANSFORM] After enrichment : {len(df)} rows")

        print(f"[TRANSFORM] Transform pipeline completed sucessfully")

        return df
    
    except Exception as e:
        print(f"[TRANSFORM] Error : Transformation pipeline failed - {str(e)}")
        raise



def get_transformation_summary(df):

    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns),
        'salary_stats': {
            'mean': df['salary'].mean() if 'salary' in df.columns else None,
            'min': df['salary'].min() if 'salary' in df.columns else None,
            'max': df['salary'].max() if 'salary' in df.columns else None
        },
        'department_counts': df['department'].value_counts().to_dict() if 'department' in df.columns else {}
    }
    return summary












