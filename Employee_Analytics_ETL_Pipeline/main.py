import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'src'))

from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data, generate_report

from src.utils import (
    setup_logging,
    create_directories,
    print_pipeline_header,
    print_pipeline_footer
)


def run_pipeline(input_file='data/raw/employee.csv'):
    
    start_time = datetime.now()

    print_pipeline_header()

    logger = setup_logging()
    logger.info('Starting ETL Pipeline')

    try:
        print("[MAIN] Creating directories")
        create_directories()
        print(f"[MAIN] Directories created successfully")

        print("="*50)
        print("Step-1 EXTRACT")
        print("="*50)
        df_raw =extract_data(input_file)
        print()

        print("="*50)
        print("Step-2 TRANSFORM")
        print("="*50)
        df_transformed = transform_data(df_raw)
        print()

        print("="*50)
        print("Step-3 LOAD")
        print("="*50)
        load_data(df_transformed)
        print()

        print("="*50)
        print("Step-4 Generate REPORTS")
        print("="*50)
        generate_report()
        print()

        print("="*50)
        print("PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*50)
        logger.info("ETL Pipeline completed successfully")

    except FileNotFoundError as e:
        print(f"\n[MAIN] ERROR: File not found - {str(e)}")
        logger.error(f"File not found: {str(e)}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n[MAIN] ERROR: Pipeline failed - {str(e)}")
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)
    
    finally:
        # Print footer with duration
        print_pipeline_footer(start_time)


if __name__ == "__main__":
    # Check if input file is provided as command line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'data/raw/employee.csv'
    
    # Run the pipeline
    run_pipeline(input_file)


       
  








