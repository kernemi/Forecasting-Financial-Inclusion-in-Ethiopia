"""
Analysis utilities for Ethiopia Financial Inclusion project.
"""
import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Tuple, Optional

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class AnalysisError(Exception):
    """Custom exception for analysis errors."""
    pass


class FinancialInclusionAnalyzer:
    """Analyze financial inclusion trends and patterns."""
    
    def __init__(self, observations: pd.DataFrame, events: pd.DataFrame = None):
        """
        Initialize analyzer.
        
        Args:
            observations: Observations dataframe
            events: Events dataframe (optional)
        
        Raises:
            AnalysisError: If observations is empty or missing required columns
        """
        if observations is None or len(observations) == 0:
            raise AnalysisError("Observations dataframe cannot be empty")
        
        required_cols = ['indicator_code', 'year', 'value_numeric']
        missing_cols = set(required_cols) - set(observations.columns)
        if missing_cols:
            raise AnalysisError(f"Missing required columns: {missing_cols}")
        
        self.observations = observations
        self.events = events
        logger.info(f"Initialized analyzer with {len(observations)} observations")
        
    def calculate_growth_rate(self, indicator_code: str) -> pd.DataFrame:
        """
        Calculate year-over-year growth rates for an indicator.
        
        Args:
            indicator_code: Indicator to analyze
            
        Returns:
            DataFrame with growth rates (empty if insufficient data)
        
        Raises:
            AnalysisError: If calculation fails
        """
        if not indicator_code:
            logger.warning("Empty indicator_code provided")
            return pd.DataFrame()
        
        try:
            data = self.observations[
                self.observations['indicator_code'] == indicator_code
            ].sort_values('year')
            
            if len(data) < 2:
                logger.warning(f"Insufficient data for {indicator_code} (need >= 2 points)")
                return pd.DataFrame()
            
            growth = data.copy()
            growth['growth_rate'] = growth['value_numeric'].pct_change() * 100
            growth['growth_pp'] = growth['value_numeric'].diff()
            
            return growth[['year', 'value_numeric', 'growth_rate', 'growth_pp']]
            
        except KeyError as e:
            raise AnalysisError(f"Missing column in data: {e}")
        except Exception as e:
            raise AnalysisError(f"Error calculating growth rate for {indicator_code}: {e}")
    
    def identify_trend_changes(self, indicator_code: str, threshold: float = 0.5) -> List[Dict]:
        """
        Identify significant trend changes.
        
        Args:
            indicator_code: Indicator to analyze
            threshold: Minimum change threshold (percentage points)
            
        Returns:
            List of trend change points
        
        Raises:
            AnalysisError: If analysis fails
        """
        try:
            growth = self.calculate_growth_rate(indicator_code)
            
            if growth.empty:
                logger.warning(f"No growth data for {indicator_code}")
                return []
            
            changes = []
            for i in range(1, len(growth)):
                current = growth.iloc[i]
                previous = growth.iloc[i-1]
                
                if pd.notna(current['growth_pp']) and abs(current['growth_pp']) < threshold:
                    if pd.notna(previous['growth_pp']) and abs(previous['growth_pp']) >= threshold:
                        changes.append({
                            'year': current['year'],
                            'type': 'slowdown',
                            'previous_growth': previous['growth_pp'],
                            'current_growth': current['growth_pp']
                        })
            
            logger.info(f"Found {len(changes)} trend changes for {indicator_code}")
            return changes
            
        except Exception as e:
            raise AnalysisError(f"Error identifying trend changes for {indicator_code}: {e}")
    
    def analyze_gender_gap(self) -> pd.DataFrame:
        """
        Analyze gender gap in financial inclusion.
        
        Returns:
            DataFrame with gender gap data
        
        Raises:
            AnalysisError: If analysis fails
        """
        try:
            if 'pillar' not in self.observations.columns:
                logger.warning("'pillar' column not found in observations")
                return pd.DataFrame()
            
            gender_data = self.observations[
                self.observations['pillar'] == 'GENDER'
            ].sort_values('year')
            
            if len(gender_data) == 0:
                logger.warning("No gender data found")
                return pd.DataFrame()
            
            # Extract gender gap values
            gap_data = gender_data[gender_data['indicator_code'].str.contains('GAP', na=False)]
            
            if len(gap_data) == 0:
                logger.warning("No gap indicators found in gender data")
                return pd.DataFrame()
            
            required_cols = ['year', 'indicator_code', 'value_numeric', 'indicator']
            available_cols = [col for col in required_cols if col in gap_data.columns]
            
            return gap_data[available_cols]
            
        except Exception as e:
            raise AnalysisError(f"Error analyzing gender gap: {e}")
    
    def compare_pillars(self) -> pd.DataFrame:
        """
        Compare growth across pillars.
        
        Returns:
            DataFrame with pillar comparison
        
        Raises:
            AnalysisError: If comparison fails
        """
        try:
            if 'pillar' not in self.observations.columns:
                raise AnalysisError("'pillar' column not found in observations")
            
            pillar_summary = []
            
            for pillar in self.observations['pillar'].unique():
                if pd.isna(pillar):
                    continue
                    
                pillar_obs = self.observations[self.observations['pillar'] == pillar]
                
                if len(pillar_obs) > 0:
                    # Safe min/max calculation
                    years = pillar_obs['year'].dropna()
                    first_year = years.min() if len(years) > 0 else None
                    last_year = years.max() if len(years) > 0 else None
                    
                    pillar_summary.append({
                        'pillar': pillar,
                        'observations': len(pillar_obs),
                        'indicators': pillar_obs['indicator_code'].nunique(),
                        'years_coverage': pillar_obs['year'].nunique(),
                        'first_year': first_year,
                        'last_year': last_year
                    })
            
            if len(pillar_summary) == 0:
                logger.warning("No pillar data found for comparison")
                return pd.DataFrame()
            
            return pd.DataFrame(pillar_summary)
            
        except Exception as e:
            raise AnalysisError(f"Error comparing pillars: {e}")
    
    def find_event_correlations(self, indicator_code: str, lag_months: int = 6) -> pd.DataFrame:
        """
        Find events that may correlate with indicator changes.
        
        Args:
            indicator_code: Indicator to analyze
            lag_months: Lag period to consider
            
        Returns:
            DataFrame with potential correlations
        
        Raises:
            AnalysisError: If correlation analysis fails
        """
        if self.events is None or len(self.events) == 0:
            logger.warning("No events data available for correlation analysis")
            return pd.DataFrame()
        
        try:
            # Validate required columns
            if 'observation_date' not in self.observations.columns:
                logger.warning("'observation_date' not found, cannot find correlations")
                return pd.DataFrame()
            
            if 'event_date' not in self.events.columns:
                logger.warning("'event_date' not found in events, cannot find correlations")
                return pd.DataFrame()
            
            indicator_data = self.observations[
                self.observations['indicator_code'] == indicator_code
            ].sort_values('observation_date')
            
            if len(indicator_data) == 0:
                logger.warning(f"No observations found for {indicator_code}")
                return pd.DataFrame()
            
            correlations = []
            
            for _, obs in indicator_data.iterrows():
                if pd.isna(obs['observation_date']):
                    continue
                    
                # Find events within lag period before observation
                try:
                    event_window_start = obs['observation_date'] - pd.DateOffset(months=lag_months)
                    event_window_end = obs['observation_date']
                    
                    relevant_events = self.events[
                        (self.events['event_date'] >= event_window_start) &
                        (self.events['event_date'] <= event_window_end)
                    ]
                    
                    for _, event in relevant_events.iterrows():
                        if pd.isna(event['event_date']):
                            continue
                            
                        lag = (obs['observation_date'] - event['event_date']).days / 30
                        correlations.append({
                            'event': event.get('indicator', 'Unknown'),
                            'event_date': event['event_date'],
                            'observation_date': obs['observation_date'],
                            'lag_months': round(lag, 1),
                            'value': obs['value_numeric']
                        })
                except Exception as e:
                    logger.warning(f"Error processing observation date {obs.get('observation_date')}: {e}")
                    continue
            
            logger.info(f"Found {len(correlations)} potential correlations for {indicator_code}")
            return pd.DataFrame(correlations)
            
        except Exception as e:
            raise AnalysisError(f"Error finding event correlations for {indicator_code}: {e}")
    
    def get_key_insights(self) -> List[str]:
        """Generate key insights from the data."""
        insights = []
        
        # 1. Temporal coverage
        year_range = self.observations['year'].max() - self.observations['year'].min()
        insights.append(
            f"Dataset spans {year_range + 1} years ({self.observations['year'].min()}-{self.observations['year'].max()})"
        )
        
        # 2. Data concentration
        recent_data = self.observations[self.observations['year'] >= 2024]
        recent_pct = len(recent_data) / len(self.observations) * 100
        insights.append(
            f"{recent_pct:.1f}% of observations are from 2024 onwards, indicating recent data focus"
        )
        
        # 3. Pillar distribution
        pillar_counts = self.observations['pillar'].value_counts()
        top_pillar = pillar_counts.index[0]
        insights.append(
            f"{top_pillar} pillar has the most data ({pillar_counts.iloc[0]} observations)"
        )
        
        # 4. Confidence levels
        high_conf = (self.observations['confidence'] == 'high').sum()
        high_conf_pct = high_conf / len(self.observations) * 100
        insights.append(
            f"{high_conf_pct:.1f}% of observations have high confidence"
        )
        
        # 5. Event coverage
        if self.events is not None and len(self.events) > 0:
            event_categories = self.events['category'].nunique()
            insights.append(
                f"{len(self.events)} events documented across {event_categories} categories"
            )
        
        return insights


class DataValidator:
    """
    Validate data schema, pillar rules, and record_type semantics.
    Ensures enrichment pipeline maintains data integrity.
    """
    
    # Schema definition
    REQUIRED_COLUMNS = [
        'record_id', 'record_type', 'pillar', 'indicator', 'indicator_code',
        'value_type', 'observation_date', 'source_name', 'confidence'
    ]
    
    VALID_RECORD_TYPES = ['observation', 'event', 'target']
    VALID_PILLARS = ['ACCESS', 'USAGE', 'QUALITY', 'AFFORDABILITY', 'GENDER']
    VALID_VALUE_TYPES = ['percentage', 'absolute', 'categorical', 'ratio', 'currency']
    VALID_CONFIDENCE_LEVELS = ['high', 'medium', 'low']
    VALID_GENDERS = ['all', 'male', 'female']
    VALID_LOCATIONS = ['national', 'urban', 'rural']
    
    # Pillar-specific rules
    PILLAR_RULES = {
        'ACCESS': {
            'valid_indicators': ['ACC_OWNERSHIP', 'MOBILE_MONEY_ACC', 'BANK_BRANCH_DENSITY'],
            'required_value_type': ['percentage', 'ratio'],
            'description': 'Account ownership and access to financial services'
        },
        'USAGE': {
            'valid_indicators': ['USG_P2P_COUNT', 'USG_ATM_COUNT', 'USG_TELEBIRR_VALUE', 'USG_MPESA_USERS'],
            'required_value_type': ['absolute', 'currency', 'percentage'],
            'description': 'Usage patterns and transaction volumes'
        },
        'GENDER': {
            'valid_indicators': ['GENDER_GAP', 'FEMALE_ACC_RATE', 'MALE_ACC_RATE'],
            'required_value_type': ['percentage'],
            'description': 'Gender-disaggregated metrics'
        },
        'AFFORDABILITY': {
            'valid_indicators': ['ACC_COST', 'TRANSACTION_FEE'],
            'required_value_type': ['currency', 'percentage'],
            'description': 'Cost and affordability metrics'
        }
    }
    
    # Event-specific rules
    EVENT_CATEGORIES = [
        'product_launch', 'policy_change', 'regulatory_update', 
        'infrastructure', 'market_entry', 'technology_adoption'
    ]
    
    def __init__(self, verbose: bool = True):
        """
        Initialize validator.
        
        Args:
            verbose: Print detailed validation messages
        """
        self.verbose = verbose
        self.validation_log = []
        
    def validate_schema(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate that dataframe conforms to required schema.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        # Check required columns
        missing_cols = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")
        
        # Check for empty dataframe
        if len(df) == 0:
            errors.append("DataFrame is empty")
            return False, errors
        
        # Validate record_type
        invalid_types = set(df['record_type'].dropna()) - set(self.VALID_RECORD_TYPES)
        if invalid_types:
            errors.append(f"Invalid record_types: {invalid_types}")
        
        # Validate pillars (only for observations)
        obs_df = df[df['record_type'] == 'observation']
        if len(obs_df) > 0:
            invalid_pillars = set(obs_df['pillar'].dropna()) - set(self.VALID_PILLARS)
            if invalid_pillars:
                errors.append(f"Invalid pillars: {invalid_pillars}")
        
        # Validate value_types
        invalid_vtypes = set(df['value_type'].dropna()) - set(self.VALID_VALUE_TYPES)
        if invalid_vtypes:
            errors.append(f"Invalid value_types: {invalid_vtypes}")
        
        # Validate confidence levels
        invalid_conf = set(df['confidence'].dropna()) - set(self.VALID_CONFIDENCE_LEVELS)
        if invalid_conf:
            errors.append(f"Invalid confidence levels: {invalid_conf}")
        
        is_valid = len(errors) == 0
        
        if self.verbose:
            if is_valid:
                print("✓ Schema validation passed")
            else:
                print("✗ Schema validation failed:")
                for error in errors:
                    print(f"  - {error}")
        
        self.validation_log.append({
            'check': 'schema',
            'passed': is_valid,
            'errors': errors
        })
        
        return is_valid, errors
    
    def validate_pillar_rules(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate that observations follow pillar-specific rules.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        obs_df = df[df['record_type'] == 'observation']
        
        for pillar, rules in self.PILLAR_RULES.items():
            pillar_obs = obs_df[obs_df['pillar'] == pillar]
            
            if len(pillar_obs) == 0:
                continue
            
            # Check indicator codes follow pattern
            invalid_indicators = []
            for idx, row in pillar_obs.iterrows():
                indicator_code = row.get('indicator_code', '')
                if pd.notna(indicator_code):
                    # Check if indicator follows expected pattern
                    is_valid_pattern = any(
                        indicator_code.startswith(valid_ind.split('_')[0])
                        for valid_ind in rules.get('valid_indicators', [])
                    )
                    if not is_valid_pattern:
                        invalid_indicators.append(indicator_code)
            
            if invalid_indicators:
                errors.append(
                    f"Pillar {pillar}: Unexpected indicator codes {set(invalid_indicators)}"
                )
            
            # Check value types
            invalid_vtypes = set(pillar_obs['value_type'].dropna()) - set(rules.get('required_value_type', []))
            if invalid_vtypes and rules.get('required_value_type'):
                errors.append(
                    f"Pillar {pillar}: Invalid value types {invalid_vtypes}, "
                    f"expected {rules['required_value_type']}"
                )
        
        is_valid = len(errors) == 0
        
        if self.verbose:
            if is_valid:
                print("✓ Pillar rules validation passed")
            else:
                print("✗ Pillar rules validation failed:")
                for error in errors:
                    print(f"  - {error}")
        
        self.validation_log.append({
            'check': 'pillar_rules',
            'passed': is_valid,
            'errors': errors
        })
        
        return is_valid, errors
    
    def validate_record_types(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate record_type semantics and constraints.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        # Observations must have pillar
        obs_df = df[df['record_type'] == 'observation']
        obs_no_pillar = obs_df[obs_df['pillar'].isna()]
        if len(obs_no_pillar) > 0:
            errors.append(
                f"{len(obs_no_pillar)} observations missing pillar: "
                f"{obs_no_pillar['record_id'].tolist()}"
            )
        
        # Observations must have numeric or categorical value
        obs_no_value = obs_df[
            (obs_df['value_numeric'].isna()) & (obs_df['value_text'].isna())
        ]
        if len(obs_no_value) > 0:
            errors.append(
                f"{len(obs_no_value)} observations missing value: "
                f"{obs_no_value['record_id'].tolist()}"
            )
        
        # Events must have category
        events_df = df[df['record_type'] == 'event']
        if len(events_df) > 0:
            events_no_cat = events_df[events_df['category'].isna()]
            if len(events_no_cat) > 0:
                errors.append(
                    f"{len(events_no_cat)} events missing category: "
                    f"{events_no_cat['record_id'].tolist()}"
                )
            
            # Events should not have pillar
            events_with_pillar = events_df[events_df['pillar'].notna()]
            if len(events_with_pillar) > 0:
                errors.append(
                    f"{len(events_with_pillar)} events incorrectly have pillar: "
                    f"{events_with_pillar['record_id'].tolist()}"
                )
        
        # Targets must have pillar and future date
        targets_df = df[df['record_type'] == 'target']
        if len(targets_df) > 0:
            targets_no_pillar = targets_df[targets_df['pillar'].isna()]
            if len(targets_no_pillar) > 0:
                errors.append(
                    f"{len(targets_no_pillar)} targets missing pillar: "
                    f"{targets_no_pillar['record_id'].tolist()}"
                )
        
        is_valid = len(errors) == 0
        
        if self.verbose:
            if is_valid:
                print("✓ Record type validation passed")
            else:
                print("✗ Record type validation failed:")
                for error in errors:
                    print(f"  - {error}")
        
        self.validation_log.append({
            'check': 'record_types',
            'passed': is_valid,
            'errors': errors
        })
        
        return is_valid, errors
    
    def validate_all(self, df: pd.DataFrame) -> Tuple[bool, Dict]:
        """
        Run all validation checks.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            (all_valid, validation_report)
        """
        print("=" * 80)
        print("DATA VALIDATION REPORT")
        print("=" * 80)
        print(f"Records to validate: {len(df)}")
        print()
        
        # Run all checks
        schema_valid, schema_errors = self.validate_schema(df)
        pillar_valid, pillar_errors = self.validate_pillar_rules(df)
        type_valid, type_errors = self.validate_record_types(df)
        
        all_valid = schema_valid and pillar_valid and type_valid
        
        report = {
            'total_records': len(df),
            'all_valid': all_valid,
            'schema_validation': {
                'passed': schema_valid,
                'errors': schema_errors
            },
            'pillar_validation': {
                'passed': pillar_valid,
                'errors': pillar_errors
            },
            'record_type_validation': {
                'passed': type_valid,
                'errors': type_errors
            },
            'validation_log': self.validation_log
        }
        
        print()
        print("=" * 80)
        if all_valid:
            print("✓ ALL VALIDATIONS PASSED")
        else:
            print("✗ VALIDATION FAILED - See errors above")
        print("=" * 80)
        
        return all_valid, report
    
    def get_enrichment_log_structure(self) -> pd.DataFrame:
        """
        Return example enrichment log structure.
        
        Returns:
            DataFrame showing enrichment log columns and example rows
        """
        enrichment_log = pd.DataFrame({
            'timestamp': ['2025-01-20 10:15:00', '2025-01-20 10:16:30'],
            'record_id': ['REC_0044', 'EVT_0011'],
            'record_type': ['observation', 'event'],
            'action': ['added', 'added'],
            'pillar': ['USAGE', None],
            'indicator': ['M-Pesa Transaction Volume', 'CBE Digital Banking Launch'],
            'indicator_code': ['USG_MPESA_VALUE', 'EVT_CBE_DIGITAL'],
            'value': ['250000000', 'Launched'],
            'observation_date': ['2024-12-31', '2024-11-15'],
            'source': ['M-Pesa Ethiopia Report', 'CBE Press Release'],
            'confidence': ['high', 'high'],
            'enriched_by': ['analyst_1', 'analyst_1'],
            'validation_status': ['passed', 'passed'],
            'notes': [
                'Q4 2024 transaction volume in ETB',
                'Digital banking platform rollout nationwide'
            ]
        })
        
        return enrichment_log
    
    def print_enrichment_guide(self):
        """Print enrichment structure and validation rules."""
        print("=" * 80)
        print("DATA ENRICHMENT LOG STRUCTURE")
        print("=" * 80)
        print("\nRequired Columns for New Records:")
        for col in self.REQUIRED_COLUMNS:
            print(f"  • {col}")
        
        print("\n" + "=" * 80)
        print("EXAMPLE ENRICHMENT LOG")
        print("=" * 80)
        log_example = self.get_enrichment_log_structure()
        print(log_example.to_string(index=False))
        
        print("\n" + "=" * 80)
        print("PILLAR RULES")
        print("=" * 80)
        for pillar, rules in self.PILLAR_RULES.items():
            print(f"\n{pillar}: {rules['description']}")
            print(f"  Valid value types: {rules['required_value_type']}")
            print(f"  Example indicators: {rules['valid_indicators'][:3]}")
        
        print("\n" + "=" * 80)
        print("RECORD TYPE SEMANTICS")
        print("=" * 80)
        print("\nOBSERVATION:")
        print("  • MUST have: pillar, value (numeric or text), indicator_code")
        print("  • MUST NOT have: category")
        print("  • Represents actual data points/measurements")
        
        print("\nEVENT:")
        print("  • MUST have: category, observation_date")
        print("  • MUST NOT have: pillar, value_numeric")
        print("  • Represents discrete occurrences (launches, policy changes)")
        
        print("\nTARGET:")
        print("  • MUST have: pillar, value, future observation_date")
        print("  • Represents policy goals or forecasts")
        print("=" * 80)
