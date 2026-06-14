"""
generate_data.py - Sample Data Generator

This script generates sample employee data for testing the ETL pipeline.
It creates a CSV file with 1000 employee records.
"""

import pandas as pd
import random
from datetime import datetime,timedelta
import os

def generate_employee(n=1000):
    """ 
    Generate n employee records.
    Args:
        n (int): Number of records to generate 
    Returns:
        pandas.DataFrame: Generated employee data
    """

    # define possible values
    departments = ['IT','HR','Finance','Marketing','Sales','Operations']
    first_names = [
        'Rahul', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Neha',
        'Rohan', 'Pooja', 'Sanjay', 'Anita', 'Raj', 'Meera',
        'Vijay', 'Deepa', 'Suresh', 'Kavita', 'Ravi', 'Nisha',
        'Arun', 'Sunita', 'Manoj', 'Priti', 'Kumar', 'Asha'
    ]
    last_names = ['Kumar', 'Sharma', 'Patel', 'Singh', 'Gupta', 'Verma', 'Reddy']
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune', 'Hyderabad', 'Kolkata']

    data = []

    for i in range(1,n+1):
        # Generate random employee_data
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        employee = {
            'id': i,
            'name': f"{first_name} {last_name}",
            'age': random.randint(22,55),
            'department': random.choice(departments),
            'salary': random.randint(27000,150000),
            'join_date':(datetime.now() - timedelta(days=random.randint(365,1825))).strftime('%Y-%m-%d'),
            'city': random.choice(cities),
            'email': f"{first_name.lower()}.{last_name.lower()}@example.com"
        }

        data.append(employee)

    # Create dataframe
    emp_df = pd.DataFrame(data)

    # Add some quality issues for testing
    # Add duplicate rows
    duplicate_row = emp_df.sample(n=50)
    emp_df = pd.concat([emp_df, duplicate_row],ignore_index=True)

    # Add null values
    null_indices = emp_df.sample(n=30).index
    emp_df.loc[null_indices,'salary'] = None 

    null_email_indices =  emp_df.sample(n=20).index
    emp_df.loc[null_email_indices,'email'] = None

    # Add invalid age groups
    invalid_age_indices = emp_df.sample(n=10).index
    emp_df.loc[invalid_age_indices,'age'] = random.choice([5,10,70,80])

    return emp_df


def main():
    """ Main function to generate and save sample data """
    print("="*50)
    print("Sample Data Generator")
    print("="*50)

    # Create data/raw directory if not exits
    os.makedirs('data/raw', exist_ok=True)

    # Generate data
    print("\n[GENERATOR] Generating 1000 employee records...")
    df = generate_employee(1000)

    # Save to CSV
    output_file = 'data/raw/employee.csv'
    df.to_csv(output_file,index=False)

    print(f"[GENERATOR] Generated {len(df)} records")
    print(f"[GENERATOR] Saved to: {output_file} ")

    # Show sample data
    print("\n[GENERATOR] Sample data {first 5 rows}:")
    print(df.head())

    # Show data info
    print("\n[GENERTOR] Data info: ")
    print(f" - Total rows: {len(df)}")
    print(f" - Columns: {list(df.columns)}")
    print(f" - Null values: {df.isnull().sum().sum()}")
    print(f" - Duplicate: {df.duplicated().sum()}") 

    print("\n" + "="*50)
    print("Data generation completed !")
    print("="*50)


if __name__ == '__main__':
    main()    



    

