# ============================================================================
# src/preprocessor.py — Data Cleaning & Transformation
# ============================================================================
# PURPOSE: Take raw messy data and make it clean, consistent, and ready
#          for analysis and machine learning.
#
# WHY DATA CLEANING MATTERS:
#   - Real-world data is NEVER perfect (missing values, duplicates, typos)
#   - ML models can't handle text categories directly (need encoding)
#   - Inconsistent data leads to wrong conclusions
#   - This is 60-80% of a Data Analyst's actual work!
#
# WHAT THIS FILE DOES:
#   1. Removes useless columns (same value for every row)
#   2. Encodes the target variable (Yes/No → 1/0)
#   3. Handles categorical variables
#   4. Saves clean data to data/processed/
# ============================================================================

import pandas as pd
import numpy as np
from pathlib import Path
from data_loader import load_raw_data, PROCESSED_DATA_DIR


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw HR dataset.

    STEP-BY-STEP:
        1. Drop columns with zero variance (same value for ALL rows)
        2. Convert target 'Attrition' from Yes/No to 1/0
        3. Remove duplicate rows (if any)
        4. Reset the index for clean numbering

    WHY EACH STEP:
        - Zero-variance columns add no information (waste of space)
        - ML models need numbers, not text (Yes/No → 1/0)
        - Duplicates can bias your analysis
        - Clean index makes debugging easier

    PARAMETERS:
        df — Raw DataFrame from load_raw_data()

    RETURNS:
        Cleaned DataFrame ready for feature engineering
    """
    print("🧹 Starting data cleaning...")
    print(f"   Input shape: {df.shape}")

    # --- Step 1: Drop columns that have the SAME value for every row ---
    # WHY: If every employee has EmployeeCount=1, it tells us nothing useful
    # HOW: nunique() counts distinct values. If only 1 unique value → useless
    cols_before = df.shape[1]
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    df = df.drop(columns=constant_cols)
    print(f"   ❌ Dropped {len(constant_cols)} constant columns: {constant_cols}")

    # --- Step 2: Encode target variable ---
    # WHY: 'Attrition' is our TARGET (what we want to predict)
    #      ML models need numbers: Yes=1 (left), No=0 (stayed)
    # HOW: .map() replaces values based on a dictionary
    df["Attrition"] = df["Attrition"].map({"Yes": 1, "No": 0})
    print(f"   ✅ Encoded 'Attrition': Yes→1, No→0")

    # --- Step 3: Remove duplicates ---
    # WHY: Duplicate rows can make our model think a pattern is more
    #      common than it actually is (overfitting)
    dupes = df.duplicated().sum()
    df = df.drop_duplicates()
    print(f"   {'❌' if dupes > 0 else '✅'} Duplicates found: {dupes}")

    # --- Step 4: Reset index ---
    # WHY: After dropping rows, the index has gaps (0,1,3,5...)
    #      Reset gives clean sequential numbers (0,1,2,3...)
    df = df.reset_index(drop=True)

    print(f"   Output shape: {df.shape}")
    print("✅ Data cleaning complete!\n")

    return df


def encode_categorical(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert text/categorical columns to numbers for ML.

    WHY:
        Machine learning models only understand NUMBERS.
        Text like "Sales", "Research" needs to be converted.

    METHODS USED:
        - Label Encoding: For binary categories (Male/Female → 0/1)
        - One-Hot Encoding: For multi-category columns (Department → 3 columns)

    ONE-HOT ENCODING EXPLAINED:
        Department has 3 values: Sales, R&D, HR
        Instead of: Sales=0, R&D=1, HR=2 (implies order that doesn't exist!)
        We create: Department_Sales=1/0, Department_RD=1/0, Department_HR=1/0
        Each row gets a 1 in its department column, 0 elsewhere.
    """
    print("🔄 Encoding categorical variables...")

    # --- Binary encoding for columns with exactly 2 unique values ---
    # Example: Gender (Male/Female), OverTime (Yes/No)
    binary_cols = [col for col in df.select_dtypes(include="object").columns
                   if df[col].nunique() == 2]

    for col in binary_cols:
        # Get the two unique values
        values = df[col].unique()
        # Map first value to 0, second to 1
        df[col] = df[col].map({values[0]: 0, values[1]: 1})
        print(f"   Binary encoded: {col} → {values[0]}=0, {values[1]}=1")

    # --- One-Hot encoding for multi-category columns ---
    # Example: Department (Sales, R&D, HR) → 3 separate 0/1 columns
    multi_cat_cols = df.select_dtypes(include="object").columns.tolist()

    if multi_cat_cols:
        # pd.get_dummies creates the one-hot encoded columns
        # drop_first=True: removes one category to avoid multicollinearity
        # WHY drop_first? If someone is NOT in Sales and NOT in HR, they MUST
        # be in R&D. So we don't need all 3 columns — 2 is enough.
        df = pd.get_dummies(df, columns=multi_cat_cols, drop_first=True)
        print(f"   One-hot encoded: {multi_cat_cols}")

    print(f"   Final shape after encoding: {df.shape}")
    print("✅ Encoding complete!\n")

    return df


def save_processed_data(df: pd.DataFrame, filename: str = "hr_attrition_cleaned.csv") -> Path:
    """
    Save the cleaned DataFrame to the processed data folder.

    WHY SAVE:
        - Don't repeat cleaning every time you open a notebook
        - Keeps raw data untouched (you can always re-clean)
        - Other scripts/dashboard can load the clean version directly
    """
    # Create the directory if it doesn't exist
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DATA_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"💾 Saved processed data to: {output_path}")
    print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")

    return output_path


# ---------------------------------------------------------------------------
# MAIN — Full preprocessing pipeline
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Step 1: Load raw data
    df = load_raw_data()

    # Step 2: Clean it
    df_clean = clean_data(df)

    # Step 3: Save cleaned (but not encoded) version — useful for EDA
    save_processed_data(df_clean, "hr_attrition_cleaned.csv")

    # Step 4: Encode for ML
    df_encoded = encode_categorical(df_clean.copy())

    # Step 5: Save ML-ready version
    save_processed_data(df_encoded, "hr_attrition_ml_ready.csv")

    print("\n🎉 Preprocessing pipeline complete!")
    print(f"   Cleaned data: data/processed/hr_attrition_cleaned.csv")
    print(f"   ML-ready data: data/processed/hr_attrition_ml_ready.csv")
