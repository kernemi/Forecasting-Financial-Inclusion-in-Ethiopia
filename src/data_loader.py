"""
Data loading utilities for Ethiopia Financial Inclusion project.
"""
import pandas as pd
from typing import Tuple, Dict, Optional
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    """Custom exception for data loading errors."""
    pass


class FinancialInclusionDataLoader:
    """Load and prepare financial inclusion datasets with robust error handling."""
    
    # Required columns for validation
    REQUIRED_DATA_COLUMNS = [
        'record_id', 'record_type', 'indicator', 'indicator_code',
        'observation_date', 'source_name'
    ]
    
    REQUIRED_IMPACT_COLUMNS = [
        'parent_id', 'child_id', 'impact_direction', 'lag_months'
    ]
    
    def __init__(self, data_dir: str = '../data/raw'):
        """
        Initialize data loader.
        
        Args:
            data_dir: Path to raw data directory
            
        Raises:
            DataLoadError: If data directory doesn't exist
        """
        if not os.path.exists(data_dir):
            raise DataLoadError(f"Data directory not found: {data_dir}")
        
        self.data_dir = data_dir
        self.data_path = os.path.join(data_dir, 'ethiopia_fi_unified_data.xlsx')
        self.reference_path = os.path.join(data_dir, 'reference_codes.xlsx')
        
        # Validate file existence
        if not os.path.exists(self.data_path):
            raise DataLoadError(f"Main data file not found: {self.data_path}")
        if not os.path.exists(self.reference_path):
            logger.warning(f"Reference file not found: {self.reference_path}")
        
    def load_all_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Load all datasets with robust error handling.
        
        Returns:
            Tuple of (main_data, impact_links, reference_codes)
            
        Raises:
            DataLoadError: If files cannot be loaded or validation fails
        """
        logger.info("Loading datasets...")
        
        try:
            # Load main data with error handling
            excel_file = pd.ExcelFile(self.data_path)
            
            if len(excel_file.sheet_names) < 2:
                raise DataLoadError(
                    f"Expected at least 2 sheets, found {len(excel_file.sheet_names)}"
                )
            
            df_data = pd.read_excel(self.data_path, sheet_name=excel_file.sheet_names[0])
            df_impact = pd.read_excel(self.data_path, sheet_name=excel_file.sheet_names[1])
            
        except FileNotFoundError as e:
            raise DataLoadError(f"File not found: {e}")
        except Exception as e:
            raise DataLoadError(f"Error loading Excel file: {e}")
        
        # Validate main data
        self._validate_dataframe(df_data, self.REQUIRED_DATA_COLUMNS, "Main data")
        
        # Validate impact data (if not empty)
        if len(df_impact) > 0:
            self._validate_dataframe(df_impact, self.REQUIRED_IMPACT_COLUMNS, "Impact data")
        
        try:
            # Load reference codes (optional)
            df_reference = pd.read_excel(self.reference_path)
            logger.info(f"✓ Reference codes: {len(df_reference)} codes")
        except Exception as e:
            logger.warning(f"Could not load reference codes: {e}. Continuing with empty DataFrame.")
            df_reference = pd.DataFrame()
        
        logger.info(f"✓ Main data: {len(df_data)} records")
        logger.info(f"✓ Impact links: {len(df_impact)} records")
        
        return df_data, df_impact, df_reference
    
    def _validate_dataframe(self, df: pd.DataFrame, required_cols: list, name: str) -> None:
        """
        Validate DataFrame has required columns.
        
        Args:
            df: DataFrame to validate
            required_cols: List of required column names
            name: Name for error messages
            
        Raises:
            DataLoadError: If validation fails
        """
        if df is None or len(df) == 0:
            logger.warning(f"{name} is empty")
            return
        
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise DataLoadError(
                f"{name} missing required columns: {missing_cols}"
            )
    
    def get_observations(self, df_data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract and prepare observations with error handling.
        
        Args:
            df_data: Main data DataFrame
            
        Returns:
            Observations DataFrame
            
        Raises:
            DataLoadError: If required columns missing or data malformed
        """
        if df_data is None or len(df_data) == 0:
            logger.warning("Empty DataFrame provided to get_observations")
            return pd.DataFrame()
        
        if 'record_type' not in df_data.columns:
            raise DataLoadError("Missing 'record_type' column in data")
        
        try:
            observations = df_data[df_data['record_type'] == 'observation'].copy()
            
            if len(observations) == 0:
                logger.warning("No observations found in dataset")
                return observations
            
            # Convert dates with error handling
            observations['observation_date'] = pd.to_datetime(
                observations['observation_date'], errors='coerce'
            )
            
            # Check for invalid dates
            invalid_dates = observations['observation_date'].isna().sum()
            if invalid_dates > 0:
                logger.warning(f"{invalid_dates} observations have invalid dates")
            
            observations['year'] = observations['observation_date'].dt.year
            
            return observations
            
        except Exception as e:
            raise DataLoadError(f"Error extracting observations: {e}")
    
    def get_events(self, df_data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract and prepare events with error handling.
        
        Args:
            df_data: Main data DataFrame
            
        Returns:
            Events DataFrame
            
        Raises:
            DataLoadError: If required columns missing or data malformed
        """
        if df_data is None or len(df_data) == 0:
            logger.warning("Empty DataFrame provided to get_events")
            return pd.DataFrame()
        
        if 'record_type' not in df_data.columns:
            raise DataLoadError("Missing 'record_type' column in data")
        
        try:
            events = df_data[df_data['record_type'] == 'event'].copy()
            
            if len(events) == 0:
                logger.warning("No events found in dataset")
                return events
            
            # Convert dates with error handling
            events['event_date'] = pd.to_datetime(
                events['observation_date'], errors='coerce'
            )
            
            # Check for invalid dates
            invalid_dates = events['event_date'].isna().sum()
            if invalid_dates > 0:
                logger.warning(f"{invalid_dates} events have invalid dates")
            
            events['year'] = events['event_date'].dt.year
            
            return events
            
        except Exception as e:
            raise DataLoadError(f"Error extracting events: {e}")
    
    def get_time_series(self, observations: pd.DataFrame, indicator_code: str) -> pd.DataFrame:
        """
        Get time series for a specific indicator with validation.
        
        Args:
            observations: Observations dataframe
            indicator_code: Indicator code to filter
            
        Returns:
            Time series dataframe
            
        Raises:
            DataLoadError: If required columns missing
        """
        if observations is None or len(observations) == 0:
            logger.warning("Empty observations DataFrame provided")
            return pd.DataFrame()
        
        required_cols = ['indicator_code', 'observation_date', 'year', 'value_numeric']
        missing_cols = set(required_cols) - set(observations.columns)
        if missing_cols:
            raise DataLoadError(f"Missing required columns: {missing_cols}")
        
        try:
            ts = observations[observations['indicator_code'] == indicator_code].copy()
            
            if len(ts) == 0:
                logger.warning(f"No data found for indicator: {indicator_code}")
                return ts
            
            ts = ts.sort_values('observation_date')
            
            # Select available columns
            available_cols = [col for col in 
                ['observation_date', 'year', 'value_numeric', 'confidence', 'source_name']
                if col in ts.columns
            ]
            
            return ts[available_cols]
            
        except Exception as e:
            raise DataLoadError(f"Error getting time series for {indicator_code}: {e}")
    
    def get_pillar_summary(self, observations: pd.DataFrame) -> Dict:
        """
        Get summary statistics by pillar with validation.
        
        Args:
            observations: Observations DataFrame
            
        Returns:
            Dictionary of pillar summaries
        """
        if observations is None or len(observations) == 0:
            logger.warning("Empty observations DataFrame provided")
            return {}
        
        required_cols = ['pillar', 'indicator_code', 'year']
        missing_cols = set(required_cols) - set(observations.columns)
        if missing_cols:
            logger.warning(f"Missing columns for pillar summary: {missing_cols}")
            return {}
        
        try:
            summary = {}
            pillars = observations['pillar'].dropna().unique()
            
            for pillar in pillars:
                pillar_data = observations[observations['pillar'] == pillar]
                summary[pillar] = {
                    'count': len(pillar_data),
                    'indicators': pillar_data['indicator_code'].nunique(),
                    'years': pillar_data['year'].nunique(),
                    'date_range': (
                        int(pillar_data['year'].min()) if not pillar_data['year'].isna().all() else None,
                        int(pillar_data['year'].max()) if not pillar_data['year'].isna().all() else None
                    )
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating pillar summary: {e}")
            return {}
