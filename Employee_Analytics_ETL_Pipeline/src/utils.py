"""
utils.py - Utility Functions Module

This module contains helper functions used across the ETL pipeline.
It includes logging, file operations, and other utility functions.
"""

import logging
import os
from datetime import datetime


def setup_logging(log_file='logs/etl.log'):
    """
    Setup logging configuration.
    
    Args:
        log_file (str): Path to log file
    """
    # Create logs directory if not exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def create_directories():
    """Create all required directories for the project."""
    directories = [
        'data/raw',
        'data/staging',
        'data/processed',
        'output/database',
        'output/reports',
        'logs',
        'tests'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"[UTILS] Created directory: {directory}")


def get_file_info(file_path):
    """
    Get information about a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        dict: File information
    """
    if not os.path.exists(file_path):
        return None
    
    stat = os.stat(file_path)
    
    return {
        'path': file_path,
        'name': os.path.basename(file_path),
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'extension': os.path.splitext(file_path)[1]
    }


def format_file_size(size_bytes):
    """
    Format file size in human readable format.
    
    Args:
        size_bytes (int): File size in bytes
        
    Returns:
        str: Formatted file size
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def print_pipeline_header():
    """Print a formatted pipeline header."""
    print("\n" + "="*60)
    print("Employee Data ETL Pipeline")
    print("="*60)
    print(f"Started at: {datetime.now()}")
    print("="*60 + "\n")


def print_pipeline_footer(start_time):
    """
    Print a formatted pipeline footer.
    
    Args:
        start_time (datetime): Pipeline start time
    """
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "="*60)
    print("Pipeline Completed!")
    print("="*60)
    print(f"Ended at: {end_time}")
    print(f"Duration: {duration}")
    print("="*60 + "\n")


def validate_dataframe(df, required_columns=None):
    """
    Validate a DataFrame has required columns and data.
    
    Args:
        df (pandas.DataFrame): DataFrame to validate
        required_columns (list): List of required column names
        
    Returns:
        tuple: (is_valid, message)
    """
    if df is None or df.empty:
        return False, "DataFrame is empty"
    
    if required_columns:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            return False, f"Missing columns: {missing_cols}"
    
    return True, "DataFrame is valid"


def save_to_csv(df, file_path, index=False):
    """
    Save DataFrame to CSV file.
    
    Args:
        df (pandas.DataFrame): DataFrame to save
        file_path (str): Output file path
        index (bool): Include index in output
    """
    try:
        # Create directory if not exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save to CSV
        df.to_csv(file_path, index=index)
        print(f"[UTILS] Saved DataFrame to: {file_path}")
        
    except Exception as e:
        print(f"[UTILS] ERROR: Failed to save CSV - {str(e)}")
        raise
