# ============================================================================
# tests/test_data_loader.py — Unit Tests for Data Loading
# ============================================================================
# PURPOSE: Verify that our data loading functions work correctly.
#
# WHY WRITE TESTS:
#   - Catches bugs early (before they reach the dashboard)
#   - Shows interviewers you write production-quality code
#   - Gives confidence when making changes (run tests → still works)
#   - Standard practice in all software teams
#
# HOW TO RUN:
#   pytest tests/
#   (or: python -m pytest tests/ -v  for verbose output)
#
# WHAT WE TEST:
#   - Does the data load successfully?
#   - Does it have the expected shape?
#   - Are the right columns present?
#   - Is the target variable correct?
# ============================================================================

import sys
from pathlib import Path

# Add src/ to import path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from data_loader import load_raw_data, get_column_info, RAW_FILE


class TestDataLoader:
    """Tests for the data_loader module."""
    
    def test_raw_file_exists(self):
        """Test that the raw CSV file exists on disk."""
        # WHAT: Check file is physically present
        # WHY: If file is missing, nothing else works
        assert RAW_FILE.exists(), f"Raw data file not found: {RAW_FILE}"
    
    def test_load_raw_data_returns_dataframe(self):
        """Test that load_raw_data returns a pandas DataFrame."""
        # WHAT: Verify the function returns correct type
        # WHY: Downstream code expects a DataFrame; anything else = crash
        df = load_raw_data()
        assert isinstance(df, pd.DataFrame), "Expected a pandas DataFrame"
    
    def test_data_shape(self):
        """Test that dataset has expected dimensions."""
        # WHAT: Check row count and column count
        # WHY: If shape is wrong, data might be corrupted or truncated
        df = load_raw_data()
        assert df.shape[0] == 1470, f"Expected 1470 rows, got {df.shape[0]}"
        assert df.shape[1] == 35, f"Expected 35 columns, got {df.shape[1]}"
    
    def test_target_column_exists(self):
        """Test that the Attrition (target) column is present."""
        # WHAT: Verify our target variable exists
        # WHY: Without it, the entire analysis is impossible
        df = load_raw_data()
        assert 'Attrition' in df.columns, "Target column 'Attrition' not found!"
    
    def test_target_values(self):
        """Test that Attrition only has 'Yes' and 'No' values."""
        # WHAT: Check for unexpected values in target
        # WHY: Any other value (null, typo) would break analysis
        df = load_raw_data()
        valid_values = {'Yes', 'No'}
        actual_values = set(df['Attrition'].unique())
        assert actual_values == valid_values, f"Unexpected values: {actual_values}"
    
    def test_key_columns_present(self):
        """Test that essential columns exist in the dataset."""
        # WHAT: Verify columns our analysis depends on
        # WHY: If renamed/missing, dashboard and SQL would break
        df = load_raw_data()
        required_cols = [
            'Age', 'Department', 'MonthlyIncome', 'JobRole',
            'OverTime', 'YearsAtCompany', 'JobSatisfaction'
        ]
        for col in required_cols:
            assert col in df.columns, f"Required column '{col}' is missing!"
    
    def test_no_null_in_critical_columns(self):
        """Test that critical columns have no missing values."""
        # WHAT: Check for NULL/NaN in important columns
        # WHY: Missing data in key columns would skew our analysis
        df = load_raw_data()
        critical = ['Age', 'Department', 'MonthlyIncome', 'Attrition']
        for col in critical:
            null_count = df[col].isnull().sum()
            assert null_count == 0, f"Column '{col}' has {null_count} null values!"
    
    def test_age_range_valid(self):
        """Test that age values are realistic (18-65)."""
        # WHAT: Sanity check on age range
        # WHY: Age of 0 or 200 would indicate data corruption
        df = load_raw_data()
        assert df['Age'].min() >= 18, f"Minimum age {df['Age'].min()} is unrealistic"
        assert df['Age'].max() <= 70, f"Maximum age {df['Age'].max()} is unrealistic"
    
    def test_income_positive(self):
        """Test that monthly income is always positive."""
        # WHAT: Verify no negative or zero salaries
        # WHY: Negative salary = data error
        df = load_raw_data()
        assert (df['MonthlyIncome'] > 0).all(), "Found non-positive income values!"
    
    def test_get_column_info(self):
        """Test that get_column_info returns expected summary."""
        df = load_raw_data()
        info = get_column_info(df)
        assert isinstance(info, pd.DataFrame)
        assert 'Column' in info.columns
        assert len(info) == 35  # One row per column
