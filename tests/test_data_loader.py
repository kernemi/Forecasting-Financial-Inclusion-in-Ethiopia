"""
Test suite for data_loader module.
"""
import pytest
import pandas as pd
import os


class TestDataStructure:
    """Test cases for data file structure and integrity."""
    
    def test_required_directories_exist(self):
        """Test that all required data directories exist."""
        required_dirs = [
            'data/raw',
            'data/processed',
            'data/enriched'
        ]
        
        for directory in required_dirs:
            assert os.path.exists(directory), f"Missing directory: {directory}"
    
    def test_processed_data_files_exist(self):
        """Test that key processed data files exist."""
        expected_files = [
            'data/processed/account_ownership_timeseries.csv',
            'data/processed/digital_adoption_timeseries.csv',
        ]
        
        for filepath in expected_files:
            assert os.path.exists(filepath), f"Missing file: {filepath}"
    
    def test_csv_files_readable(self):
        """Test that CSV files can be read without errors."""
        csv_files = [
            'data/processed/account_ownership_timeseries.csv',
            'data/processed/digital_adoption_timeseries.csv',
        ]
        
        for filepath in csv_files:
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)
                assert isinstance(df, pd.DataFrame)
                assert len(df) > 0, f"Empty file: {filepath}"


class TestProcessedDataQuality:
    """Test cases for processed data quality."""
    
    def test_account_ownership_data_structure(self):
        """Test account ownership time series structure."""
        filepath = 'data/processed/account_ownership_timeseries.csv'
        if not os.path.exists(filepath):
            pytest.skip(f"File not found: {filepath}")
        
        df = pd.read_csv(filepath)
        
        # Check for essential columns
        assert 'fiscal_year' in df.columns or 'year' in df.columns
        assert len(df) > 0
        
    def test_digital_adoption_data_structure(self):
        """Test digital adoption time series structure."""
        filepath = 'data/processed/digital_adoption_timeseries.csv'
        if not os.path.exists(filepath):
            pytest.skip(f"File not found: {filepath}")
        
        df = pd.read_csv(filepath)
        
        # Check for essential columns
        assert 'fiscal_year' in df.columns or 'year' in df.columns
        assert len(df) > 0
    
    def test_no_duplicate_years(self):
        """Test that time series data has no duplicate years."""
        filepaths = [
            'data/processed/account_ownership_timeseries.csv',
            'data/processed/digital_adoption_timeseries.csv',
        ]
        
        for filepath in filepaths:
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)
                year_col = 'fiscal_year' if 'fiscal_year' in df.columns else 'year'
                if year_col in df.columns:
                    duplicates = df[year_col].duplicated().sum()
                    assert duplicates == 0, f"Found {duplicates} duplicate years in {filepath}"
