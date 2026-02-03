"""
Validation utilities for robust data processing.
"""
import pandas as pd
import numpy as np
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


def validate_dataframe(df: pd.DataFrame, 
                       required_cols: Optional[List[str]] = None,
                       min_rows: int = 1,
                       name: str = "DataFrame") -> bool:
    """
    Validate DataFrame meets basic requirements.
    
    Args:
        df: DataFrame to validate
        required_cols: List of required column names
        min_rows: Minimum number of rows required
        name: Name for error messages
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails
    """
    if df is None:
        raise ValueError(f"{name} is None")
    
    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"{name} is not a pandas DataFrame (type: {type(df)})")
    
    if len(df) < min_rows:
        raise ValueError(f"{name} has {len(df)} rows, expected at least {min_rows}")
    
    if required_cols:
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise ValueError(f"{name} missing required columns: {missing_cols}")
    
    return True


def safe_numeric_conversion(series: pd.Series, 
                            default: float = np.nan) -> pd.Series:
    """
    Safely convert series to numeric, handling errors.
    
    Args:
        series: Pandas Series to convert
        default: Default value for non-convertible entries
        
    Returns:
        Numeric series
    """
    try:
        return pd.to_numeric(series, errors='coerce')
    except Exception as e:
        logger.warning(f"Error converting to numeric: {e}. Returning original.")
        return series


def safe_datetime_conversion(series: pd.Series,
                             errors: str = 'coerce') -> pd.Series:
    """
    Safely convert series to datetime, handling errors.
    
    Args:
        series: Pandas Series to convert
        errors: How to handle errors ('coerce', 'raise', 'ignore')
        
    Returns:
        Datetime series
    """
    try:
        result = pd.to_datetime(series, errors=errors)
        invalid_count = result.isna().sum() - series.isna().sum()
        if invalid_count > 0:
            logger.warning(f"{invalid_count} invalid dates converted to NaT")
        return result
    except Exception as e:
        logger.error(f"Error converting to datetime: {e}")
        return series


def check_column_types(df: pd.DataFrame,
                       expected_types: dict,
                       strict: bool = False) -> dict:
    """
    Check if DataFrame columns match expected types.
    
    Args:
        df: DataFrame to check
        expected_types: Dict of {column_name: expected_dtype}
        strict: If True, raise error on mismatch. If False, return mismatches.
        
    Returns:
        Dictionary of mismatched columns
        
    Raises:
        ValueError: If strict=True and types don't match
    """
    mismatches = {}
    
    for col, expected_type in expected_types.items():
        if col not in df.columns:
            mismatches[col] = f"Column missing"
            continue
        
        actual_type = df[col].dtype
        
        # Handle numeric types
        if expected_type in ['numeric', 'float', 'int']:
            if not pd.api.types.is_numeric_dtype(actual_type):
                mismatches[col] = f"Expected numeric, got {actual_type}"
        
        # Handle datetime
        elif expected_type == 'datetime':
            if not pd.api.types.is_datetime64_any_dtype(actual_type):
                mismatches[col] = f"Expected datetime, got {actual_type}"
        
        # Handle object/string
        elif expected_type in ['object', 'string']:
            if actual_type not in ['object', 'string']:
                mismatches[col] = f"Expected object/string, got {actual_type}"
    
    if strict and mismatches:
        raise ValueError(f"Column type mismatches: {mismatches}")
    
    return mismatches


def assert_not_empty(df: pd.DataFrame, name: str = "DataFrame") -> None:
    """
    Assert DataFrame is not empty.
    
    Args:
        df: DataFrame to check
        name: Name for error message
        
    Raises:
        AssertionError: If DataFrame is empty
    """
    assert df is not None, f"{name} is None"
    assert len(df) > 0, f"{name} is empty"


def assert_has_columns(df: pd.DataFrame, columns: List[str], name: str = "DataFrame") -> None:
    """
    Assert DataFrame has required columns.
    
    Args:
        df: DataFrame to check
        columns: List of required column names
        name: Name for error message
        
    Raises:
        AssertionError: If columns are missing
    """
    missing = set(columns) - set(df.columns)
    assert not missing, f"{name} missing columns: {missing}"


def safe_merge(left: pd.DataFrame,
               right: pd.DataFrame,
               **kwargs) -> pd.DataFrame:
    """
    Safely merge DataFrames with validation.
    
    Args:
        left: Left DataFrame
        right: Right DataFrame
        **kwargs: Arguments to pass to pd.merge()
        
    Returns:
        Merged DataFrame
        
    Raises:
        ValueError: If merge fails or produces unexpected results
    """
    try:
        # Validate inputs
        validate_dataframe(left, name="Left DataFrame")
        validate_dataframe(right, name="Right DataFrame")
        
        # Perform merge
        result = pd.merge(left, right, **kwargs)
        
        # Warn if result is unexpectedly empty
        if len(result) == 0 and len(left) > 0 and len(right) > 0:
            logger.warning("Merge produced empty result despite non-empty inputs")
        
        return result
        
    except Exception as e:
        raise ValueError(f"Error merging DataFrames: {e}")


def filter_outliers(series: pd.Series,
                    n_std: float = 3.0,
                    method: str = 'zscore') -> pd.Series:
    """
    Filter outliers from numeric series.
    
    Args:
        series: Numeric series
        n_std: Number of standard deviations for threshold
        method: Method to use ('zscore' or 'iqr')
        
    Returns:
        Boolean mask where True = keep, False = outlier
    """
    try:
        if method == 'zscore':
            z_scores = np.abs((series - series.mean()) / series.std())
            return z_scores < n_std
        
        elif method == 'iqr':
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            return (series >= lower) & (series <= upper)
        
        else:
            logger.warning(f"Unknown method '{method}', returning all True")
            return pd.Series([True] * len(series), index=series.index)
            
    except Exception as e:
        logger.error(f"Error filtering outliers: {e}")
        return pd.Series([True] * len(series), index=series.index)
