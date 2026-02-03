# Error Handling Quick Reference

## Common Error Scenarios and Solutions

### 1. DataLoadError

#### File Not Found

```python
# Error:
DataLoadError: "File not found: data/raw/missing_file.xlsx"

# Solution:
- Check file path is correct
- Ensure file exists in specified location
- Use absolute path if relative path fails
```

#### Missing Required Columns

```python
# Error:
DataLoadError: "Missing columns in data: {'year', 'value_numeric'}"

# Solution:
- Verify Excel file has correct structure
- Check column names match exactly (case-sensitive)
- Review data/raw/README.md for expected schema
```

#### Empty Dataset

```python
# Error:
DataLoadError: "Data sheet is empty"

# Solution:
- Check Excel file is not corrupted
- Verify data exists in the expected sheet
- Ensure correct sheet name is used
```

### 2. AnalysisError

#### Empty Observations

```python
# Error:
AnalysisError: "Observations dataframe cannot be empty"

# Solution:
obs = loader.get_observations()
if len(obs) == 0:
    print("No observations loaded - check data source")
else:
    analyzer = FinancialInclusionAnalyzer(obs)
```

#### Insufficient Data for Growth Analysis

```python
# Warning:
WARNING: Insufficient data for INDICATOR_CODE (need >= 2 points)

# Solution:
- Growth rate requires at least 2 data points
- Check if indicator has multiple years of data
- Use different indicator with more historical data
```

#### Missing Pillar Column

```python
# Error:
AnalysisError: "'pillar' column not found in observations"

# Solution:
- Ensure observations DataFrame has 'pillar' column
- Check data loader correctly parsed pillars
- Verify Excel file has pillar information
```

### 3. VisualizationError

#### Empty Plot Data

```python
# Error:
VisualizationError: "Empty data for time series plot"

# Solution:
data = analyzer.calculate_growth_rate(indicator)
if len(data) > 0:
    fig = viz.plot_time_series(data)
else:
    print("No data available for plotting")
```

#### Missing Required Columns

```python
# Error:
VisualizationError: "Missing columns for growth analysis: {'growth_pp'}"

# Solution:
- Ensure data has all required columns
- Use correct analyzer method to prepare data
- Check column names match visualization expectations
```

#### No Valid Data After NA Removal

```python
# Warning:
WARNING: No valid time series data after removing NA values

# Result: Fallback plot with informative message

# Prevention:
data_clean = data.dropna(subset=['year', 'value_numeric'])
if len(data_clean) > 0:
    fig = viz.plot_time_series(data_clean)
```

## Logging Messages Guide

### INFO Messages (Success)

```
INFO: Initialized analyzer with 30 observations
INFO: Successfully loaded 30 observations and 10 events
INFO: Found 3 trend changes for TELEBIRR_USAGE
```

**Action**: None required - operations successful

### WARNING Messages (Non-Critical Issues)

```
WARNING: 5 invalid dates converted to NaT
WARNING: No gender data found
WARNING: Reference codes not found, proceeding without them
```

**Action**: Review data quality, but processing continues

### ERROR Messages (Critical Failures)

```
ERROR: Time series validation failed: Missing columns
ERROR: Pillar comparison validation failed
```

**Action**: Fix underlying issue before proceeding

## Best Practices

### 1. Always Validate Before Processing

```python
# Good
from src.validators import validate_dataframe

validate_dataframe(df, required_cols=['year', 'value'], min_rows=1)
result = process_data(df)

# Bad
result = process_data(df)  # May crash if df invalid
```

### 2. Handle Expected Failures

```python
# Good
from src.analysis import AnalysisError

try:
    analyzer = FinancialInclusionAnalyzer(obs)
    growth = analyzer.calculate_growth_rate(indicator)
except AnalysisError as e:
    logger.error(f"Analysis failed: {e}")
    growth = pd.DataFrame()  # Use empty DataFrame as fallback

# Bad
analyzer = FinancialInclusionAnalyzer(obs)  # May crash
growth = analyzer.calculate_growth_rate(indicator)
```

### 3. Check Return Values

```python
# Good
data = loader.get_observations()
if len(data) == 0:
    print("Warning: No observations loaded")
    return

growth = analyzer.calculate_growth_rate(indicator)
if growth.empty:
    print(f"No growth data for {indicator}")
    return

# Bad
data = loader.get_observations()  # Assume success
growth = analyzer.calculate_growth_rate(indicator)  # Assume success
```

### 4. Use Safe Conversions

```python
# Good
from src.validators import safe_numeric_conversion, safe_datetime_conversion

df['value'] = safe_numeric_conversion(df['value_str'], default=0)
df['date'] = safe_datetime_conversion(df['date_str'], errors='coerce')

# Bad
df['value'] = df['value_str'].astype(float)  # May crash
df['date'] = pd.to_datetime(df['date_str'])  # May crash
```

## Debugging Tips

### Enable Detailed Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Show all messages
    format='%(levelname)s: %(name)s: %(message)s'
)
```

### Inspect Data Quality

```python
# Check for missing values
print(df.isna().sum())

# Check data types
print(df.dtypes)

# Check for empty DataFrames
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")

# Check required columns
required = ['year', 'value_numeric', 'indicator_code']
missing = set(required) - set(df.columns)
if missing:
    print(f"Missing columns: {missing}")
```

### Test Individual Components

```python
# Test data loading
loader = FinancialDataLoader('data.xlsx')
data, impacts = loader.load_all_data()
print(f"Loaded {len(data['observations'])} observations")

# Test analysis
analyzer = FinancialInclusionAnalyzer(data['observations'])
pillars = analyzer.compare_pillars()
print(pillars)

# Test visualization
viz = FinancialInclusionVisualizer()
fig = viz.plot_pillar_comparison(pillars)
```

## Recovery Strategies

### Missing Data Files

```python
import os

data_file = 'data/raw/financial_inclusion_data.xlsx'
if not os.path.exists(data_file):
    print(f"ERROR: {data_file} not found")
    print("Please ensure data file is in correct location")
    print("Expected location: data/raw/")
else:
    loader = FinancialDataLoader(data_file)
```

### Incomplete Data

```python
# Graceful degradation
obs = loader.get_observations()
events = loader.get_events()

if len(obs) == 0:
    print("No observations - cannot proceed")
elif len(events) == 0:
    print("No events - proceeding with observations only")
    analyzer = FinancialInclusionAnalyzer(obs, events=None)
else:
    analyzer = FinancialInclusionAnalyzer(obs, events)
```

### Failed Visualizations

```python
# Try plotting, fall back to data display
try:
    fig = viz.plot_time_series(growth)
    if fig is not None:
        fig.savefig('output.png')
    else:
        print("Visualization returned None - showing data instead:")
        print(growth)
except VisualizationError as e:
    print(f"Visualization failed: {e}")
    print("Data table:")
    print(growth)
```

## Contact & Support

If you encounter errors not covered in this guide:

1. Check the log messages for details
2. Verify data file structure matches expected schema
3. Review [ROBUSTNESS_IMPROVEMENTS.md](ROBUSTNESS_IMPROVEMENTS.md) for implementation details
4. Check [VALIDATION_QUICK_REFERENCE.md](VALIDATION_QUICK_REFERENCE.md) for validation rules
5. Create an issue with error message and context
