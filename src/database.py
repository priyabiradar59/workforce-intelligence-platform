# ============================================================================
# src/database.py — Load CSV data into SQLite database
# ============================================================================
# PURPOSE: Create a SQLite database and load the HR dataset into it.
#
# WHY:
#   - Demonstrates you can work with DATABASES, not just CSVs
#   - SQL queries in sql/ folder can run against this database
#   - Dashboard can query the database for live data
#   - Shows real-world data pipeline: CSV → Database → Analysis
#
# HOW:
#   - SQLAlchemy creates the database connection
#   - pandas .to_sql() loads the DataFrame directly into a table
#   - SQLite stores everything in one file (no server needed!)
# ============================================================================

import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# Import our data loader
import sys
sys.path.insert(0, str(Path(__file__).parent))
from data_loader import load_raw_data


def create_database() -> str:
    """
    Create a SQLite database and load HR data into it.
    
    WHAT HAPPENS:
        1. Creates a file called 'hr_analytics.db' in data/ folder
        2. Loads the raw CSV data into a table called 'employees'
        3. Returns the path to the database file
    
    WHY SQLite:
        - No installation needed (comes with Python!)
        - Entire database is ONE file (easy to share)
        - Supports standard SQL (same syntax as MySQL/PostgreSQL)
        - Perfect for portfolio projects and small datasets
    """
    # Define where to store the database
    db_path = Path(__file__).parent.parent / "data" / "hr_analytics.db"
    
    # Create SQLAlchemy engine (the connection to the database)
    # 'sqlite:///' + path = tells Python to use SQLite at that location
    engine = create_engine(f"sqlite:///{db_path}")
    
    # Load the raw data
    df = load_raw_data()
    
    # Load DataFrame into the database as a table called 'employees'
    # if_exists='replace': if table already exists, drop and recreate it
    # index=False: don't save the DataFrame index as a column
    df.to_sql('employees', engine, if_exists='replace', index=False)
    
    print(f"\n💾 Database created: {db_path}")
    print(f"   Table 'employees': {df.shape[0]} rows loaded")
    
    # Verify by running a quick query
    result = pd.read_sql("SELECT COUNT(*) as total FROM employees", engine)
    print(f"   Verification query: {result['total'].iloc[0]} records confirmed")
    
    return str(db_path)


def run_query(query: str) -> pd.DataFrame:
    """
    Run a SQL query against the HR database and return results as DataFrame.
    
    PARAMETERS:
        query (str) — Any SQL SELECT statement
    
    RETURNS:
        pd.DataFrame — Query results as a pandas table
    
    EXAMPLE:
        >>> from src.database import run_query
        >>> result = run_query("SELECT Department, COUNT(*) FROM employees GROUP BY Department")
        >>> print(result)
    """
    db_path = Path(__file__).parent.parent / "data" / "hr_analytics.db"
    
    if not db_path.exists():
        print("⚠️  Database not found! Creating it now...")
        create_database()
    
    engine = create_engine(f"sqlite:///{db_path}")
    return pd.read_sql(query, engine)


# ---------------------------------------------------------------------------
# MAIN — Create database and run sample queries
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Step 1: Create the database
    create_database()
    
    # Step 2: Run sample queries to demonstrate it works
    print("\n" + "=" * 60)
    print("📊 SAMPLE SQL QUERIES")
    print("=" * 60)
    
    # Query 1: Attrition by Department
    print("\n🔍 Query: Attrition rate by department")
    result = run_query("""
        SELECT 
            Department,
            COUNT(*) AS total,
            SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
            ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate
        FROM employees
        GROUP BY Department
        ORDER BY attrition_rate DESC
    """)
    print(result.to_string(index=False))
    
    # Query 2: Top 5 highest paid who left
    print("\n🔍 Query: Top 5 highest-paid employees who left")
    result = run_query("""
        SELECT EmployeeNumber, Department, JobRole, MonthlyIncome, YearsAtCompany
        FROM employees
        WHERE Attrition = 'Yes'
        ORDER BY MonthlyIncome DESC
        LIMIT 5
    """)
    print(result.to_string(index=False))
    
    print("\n✅ Database ready! Run SQL queries from sql/ folder against data/hr_analytics.db")
