# Enriched Data Directory

This directory contains enriched datasets generated during analysis tasks.

## Contents

### Enrichment Logs

- **`enrichment_log.csv`** - Audit trail of all new records added to the dataset
  - Columns: timestamp, record_type, pillar, indicator_code, year, value_numeric, source, notes
  - Created by: Task 1 data enrichment process
  - Purpose: Track data additions for reproducibility

### Processed Datasets

- **`observations_enriched.csv`** - Observations with additional data points from Task 1
- **`events_enriched.csv`** - Events data with enriched context
- **`complete_dataset.csv`** - Full unified dataset including observations, events, and targets

### Analysis Outputs

- **`time_series_data.csv`** - Time series prepared for forecasting (Task 2-4)
- **`pillar_summary.csv`** - Summary statistics by pillar
- **`event_impact_analysis.csv`** - Event correlation results (Task 3)

## Data Workflow

```
raw/ (original data)
  ↓
Task 1: Exploration & Enrichment
  ↓
enriched/ (validated additions)
  ↓
Task 2: EDA & Feature Engineering
  ↓
processed/ (analysis-ready data)
  ↓
Task 3-5: Modeling & Forecasting
```

## File Naming Convention

- `*_enriched.csv` - Data with validated additions
- `*_processed.csv` - Analysis-ready transformed data
- `*_log.csv` - Audit trails and metadata

## Best Practices

1. **Never modify raw data** - Keep originals in `data/raw/`
2. **Document changes** - Use enrichment log for all additions
3. **Version enriched data** - Include timestamp in enrichment log
4. **Validate before saving** - Use DataValidator before writing enriched data
