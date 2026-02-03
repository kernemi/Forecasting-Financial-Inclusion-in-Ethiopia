# Enrichment Log Structure

## Overview

All new records added to the Ethiopia Financial Inclusion dataset must be documented in the enrichment log to maintain reproducibility and auditability.

---

## Columns

| Column              | Type     | Required | Description               | Example                          |
| ------------------- | -------- | -------- | ------------------------- | -------------------------------- |
| `timestamp`         | datetime | ✅       | When record was added     | `2025-01-20 10:15:00`            |
| `record_id`         | string   | ✅       | Unique identifier         | `REC_0044`, `EVT_0011`           |
| `record_type`       | string   | ✅       | Type of record            | `observation`, `event`, `target` |
| `action`            | string   | ✅       | Operation performed       | `added`, `updated`, `validated`  |
| `pillar`            | string   | ⚠️       | Pillar (obs/target only)  | `ACCESS`, `USAGE`, `GENDER`      |
| `indicator`         | string   | ✅       | Human-readable name       | `Account Ownership Rate`         |
| `indicator_code`    | string   | ✅       | Standardized code         | `ACC_OWNERSHIP`                  |
| `value`             | string   | ✅       | Recorded value            | `35.0`, `Launched`               |
| `observation_date`  | date     | ✅       | Date of observation/event | `2024-12-31`                     |
| `source`            | string   | ✅       | Data source               | `Global Findex 2024`             |
| `confidence`        | string   | ✅       | Quality level             | `high`, `medium`, `low`          |
| `enriched_by`       | string   | ✅       | Who added record          | `analyst_1`                      |
| `validation_status` | string   | ✅       | Passed validation         | `passed`, `failed`               |
| `notes`             | string   | ⚠️       | Additional context        | `Q4 2024 data`                   |

**Legend:** ✅ Required | ⚠️ Optional (but recommended)

---

## Example Rows

### Observation Record

```
timestamp: 2025-01-20 10:15:00
record_id: REC_0044
record_type: observation
action: added
pillar: USAGE
indicator: M-Pesa Transaction Volume
indicator_code: USG_MPESA_VALUE
value: 250000000
observation_date: 2024-12-31
source: M-Pesa Ethiopia Q4 Report
confidence: high
enriched_by: analyst_1
validation_status: passed
notes: Q4 2024 transaction volume in ETB
```

### Event Record

```
timestamp: 2025-01-20 10:16:30
record_id: EVT_0011
record_type: event
action: added
pillar: (empty - events are cross-cutting)
indicator: CBE Digital Banking Launch
indicator_code: EVT_CBE_DIGITAL
value: Launched
observation_date: 2024-11-15
source: CBE Press Release
confidence: high
enriched_by: analyst_1
validation_status: passed
notes: Digital banking platform rollout nationwide
```

---

## Table Format Example

| timestamp           | record_id | record_type | action | pillar | indicator                  | value     | confidence | validation_status |
| ------------------- | --------- | ----------- | ------ | ------ | -------------------------- | --------- | ---------- | ----------------- |
| 2025-01-20 10:15:00 | REC_0044  | observation | added  | USAGE  | M-Pesa Transaction Volume  | 250000000 | high       | passed            |
| 2025-01-20 10:16:30 | EVT_0011  | event       | added  | -      | CBE Digital Banking Launch | Launched  | high       | passed            |
| 2025-01-20 10:17:45 | REC_0045  | observation | added  | ACCESS | Rural Account Ownership    | 28.5      | medium     | passed            |

---

## Usage Workflow

1. **Add Record to Main Dataset**

   ```python
   new_record = {
       'record_id': 'REC_0044',
       'record_type': 'observation',
       'pillar': 'USAGE',
       # ... all required fields
   }
   ```

2. **Validate Record**

   ```python
   from src.analysis import DataValidator
   validator = DataValidator()
   is_valid, report = validator.validate_all(new_df)
   ```

3. **Log Enrichment**

   ```python
   enrichment_entry = {
       'timestamp': pd.Timestamp.now(),
       'record_id': 'REC_0044',
       'record_type': 'observation',
       'action': 'added',
       'validation_status': 'passed' if is_valid else 'failed',
       # ... other fields
   }

   log_df = pd.DataFrame([enrichment_entry])
   log_df.to_csv('data/processed/enrichment_log.csv',
                 mode='a', header=False, index=False)
   ```

4. **Commit Changes**
   ```bash
   git add data/raw/ethiopia_fi_unified_data.xlsx
   git add data/processed/enrichment_log.csv
   git commit -m "Added REC_0044: M-Pesa Q4 2024 transaction data"
   ```

---

## File Location

```
data/processed/enrichment_log.csv
```

**Format:** CSV with header row  
**Encoding:** UTF-8  
**Version Control:** Yes (commit with data updates)

---

## See Also

- **Complete Guide:** `docs/ENRICHMENT_VALIDATION_GUIDE.md`
- **Quick Reference:** `docs/VALIDATION_QUICK_REFERENCE.md`
- **Code Implementation:** `src/analysis.py` → `DataValidator` class
- **Example Usage:** `notebooks/task1_data_exploration.ipynb` → Section 8

---

**Last Updated:** 2025-01-28  
**Maintained By:** Financial Inclusion Forecasting Team
