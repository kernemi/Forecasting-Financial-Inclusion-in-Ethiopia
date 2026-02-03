# Data Enrichment & Validation Guide

## Overview

This guide documents the **enrichment log structure** and **validation rules** for the Financial Inclusion dataset. All new records must pass validation checks before being added to ensure data integrity and reproducibility.

---

## Enrichment Log Structure

### Required Columns

When documenting new records in the enrichment log, include these columns:

| Column              | Description                | Example                          |
| ------------------- | -------------------------- | -------------------------------- |
| `timestamp`         | When record was added      | `2025-01-20 10:15:00`            |
| `record_id`         | Unique identifier          | `REC_0044`, `EVT_0011`           |
| `record_type`       | Type of record             | `observation`, `event`, `target` |
| `action`            | Operation performed        | `added`, `updated`, `validated`  |
| `pillar`            | Pillar category (obs only) | `ACCESS`, `USAGE`, `GENDER`      |
| `indicator`         | Human-readable name        | `Account Ownership Rate`         |
| `indicator_code`    | Standardized code          | `ACC_OWNERSHIP`                  |
| `value`             | Recorded value             | `35.0`, `Launched`               |
| `observation_date`  | Date of observation/event  | `2024-12-31`                     |
| `source`            | Data source                | `Global Findex 2024`             |
| `confidence`        | Quality level              | `high`, `medium`, `low`          |
| `enriched_by`       | Who added the record       | `analyst_1`                      |
| `validation_status` | Passed validation          | `passed`, `failed`               |
| `notes`             | Additional context         | `Q4 2024 data`                   |

### Example Enrichment Log

```
timestamp            record_id  record_type  action  pillar  indicator                    value        confidence  validation_status
2025-01-20 10:15:00  REC_0044   observation  added   USAGE   M-Pesa Transaction Volume    250000000    high        passed
2025-01-20 10:16:30  EVT_0011   event        added   None    CBE Digital Banking Launch   Launched     high        passed
```

---

## Schema Validation Rules

### 1. Required Columns

Every record MUST include:

- `record_id` - Unique identifier
- `record_type` - Must be `observation`, `event`, or `target`
- `pillar` - Required for observations and targets
- `indicator` - Human-readable name
- `indicator_code` - Standardized code
- `value_type` - `percentage`, `absolute`, `categorical`, `ratio`, `currency`
- `observation_date` - When data was observed
- `source_name` - Where data came from
- `confidence` - `high`, `medium`, or `low`

### 2. Valid Values

**Record Types:**

- `observation` - Actual data point/measurement
- `event` - Discrete occurrence (launch, policy change)
- `target` - Future goal or forecast

**Pillars (observations only):**

- `ACCESS` - Account ownership, branch density
- `USAGE` - Transaction volumes, activity rates
- `QUALITY` - Service quality metrics
- `AFFORDABILITY` - Costs and fees
- `GENDER` - Gender-disaggregated metrics

**Value Types:**

- `percentage` - 0-100% (e.g., 35.2%)
- `absolute` - Raw numbers (e.g., 1,000,000)
- `categorical` - Text values (e.g., "Launched")
- `ratio` - Per capita metrics
- `currency` - Monetary values (ETB, USD)

**Confidence Levels:**

- `high` - Authoritative source, verified data
- `medium` - Secondary source, reasonable estimate
- `low` - Unverified or uncertain

---

## Pillar-Specific Rules

### ACCESS Pillar

```
Description: Account ownership and access to financial services
Valid Indicators: ACC_OWNERSHIP, MOBILE_MONEY_ACC, BANK_BRANCH_DENSITY
Required Value Types: percentage, ratio
Example: 35.2% account ownership in 2024
```

### USAGE Pillar

```
Description: Usage patterns and transaction volumes
Valid Indicators: USG_P2P_COUNT, USG_ATM_COUNT, USG_TELEBIRR_VALUE, USG_MPESA_USERS
Required Value Types: absolute, currency, percentage
Example: 2.38 trillion ETB Telebirr transaction value
```

### GENDER Pillar

```
Description: Gender-disaggregated financial inclusion metrics
Valid Indicators: GENDER_GAP, FEMALE_ACC_RATE, MALE_ACC_RATE
Required Value Types: percentage
Example: 12pp gender gap in account ownership
```

### AFFORDABILITY Pillar

```
Description: Cost and affordability of financial services
Valid Indicators: ACC_COST, TRANSACTION_FEE
Required Value Types: currency, percentage
Example: 50 ETB average account maintenance fee
```

---

## Record Type Semantics

### OBSERVATION Records

**MUST HAVE:**

- `pillar` - One of: ACCESS, USAGE, QUALITY, AFFORDABILITY, GENDER
- `value_numeric` OR `value_text` - The actual measurement
- `indicator_code` - Following pillar naming convention
- `gender` - `all`, `male`, or `female`
- `location` - `national`, `urban`, or `rural`

**MUST NOT HAVE:**

- `category` - Only events have categories

**Example:**

```python
{
    'record_id': 'REC_0044',
    'record_type': 'observation',
    'pillar': 'ACCESS',
    'indicator': 'Account Ownership Rate',
    'indicator_code': 'ACC_OWNERSHIP',
    'value_numeric': 35.2,
    'value_type': 'percentage',
    'observation_date': '2024-12-31',
    'gender': 'all',
    'location': 'national',
    'source_name': 'Global Findex 2024',
    'confidence': 'high'
}
```

### EVENT Records

**MUST HAVE:**

- `category` - Type of event (product_launch, policy_change, regulatory_update, infrastructure, market_entry, technology_adoption)
- `observation_date` - When event occurred (use this field, not period_start)
- `value_text` - Description of event

**MUST NOT HAVE:**

- `pillar` - Events are cross-cutting, not assigned to pillars
- `value_numeric` - Events don't have numeric values

**Example:**

```python
{
    'record_id': 'EVT_0011',
    'record_type': 'event',
    'category': 'product_launch',
    'indicator': 'CBE Digital Banking Launch',
    'indicator_code': 'EVT_CBE_DIGITAL',
    'value_text': 'Launched',
    'value_type': 'categorical',
    'observation_date': '2024-11-15',
    'source_name': 'CBE Press Release',
    'confidence': 'high'
}
```

### TARGET Records

**MUST HAVE:**

- `pillar` - The pillar this target relates to
- `value_numeric` - Target value
- `observation_date` - **FUTURE DATE** (when target should be achieved)

**Example:**

```python
{
    'record_id': 'TGT_0004',
    'record_type': 'target',
    'pillar': 'ACCESS',
    'indicator': 'Universal Account Ownership',
    'indicator_code': 'TGT_ACC_2030',
    'value_numeric': 80.0,
    'value_type': 'percentage',
    'observation_date': '2030-12-31',
    'source_name': 'National Financial Inclusion Strategy',
    'confidence': 'medium'
}
```

---

## Validation Workflow

### Step 1: Import Validator

```python
import sys
sys.path.append('../src')
from analysis import DataValidator

# Initialize validator
validator = DataValidator(verbose=True)
```

### Step 2: Create New Records

```python
import pandas as pd

new_records = pd.DataFrame([
    {
        'record_id': 'REC_0044',
        'record_type': 'observation',
        'pillar': 'USAGE',
        'indicator': 'M-Pesa Transaction Volume',
        'indicator_code': 'USG_MPESA_VALUE',
        'value_numeric': 250000000,
        'value_type': 'currency',
        'unit': 'ETB',
        'observation_date': '2024-12-31',
        'gender': 'all',
        'location': 'national',
        'source_name': 'M-Pesa Ethiopia Q4 Report',
        'source_type': 'operator',
        'confidence': 'high'
    }
])
```

### Step 3: Validate

```python
# Run validation
is_valid, report = validator.validate_all(new_records)

# Check results
if is_valid:
    print("✓ Validation passed - safe to add records")
else:
    print("✗ Validation failed - review errors:")
    for check, result in report.items():
        if not result.get('passed', True):
            print(f"  {check}: {result.get('errors', [])}")
```

### Step 4: Document in Enrichment Log

```python
# Add to enrichment log
enrichment_entry = {
    'timestamp': pd.Timestamp.now(),
    'record_id': 'REC_0044',
    'record_type': 'observation',
    'action': 'added',
    'pillar': 'USAGE',
    'indicator': 'M-Pesa Transaction Volume',
    'value': '250000000',
    'source': 'M-Pesa Ethiopia Q4 Report',
    'confidence': 'high',
    'enriched_by': 'analyst_1',
    'validation_status': 'passed',
    'notes': 'Q4 2024 transaction volume in ETB'
}

# Append to enrichment log CSV
enrichment_log = pd.DataFrame([enrichment_entry])
enrichment_log.to_csv('../data/processed/enrichment_log.csv',
                      mode='a', header=False, index=False)
```

---

## Common Validation Errors

### ❌ Missing Required Column

```
Error: Missing required columns: {'pillar'}
Fix: Add pillar field to observation records
```

### ❌ Invalid Record Type

```
Error: Invalid record_types: {'data_point'}
Fix: Use 'observation', 'event', or 'target' only
```

### ❌ Events with Pillar

```
Error: 2 events incorrectly have pillar: ['EVT_0011', 'EVT_0012']
Fix: Remove pillar field from event records (events are cross-cutting)
```

### ❌ Observation Without Value

```
Error: 3 observations missing value: ['REC_0044', 'REC_0045', 'REC_0046']
Fix: Add value_numeric or value_text to observation records
```

### ❌ Wrong Value Type for Pillar

```
Error: Pillar ACCESS: Invalid value types {'currency'}, expected ['percentage', 'ratio']
Fix: Use percentage or ratio for ACCESS pillar indicators
```

---

## Best Practices

### ✅ DO:

- Run validation BEFORE committing new records
- Document all enrichment in the log
- Use standardized indicator codes (pillar prefix + descriptor)
- Assign high confidence only to authoritative sources
- Include source URLs when available
- Add enrichment notes explaining context

### ❌ DON'T:

- Skip validation checks
- Mix record types (don't add pillar to events)
- Use custom/non-standard value types
- Add future-dated observations (use targets instead)
- Assign high confidence to estimates
- Leave source_name blank

---

## Validation Functions Reference

### `validate_schema(df)`

Checks:

- Required columns present
- Valid record types
- Valid pillars
- Valid value types
- Valid confidence levels

### `validate_pillar_rules(df)`

Checks:

- Indicator codes match pillar patterns
- Value types appropriate for pillar
- Pillar-specific constraints

### `validate_record_types(df)`

Checks:

- Observations have pillar and value
- Events have category and observation_date
- Events don't have pillar
- Targets have future dates

### `validate_all(df)`

Runs all three checks and returns comprehensive report.

---

## Output Files

### Enrichment Log Location

```
data/processed/enrichment_log.csv
```

### Validation Report Structure

```python
{
    'total_records': 43,
    'all_valid': True,
    'schema_validation': {
        'passed': True,
        'errors': []
    },
    'pillar_validation': {
        'passed': True,
        'errors': []
    },
    'record_type_validation': {
        'passed': True,
        'errors': []
    }
}
```

---

## Questions?

For issues or clarifications:

1. Review this guide
2. Check `src/analysis.py` DataValidator class
3. Run `validator.print_enrichment_guide()` in Python
4. See examples in `notebooks/task1_data_exploration.ipynb`

---

**Last Updated:** 2025-01-28  
**Version:** 1.0  
**Author:** Financial Inclusion Forecasting Team
