# Data Validation Quick Reference Card

## 🚀 Quick Start

```python
from analysis import DataValidator

validator = DataValidator()
is_valid, report = validator.validate_all(your_dataframe)
```

---

## ✅ Required Columns

Every record MUST have:

- `record_id`, `record_type`, `indicator`, `indicator_code`
- `value_type`, `observation_date`, `source_name`, `confidence`

Observations MUST also have:

- `pillar`

---

## 📋 Valid Values

| Field         | Valid Options                                                |
| ------------- | ------------------------------------------------------------ |
| `record_type` | `observation`, `event`, `target`                             |
| `pillar`      | `ACCESS`, `USAGE`, `QUALITY`, `AFFORDABILITY`, `GENDER`      |
| `value_type`  | `percentage`, `absolute`, `categorical`, `ratio`, `currency` |
| `confidence`  | `high`, `medium`, `low`                                      |
| `gender`      | `all`, `male`, `female`                                      |
| `location`    | `national`, `urban`, `rural`                                 |

---

## 🏛️ Pillar Rules

### ACCESS

- **Indicators:** ACC_OWNERSHIP, MOBILE_MONEY_ACC, BANK_BRANCH_DENSITY
- **Value Types:** percentage, ratio
- **Example:** 35.2% account ownership

### USAGE

- **Indicators:** USG_P2P_COUNT, USG_TELEBIRR_VALUE, USG_MPESA_USERS
- **Value Types:** absolute, currency, percentage
- **Example:** 2.38T ETB transaction value

### GENDER

- **Indicators:** GENDER_GAP, FEMALE_ACC_RATE, MALE_ACC_RATE
- **Value Types:** percentage
- **Example:** 12pp gender gap

---

## 📝 Record Type Rules

### OBSERVATION

✅ MUST: pillar, value (numeric or text), gender, location  
❌ MUST NOT: category

### EVENT

✅ MUST: category, observation_date, value_text  
❌ MUST NOT: pillar, value_numeric

### TARGET

✅ MUST: pillar, value_numeric, future observation_date  
❌ MUST NOT: category

---

## 🔍 Common Errors

| Error            | Fix                                      |
| ---------------- | ---------------------------------------- |
| Missing pillar   | Add pillar to observations               |
| Event has pillar | Remove pillar (events are cross-cutting) |
| Missing value    | Add value_numeric or value_text          |
| Wrong value type | Check pillar rules above                 |

---

## 📊 Enrichment Log Template

```python
{
    'timestamp': '2025-01-20 10:15:00',
    'record_id': 'REC_0044',
    'record_type': 'observation',
    'action': 'added',
    'pillar': 'USAGE',
    'indicator': 'M-Pesa Transaction Volume',
    'value': '250000000',
    'source': 'M-Pesa Q4 Report',
    'confidence': 'high',
    'enriched_by': 'analyst_1',
    'validation_status': 'passed',
    'notes': 'Q4 2024 data'
}
```

---

## 🎯 Best Practices

**DO:**

- ✅ Validate before committing
- ✅ Use standardized indicator codes
- ✅ Document in enrichment log
- ✅ Include source URLs

**DON'T:**

- ❌ Skip validation
- ❌ Mix record types
- ❌ Use high confidence for estimates
- ❌ Leave source blank

---

**Full Guide:** `docs/ENRICHMENT_VALIDATION_GUIDE.md`  
**Code:** `src/analysis.py` → `DataValidator` class  
**Example:** `notebooks/task1_data_exploration.ipynb` → Section 8
