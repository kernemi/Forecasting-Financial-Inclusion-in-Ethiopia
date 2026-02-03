# Processed Data Directory

This directory contains cleaned and processed datasets ready for analysis and modeling.

## Contents

### Task 3: Time Series Forecasting

**`account_ownership_timeseries.csv`**

- Account ownership rate time series (2014-2024)
- Columns: `year`, `account_ownership`
- 4 data points extracted from ACC_OWNERSHIP indicator
- Filtered for percentage values only
- Source: ethiopia_fi_unified_data.xlsx

**`digital_adoption_timeseries.csv`**

- Digital payment adoption time series (2024)
- Columns: `year`, `digital_adoption`
- 1 data point (insufficient for time series forecasting)
- Filtered for percentage values from USAGE pillar
- Source: ethiopia_fi_unified_data.xlsx

**`train_test_split.json`**

- Train/test split metadata for model validation
- Contains: train_years, train_values, test_years, test_values, train_size, test_size
- Split: 50% training (2014, 2017) / 50% testing (2021, 2024)
- Used for ARIMA and ETS model evaluation

## Data Processing Pipeline

### Task 3: Account Ownership Time Series

1. **Raw Data**: `data/raw/ethiopia_fi_unified_data.xlsx`
2. **Filtering**:
   - Record type: `observation` only
   - Pillar: `ACCESS`
   - Indicator code: `ACC_OWNERSHIP`
   - Value type: `percentage` (exclude absolute counts like Fayda enrollment)
3. **Cleaning**:
   - Convert `fiscal_year` to numeric (handle mixed types: 2014, "FY2022/23")
   - Drop NA values in fiscal_year and value_numeric
   - Aggregate multiple values per year using mean
4. **Output**: Clean time series with 4 data points ready for ARIMA/ETS modeling

### Data Quality Notes

- **Irregular intervals**: Data available for 2014, 2017, 2021, 2024 (not annual)
- **Limited points**: Only 4 observations constrains model complexity
- **Digital adoption**: Only 1 data point (2024: 66%) - excluded from forecasting

## Usage

```python
import pandas as pd
import json

# Load processed time series
ts_ownership = pd.read_csv('data/processed/account_ownership_timeseries.csv')
ts_digital = pd.read_csv('data/processed/digital_adoption_timeseries.csv')

# Load train/test split metadata
with open('data/processed/train_test_split.json', 'r') as f:
    split_data = json.load(f)

print(f"Training years: {split_data['train_years']}")
print(f"Testing years: {split_data['test_years']}")

# Ready for modeling
from statsmodels.tsa.holtwinters import ExponentialSmoothing
model = ExponentialSmoothing(
    ts_ownership['account_ownership'],
    trend='add',
    seasonal=None
)
fitted = model.fit()
```

## File Formats

### CSV Files

- Encoding: UTF-8
- Delimiter: Comma (,)
- Header: First row contains column names
- Missing values: Empty cells (no placeholders)

### JSON Files

- Encoding: UTF-8
- Indentation: 2 spaces
- Arrays and objects properly formatted

## Data Dictionary

See `docs/DATA_DICTIONARY.md` for complete field descriptions.
