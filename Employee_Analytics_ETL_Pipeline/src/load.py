
import pandas as pd
import sqlite3
import os
from datetime import datetime

def create_database_connection(db_path):

    try:
        print(f"[LOAD] Creating database connection : {db_path}")

        # Create connection
        conn = sqlite3.connect(db_path)

        conn.execute("PRAGMA journal_mode=WAL")

        print("[LOAD] Database connection created successfully")
        return conn
    
    except Exception as e:
        print(f"[LOAD] Error : Database connection failed - {str(e)}")
        raise

def create_table(conn):

    try:
        print(f"[LOAD] Creating tables...")
        cursor = conn.cursor()

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS employee (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      age INTEGER,
                      department TEXT,
                      salary REAL,
                      annual_salary REAL,
                      tax REAL,
                      net_salary REAL,
                      salary_category TEXT,
                      join_date DATE,
                      city TEXT,
                      email TEXT,
                      year INTEGER,
                      month INTEGER
                    )

        ''') 
        print(f"[LOAD] Created 'employee' table")

        # Create department summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS department_summary (
                       department TEXT PRIMARY KEY,
                       emp_count INTEGER,
                       avg_salary REAL,
                       total_salary REAL,
                       min_salary REAL,
                       max_salary REAL
                    )
 
              ''')
        print(f"[LOAD] Created 'department_summary' table")   

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS monthly_report (
                       year INTEGER,
                       month INTEGER,
                       total_employee INTEGER,
                       avg_salary REAL,
                       total_salary REAL,
                       new_joins INTEGER,
                       PRIMARY KEY (year,month)
                    )
        ''')
        print(f"[LOAD] Created 'monthly_report' table")   

    except Exception as e:
        print(f"[LOAD] Error : Table creation failed - {str(e)}")
        raise 

def load_employees(df,conn):

    try:
        print(f"[LOAD] Loading {len(df)} employee records")

        # Insert data using pandas to sql
        df.to_sql('employee', conn, if_exists='replace',index=False)
        print(f"[LOAD] Loaded {len(df)} records into 'employee' table")

    except Exception as e:
        print(f"[LOAD] Error : Employee loading  failed - {str(e)}")
        raise

def load_department_summary(df,conn):
    try:
        print(f"[LOAD] Creating department summary")
         
        # Create summary using pandas 
        dep_summary = df.groupby('department').agg({
            'salary':['count','mean','sum','min','max']
        }).round(2)

        # Flatten column names
        dep_summary.columns = ['emp_count','avg_salary','total_salary','min_salary','max_salary']

        # Reset index
        dep_summary = dep_summary.reset_index()

        # Insert into database
        dep_summary.to_sql('department_summary',conn, if_exists='replace',index=False)

        print(f"[Load] Loaded summary for {len(dep_summary)} departments")

    except Exception as e:
        print(f"[LOAD] Error: Department summary failed - {str(e)} ")
        raise

def load_monthly_report(df,conn):
    try:
        print(f"[LOAD] Creating Monthly Report...")

        monthly = df.groupby(['year','month']).agg({
            'id': 'count',
            'salary': ['mean','sum']
        }).round(2)

        # Flatten columns names

        monthly.columns = ['total_employees','avg_salary','total_salary']

        monthly = monthly.reset_index()

        monthly.to_sql('monthly_report',conn,if_exists='replace',index=False)

        print(f"[LOAD] Loaded report for {len(monthly)} months")

    except Exception as e:
        print(f"[LOAD] Error : Monthly report failed - {str(e)}")
        raise

def load_data(df,db_path='output/database/company.db'):
    try:
        print(f"[LOAD] Starting data loading pipeline")

        os.makedirs(os.path.dirname(db_path),exist_ok=True)

        conn = create_database_connection(db_path)

        create_table(conn)

        load_employees(df,conn)      
        load_department_summary(df,conn)
        load_monthly_report(df,conn)

        conn.close()

        print(f"[LOAD] Data loading completed successfully")

    except Exception as e:
        print(f"[LOAD] ERROR: Data loading failed - {str(e)}")
        raise


def generate_report(db_path='output/database/company.db'):

    try:
        print(f"[LOAD] Generating reports...")

        os.makedirs('output/reports',exist_ok=True)

        conn = sqlite3.connect(db_path)

        # Generate departments analysis report
        dept_df = pd.read_sql_query('SELECT * FROM department_summary',conn)
        dept_df.to_csv('output/reports/department_analysis.csv',index=False)
        print(f"[LOAD] Generated department_analysis.csv")

        # Generate monthly report
        month_df = pd.read_sql_query('SELECT* FROM monthly_report',conn)
        month_df.to_csv('output/reports/monthly_report.csv',index=False)
        print(f"[LOAD] Generated monthly_report.csv")

        # Generate High salary employees report
        query = '''
            SELECT name, department, salary, salary_category
            from employee
            where salary_category = 'High'
            ORDER BY salary DESC
        '''  

        high_salary_df = pd.read_sql_query(query,conn)
        high_salary_df.to_csv('output/reports/high_salary_employees.csv',index=False)
        print('[LOAD] Generated high_salary_employees.csv')

        conn.close()

        print("[LOAD] Report generation completed")

    except Exception as e:
        print(f"[LOAD] ERROR: Report generation failed - {str(e)}")
        raise      







           