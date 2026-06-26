# ============================================================================
# tests/test_preprocessor.py — Unit Tests for Data Preprocessing
# ============================================================================
# PURPOSE: Verify that data cleaning works correctly.
#
# WHAT WE TEST:
#   - Does cleaning reduce columns? (constant columns removed)
#   - Is the target encoded correctly? (Yes→1, No→0)
#   - Are there no duplicates after cleaning?
#   - Does encoding produce only numeric columns?
# ============================================================================

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
import numpy as np
from data_loader import load_raw_data
from preprocessor import clean_data, encode_categorical


class TestPreprocessor:
    """Tests for the preprocessor module."""
    
    def test_clean_removes_constant_columns(self):
        """Test that columns with only one unique value are removed."""
        df = load_raw_data()
        df_clean = clean_data(df)
        # EmployeeCount, Over18, StandardHours should be removed
        assert 'EmployeeCount' not in df_clean.columns
        assert 'Over18' not in df_clean.columns
        assert 'StandardHours' not in df_clean.columns
    
    def test_clean_encodes_target(self):
        """Test that Attrition is converted from Yes/No to 1/0."""
        df = load_raw_data()
        df_clean = clean_data(df)
        # Should only have 0 and 1
        assert set(df_clean['Attrition'].unique()) == {0, 1}
    
    def test_clean_no_duplicates(self):
        """Test that no duplicate rows remain after cleaning."""
        df = load_raw_data()
        df_clean = clean_data(df)
        assert df_clean.duplicated().sum() == 0
    
    def test_clean_preserves_row_count(self):
        """Test that cleaning doesn't accidentally drop rows."""
        df = load_raw_data()
        df_clean = clean_data(df)
        # Original has 1470 rows, cleaning should keep all (no duplicates in this dataset)
        assert len(df_clean) == 1470
    
    def test_encode_produces_numeric(self):
        """Test that encoding converts all columns to numeric."""
        df = load_raw_data()
        df_clean = clean_data(df)
        df_encoded = encode_categorical(df_clean)
        # All columns should be numeric after encoding
        non_numeric = df_encoded.select_dtypes(include=['object', 'string']).columns.tolist()
        assert len(non_numeric) == 0, f"Non-numeric columns remain: {non_numeric}"
    
    def test_encode_increases_columns(self):
        """Test that one-hot encoding creates more columns."""
        df = load_raw_data()
        df_clean = clean_data(df)
        df_encoded = encode_categorical(df_clean)
        # One-hot encoding always increases column count
        assert df_encoded.shape[1] > df_clean.shape[1]
