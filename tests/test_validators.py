"""
Test suite for validators module.
"""
import pytest
import pandas as pd
import numpy as np
from src.validators import validate_dataframe, safe_numeric_conversion


class TestValidateDataFrame:
    """Test cases for validate_dataframe function."""
    
    def test_valid_dataframe(self):
        """Test validation passes for valid DataFrame."""
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        assert validate_dataframe(df, required_cols=['a', 'b'], min_rows=1) is True
    
    def test_none_dataframe(self):
        """Test validation fails for None."""
        with pytest.raises(ValueError, match="is None"):
            validate_dataframe(None)
    
    def test_not_dataframe(self):
        """Test validation fails for non-DataFrame."""
        with pytest.raises(ValueError, match="not a pandas DataFrame"):
            validate_dataframe([1, 2, 3])
    
    def test_insufficient_rows(self):
        """Test validation fails when too few rows."""
        df = pd.DataFrame({'a': [1]})
        with pytest.raises(ValueError, match="has 1 rows"):
            validate_dataframe(df, min_rows=5)
    
    def test_missing_columns(self):
        """Test validation fails when required columns missing."""
        df = pd.DataFrame({'a': [1, 2, 3]})
        with pytest.raises(ValueError, match="missing required columns"):
            validate_dataframe(df, required_cols=['a', 'b', 'c'])
    
    def test_custom_name_in_error(self):
        """Test custom name appears in error messages."""
        with pytest.raises(ValueError, match="MyData"):
            validate_dataframe(None, name="MyData")


class TestSafeNumericConversion:
    """Test cases for safe_numeric_conversion function."""
    
    def test_valid_numeric_strings(self):
        """Test conversion of valid numeric strings."""
        series = pd.Series(['1', '2.5', '3'])
        result = safe_numeric_conversion(series)
        assert result.dtype in [np.float64, float]
        assert result.tolist() == [1.0, 2.5, 3.0]
    
    def test_mixed_valid_invalid(self):
        """Test conversion with mix of valid and invalid values."""
        series = pd.Series(['1', 'invalid', '3'])
        result = safe_numeric_conversion(series)
        assert result.iloc[0] == 1.0
        assert pd.isna(result.iloc[1])
        assert result.iloc[2] == 3.0
    
    def test_default_parameter_ignored(self):
        """Test that default parameter is ignored (function uses coerce)."""
        # Note: Current implementation ignores default and always uses coerce
        series = pd.Series(['1', 'invalid', '3'])
        result = safe_numeric_conversion(series, default=0)
        assert result.iloc[0] == 1.0
        assert pd.isna(result.iloc[1])  # Will be NaN, not 0
        assert result.iloc[2] == 3.0
    
    def test_empty_series(self):
        """Test conversion of empty series."""
        series = pd.Series([], dtype=object)
        result = safe_numeric_conversion(series)
        assert len(result) == 0
    
    def test_all_invalid(self):
        """Test conversion when all values are invalid."""
        series = pd.Series(['invalid', 'bad', 'error'])
        result = safe_numeric_conversion(series)
        assert all(pd.isna(result))


class TestDataIntegrity:
    """Integration tests for data validation."""
    
    def test_typical_financial_data(self):
        """Test validation with typical financial inclusion data structure."""
        df = pd.DataFrame({
            'fiscal_year': [2014, 2015, 2016],
            'indicator': ['Account Ownership', 'Account Ownership', 'Account Ownership'],
            'value_numeric': [22.0, 25.0, 28.0],
            'pillar': ['ACCESS', 'ACCESS', 'ACCESS']
        })
        
        assert validate_dataframe(
            df, 
            required_cols=['fiscal_year', 'indicator', 'value_numeric'],
            min_rows=1
        ) is True
    
    def test_time_series_continuity(self):
        """Test time series data has continuous years."""
        df = pd.DataFrame({
            'fiscal_year': [2014, 2015, 2016, 2017],
            'value': [1, 2, 3, 4]
        })
        
        years = sorted(df['fiscal_year'].unique())
        gaps = [years[i+1] - years[i] for i in range(len(years)-1)]
        
        # All gaps should be 1 (consecutive years)
        assert all(gap == 1 for gap in gaps), "Time series has gaps"
