"""
extract.py - Data Extraction Module

This module contains function to extarct data from CSV files
it reads raw data and return pandas Dataframe
"""

import pandas as pd
import os
from datetime import datetime

def validate_file(file_path):

    # Check if file exits
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check if file is CSV
    if not file_path.endswith('.csv'):
        raise ValueError(f"File is not a CSV: {file_path}")
    
    # Check if file is not empty
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"File is empty: {file_path}")
    
    return True




def extract_data(file_path):
    try:
        #Log extraction start
        print(f"[EXTRACT] Starting extraction from: {file_path}")
        print(f"[EXTRACT] Timestamp: {datetime.now()}")

        # Validate file
        validate_file(file_path)
        print(f"[EXTRACT] File validation passed")

        # Read CSV file
        df = pd.read_csv(file_path)
        print(f"[EXTRACT] Successfully read CSV file")

        # Basic info about extarced data
        rows,cols = df.shape
        print(f"[EXTRACT] Extracted {rows} and {cols} columns")

        # Log columns names
        print(f"[EXTRACT] Columns: {list(df.columns)}")

        # Log data types
        print(f"[EXTACT] Data types:")
        for col in df.columns:
            print(f" - {col}: {df[col].dtype}")


        # Log extraction completion
        print(f"[EXTRACT] Extraction completed successfully")
        print(f"[EXTRACT] Timestamp: {datetime.now()}")

        return df
    
    except FileNotFoundError :
        print(f"[EXTRACT] File not found - {file_path}")
        raise

    except ValueError as e :
        print(f"[EXTRACT] ERROR: Validation error - {str(e)}")
        raise

    except Exception as e :
        print(f"[EXTRACT] EROR: Extraction failed - {str(e)}")
        raise


def extract_multiple_files(folder_path,pattern='*.csv'):

    try:
        print(f"[EXTRACT] Extracting multiple files from : {folder_path}")

        # Get all csv files in folder

        files = [f for f in os.listdir(folder_path) if f.endsWith('.csv')]    

        if not files:
            print(f"[EXTRACT WARNING: no CSV files found in {folder_path}]")
            return {}
        
        # Extract data from each file
        dateframes = {}
        for file in files:
            file_path = os.path.join(folder_path,file)
            df = extract_data(file_path)
            dateframes[file] = df
        
        print(f"[EXTRACT] Extracted {len(dateframes)} files successfully")
        return dateframes
    
    except Exception as e:
        print(f"[EXTRACT] ERROR: Multiple extraction failed - {str(e)}")
        raise

def get_extraction_summary(df):

    summary ={
        'total_rows':len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns),
        'data_types': df.dtypes.to_dict(),
        'null_counts':df.isnull().sum().to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum()
    }
    return summary    

    


