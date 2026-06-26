# ============================================================================
# src/pipeline.py — End-to-End Data Pipeline
# ============================================================================
# PURPOSE: Run the entire data processing flow with ONE command.
#
# WHY:
#   - In real companies, data pipelines run automatically (daily/weekly)
#   - This shows you understand the concept of automated data workflows
#   - Anyone who clones your repo can run: python src/pipeline.py
#     and have everything ready (database, clean data, processed files)
#
# WHAT IT DOES:
#   1. Loads raw CSV data
#   2. Cleans and validates it
#   3. Saves processed versions
#   4. Creates SQLite database
#   5. Prints summary statistics
#
# HOW TO RUN:
#   python src/pipeline.py
# ============================================================================

import sys
from pathlib import Path

# Add src/ to path so imports work
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import load_raw_data, get_column_info
from preprocessor import clean_data, encode_categorical, save_processed_data
from database import create_database, run_query


def run_pipeline():
    """
    Execute the full data pipeline from raw CSV to analysis-ready outputs.
    
    PIPELINE STEPS:
        Raw CSV → Validate → Clean → Save → Load to Database → Verify
    """
    print("🚀 WORKFORCE INTELLIGENCE — DATA PIPELINE")
    print("=" * 60)
    
    # --- Step 1: Load raw data ---
    print("\n📥 Step 1: Loading raw data...")
    df = load_raw_data()
    
    # --- Step 2: Clean the data ---
    print("\n🧹 Step 2: Cleaning data...")
    df_clean = clean_data(df)
    
    # --- Step 3: Save cleaned version (for EDA and dashboard) ---
    print("\n💾 Step 3: Saving cleaned data...")
    save_processed_data(df_clean, "hr_attrition_cleaned.csv")
    
    # --- Step 4: Create encoded version (for any future analysis) ---
    print("\n🔄 Step 4: Encoding categorical variables...")
    df_encoded = encode_categorical(df_clean.copy())
    save_processed_data(df_encoded, "hr_attrition_encoded.csv")
    
    # --- Step 5: Create SQLite database ---
    print("\n🗄️  Step 5: Creating SQLite database...")
    create_database()
    
    # --- Step 6: Verify with a sample query ---
    print("\n✅ Step 6: Verification query...")
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
    
    # --- Summary ---
    print("\n" + "=" * 60)
    print("🎉 PIPELINE COMPLETE!")
    print("=" * 60)
    print(f"""
    📁 Files generated:
       • data/processed/hr_attrition_cleaned.csv  (for EDA/dashboard)
       • data/processed/hr_attrition_encoded.csv   (numeric version)
       • data/hr_analytics.db                      (SQLite database)
    
    📊 Next steps:
       • Run EDA notebook:  jupyter notebook notebooks/01_eda.ipynb
       • Start dashboard:   streamlit run dashboard/app.py
       • Query database:    Use sql/ files with any SQLite client
    """)


if __name__ == "__main__":
    run_pipeline()
