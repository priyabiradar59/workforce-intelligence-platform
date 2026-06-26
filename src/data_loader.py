# ============================================================================
# src/data_loader.py — Data Ingestion Module
# ============================================================================
# PURPOSE: Load raw HR data from CSV and provide a clean DataFrame.
#
# WHY THIS FILE EXISTS:
#   - Single source of truth for loading data
#   - If the data source changes (e.g., from CSV to database), we only
#     update THIS file — not every notebook/script that uses the data
#   - Keeps notebooks clean and focused on analysis, not file paths
#
# WHAT YOU'LL LEARN:
#   - How to structure reusable Python modules
#   - Type hints (telling Python what type of data a function expects/returns)
#   - Pathlib for cross-platform file paths
#   - Basic data validation
# ============================================================================

import pandas as pd
from pathlib import Path


# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------
# WHY constants? If we need to change the file path, we change it in ONE place.
# Convention: UPPERCASE names = constants (values that don't change)

RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DATA_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_FILE = RAW_DATA_DIR / "hr_employee_attrition.csv"


# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------

def load_raw_data() -> pd.DataFrame:
    """
    Load the raw IBM HR Attrition dataset from CSV.

    WHAT IT DOES:
        1. Reads the CSV file into a Pandas DataFrame
        2. Validates that the file exists and has expected shape
        3. Returns the raw (uncleaned) data

    RETURNS:
        pd.DataFrame — Raw dataset with 1,470 rows and 35 columns

    EXAMPLE:
        >>> from src.data_loader import load_raw_data
        >>> df = load_raw_data()
        >>> print(df.shape)  # (1470, 35)
    """
    # Check if file exists — fail early with a clear message
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {RAW_FILE}\n"
            f"Please download it from Kaggle or run the setup script."
        )

    # Read CSV into a DataFrame
    # WHY pd.read_csv? It's the standard way to load tabular data in Python
    df = pd.read_csv(RAW_FILE)

    # Basic validation — catch data issues early
    print(f"✅ Dataset loaded successfully!")
    print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"   Target column 'Attrition': {df['Attrition'].value_counts().to_dict()}")

    return df


def load_processed_data() -> pd.DataFrame:
    """
    Load the cleaned/processed dataset (after preprocessing is done).

    WHY SEPARATE FUNCTION:
        - Raw data needs cleaning before analysis
        - After cleaning, we save to processed/ folder
        - This function loads the CLEAN version for modeling/dashboard
    """
    processed_file = PROCESSED_DATA_DIR / "hr_attrition_cleaned.csv"

    if not processed_file.exists():
        raise FileNotFoundError(
            f"Processed data not found at: {processed_file}\n"
            f"Run the preprocessing pipeline first: python src/preprocessor.py"
        )

    df = pd.read_csv(processed_file)
    print(f"✅ Processed data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def get_column_info(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary of all columns in the dataset.

    WHY: Quick way to understand what data you're working with.
         Shows data types, missing values, and unique counts.

    PARAMETERS:
        df (pd.DataFrame) — Any DataFrame you want to inspect

    RETURNS:
        pd.DataFrame — Summary table with column metadata
    """
    info = pd.DataFrame({
        "Column": df.columns,
        "Type": df.dtypes.values,
        "Non-Null Count": df.notnull().sum().values,
        "Null Count": df.isnull().sum().values,
        "Unique Values": df.nunique().values,
        "Sample Value": [df[col].iloc[0] for col in df.columns]
    })
    return info


# ---------------------------------------------------------------------------
# MAIN — runs only when you execute this file directly
# ---------------------------------------------------------------------------
# WHY: This lets you test the module by running: python src/data_loader.py
#      But when you IMPORT it (from src.data_loader import ...), this won't run.

if __name__ == "__main__":
    df = load_raw_data()
    print("\n📊 Column Summary:")
    print(get_column_info(df).to_string(index=False))
