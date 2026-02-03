# Task 4: Machine Learning Models - Ethiopia Financial Inclusion

**Date:** February 3, 2026  
**Project:** Forecasting Financial Inclusion in Ethiopia  
**Task Type:** Supervised Machine Learning - Classification & Regression

---

## Executive Summary

This report presents the development and evaluation of machine learning models to predict financial inclusion outcomes in Ethiopia. Using historical data on account ownership, digital payments, and various financial inclusion indicators, we trained and compared multiple supervised learning models to identify key drivers of financial inclusion.

### Key Findings

1. **Best Regression Model:** Random Forest Regressor (MAE: 24.50, RMSE: 29.14)
2. **Data Limitations:** Only 4 data points available (2014, 2017, 2021, 2024), limiting model complexity
3. **Feature Engineering:** Created 10 features from observations including account ownership, mobile money adoption, gender gaps, and usage metrics
4. **Classification:** Skipped due to single class in training data (insufficient class diversity)
5. **Model Performance:** All models showed similar performance due to limited training data

---

## 1. Methodology

### 1.1 Data Preparation

**Source Data:**

- Total records: 43 (30 observations, 10 events, 3 targets)
- Pillars: ACCESS (16), USAGE (11), GENDER (5), AFFORDABILITY (1)
- Time range: 2014-2025 (fiscal years)

**Feature Engineering:**

- Pivoted observations to create wide format (11 indicators)
- Created lag features (previous year values)
- Created change features (year-over-year differences)
- Merged event counts by pillar
- Final feature set: 10 features after removing target leakage

**Features Used:**

1. `ACC_FAYDA` - Fayda card accounts
2. `ACC_MM_ACCOUNT` - Mobile money accounts (%)
3. `ACC_MOBILE_PEN` - Mobile penetration (%)
4. `AFF_DATA_INCOME` - Data cost as % of income
5. `GEN_GAP_ACC` - Gender gap in account ownership
6. `GEN_GAP_MOBILE` - Gender gap in mobile ownership
7. `GEN_MM_SHARE` - Share of women using mobile money
8. `USG_ACTIVE_RATE` - Active account usage rate (%)
9. `USG_MPESA_ACTIVE` - Active M-PESA users
10. `USG_MPESA_USERS` - Total M-PESA users

### 1.2 Target Variables

**Classification Target:**

- `high_ownership`: Binary (0/1) based on median threshold (35%)
- Class distribution: 3 low, 2 high
- **Status:** Skipped due to single class in training split

**Regression Target:**

- `target_ownership_next_year`: Predict next year's account ownership rate
- Available for 4 years (2014→2015, 2017→2018, 2021→2022, 2024→2025)

### 1.3 Train/Test Split

- **Temporal split:** 70-30 (earlier years for training)
- **Train size:** 2 samples (2014, 2017)
- **Test size:** 2 samples (2021, 2024)
- **Scaling:** StandardScaler applied to features

---

## 2. Models Trained

### 2.1 Ridge Regression (Baseline)

**Configuration:**

- Alpha: 1.0 (L2 regularization)
- Random state: 42

**Performance:**

- **MAE:** 24.50
- **RMSE:** 29.26
- **R²:** -0.43 (negative indicates worse than mean baseline)

**Interpretation:**

- Linear model with regularization
- Poor fit due to limited data
- Negative R² suggests model cannot capture underlying pattern

### 2.2 Random Forest Regressor

**Configuration:**

- n_estimators: 100 trees
- max_depth: 3 (limited to prevent overfitting)
- Random state: 42

**Performance:**

- **MAE:** 24.50
- **RMSE:** 29.14 ⭐ (Best)
- **R²:** -0.41

**Interpretation:**

- Ensemble method using bagging
- Slightly better than Ridge on RMSE
- All feature importances are 0 (model defaulting to mean prediction)

### 2.3 Gradient Boosting Regressor

**Configuration:**

- n_estimators: 100 trees
- max_depth: 2
- Random state: 42

**Performance:**

- **MAE:** 24.50
- **RMSE:** 29.26
- **R²:** -0.43

**Interpretation:**

- Sequential boosting ensemble
- Identical performance to Ridge
- Limited data prevents effective boosting

---

## 3. Model Comparison

### 3.1 Performance Summary

| Model             | MAE       | RMSE         | R²        | Rank  |
| ----------------- | --------- | ------------ | --------- | ----- |
| Ridge Regression  | 24.50     | 29.26        | -0.43     | 2     |
| **Random Forest** | **24.50** | **29.14** ⭐ | **-0.41** | **1** |
| Gradient Boosting | 24.50     | 29.26        | -0.43     | 2     |

**Winner:** Random Forest Regressor (marginally better RMSE)

### 3.2 Key Observations

1. **Identical MAE:** All models predict with same average error (24.5 percentage points)
2. **Negative R²:** All models perform worse than simply predicting the mean
3. **Minimal Variation:** Little difference between models due to data constraints
4. **Feature Importance:** All features show 0 importance (Random Forest defaulting to mean)

---

## 4. Feature Importance Analysis

### 4.1 Random Forest Feature Importance

**Finding:** All features show 0% importance

| Feature          | Importance |
| ---------------- | ---------- |
| ACC_FAYDA        | 0.0        |
| ACC_MM_ACCOUNT   | 0.0        |
| ACC_MOBILE_PEN   | 0.0        |
| AFF_DATA_INCOME  | 0.0        |
| GEN_GAP_ACC      | 0.0        |
| GEN_GAP_MOBILE   | 0.0        |
| GEN_MM_SHARE     | 0.0        |
| USG_ACTIVE_RATE  | 0.0        |
| USG_MPESA_ACTIVE | 0.0        |
| USG_MPESA_USERS  | 0.0        |

**Interpretation:**

- Model cannot differentiate feature contributions with only 2 training samples
- Random Forest is essentially predicting the mean
- Need more data to identify meaningful feature relationships

### 4.2 Data Limitations Impact

**Root Causes:**

1. **Insufficient Training Data:** Only 2 samples for training
2. **High Dimensionality:** 10 features vs 2 samples (features > samples)
3. **Missing Values:** Most features have NaN for early years (2014, 2017)
4. **No Variation:** Limited feature variation in small sample

---

## 5. Visualizations Generated

### 5.1 Predicted vs Actual (Regression Models)

**Saved:** `reports/task4/regression_predictions.png`

**Description:**

- 3-panel comparison of Ridge, Random Forest, and Gradient Boosting
- Shows predicted vs actual account ownership rates
- Red dashed line represents perfect prediction
- All models show similar prediction patterns

### 5.2 Feature Importance (Random Forest)

**Saved:** `reports/task4/feature_importance.png`

**Description:**

- Horizontal bar chart of top 10 features
- All features show 0 importance (flat bars)
- Highlights data limitation issue

---

## 6. Model Artifacts Saved

### 6.1 Files Created

**Reports Directory** (`reports/task4/`):

1. `regression_results.csv` - Model performance metrics
2. `feature_importance_regression.csv` - Feature importance scores
3. `regression_predictions.png` - Predicted vs actual visualization
4. `feature_importance.png` - Feature importance chart

**Models Directory** (`models/`):

1. `rf_regressor.pkl` - Trained Random Forest Regressor
2. `scaler.pkl` - StandardScaler for feature normalization
3. `ml_model_metadata.json` - Model configuration and metrics

### 6.2 Model Metadata

```json
{
  "training_date": "2026-02-03",
  "n_features": 10,
  "features": [...],
  "train_years": [2014.0, 2017.0],
  "test_years": [2021.0, 2024.0],
  "best_classifier": "N/A",
  "best_regressor": "Random Forest",
  "regression_metrics": [...]
}
```

---

## 7. Limitations and Challenges

### 7.1 Data Constraints

1. **Sample Size:** Only 4 complete observations (2014, 2017, 2021, 2024)
2. **Missing Values:** 60-90% missing values for most features in early years
3. **Class Imbalance:** Single class in classification training set
4. **Temporal Sparsity:** Large gaps between observations (3-4 years)

### 7.2 Model Performance Issues

1. **Negative R²:** All models worse than mean baseline
2. **No Feature Learning:** Zero feature importance across all features
3. **High Error:** 24.5 MAE represents ~50% error on typical 49% ownership rate
4. **No Generalization:** Models cannot learn patterns from 2 training samples

### 7.3 Statistical Validity

**Warning:** Models are **NOT statistically reliable** for production use due to:

- Insufficient training data (n=2)
- Features outnumber samples (10 features > 2 samples)
- No cross-validation possible with 2 samples
- High variance expected in predictions

---

## 8. Recommendations

### 8.1 Short-Term Actions

1. **Use Time Series Instead:** Task 3's ETS model is more appropriate for this data
2. **Combine with Expert Knowledge:** Leverage domain expertise over ML
3. **Focus on Data Collection:** Prioritize gathering more historical data
4. **Simpler Models:** Use linear regression or correlation analysis

### 8.2 Long-Term Improvements

1. **Data Collection:**
   - Increase observation frequency (annual instead of 3-4 year gaps)
   - Fill historical gaps through data reconstruction
   - Target minimum 20-30 observations for reliable ML

2. **Feature Engineering:**
   - Create more robust features (rolling averages, momentum indicators)
   - External data integration (GDP, population, literacy rates)
   - Event impact quantification (policy change effects)

3. **Model Development:**
   - Implement cross-validation when data allows
   - Try ensemble methods combining time series + ML
   - Explore transfer learning from similar countries

4. **Alternative Approaches:**
   - **Synthetic Data Augmentation:** Generate plausible scenarios
   - **Bayesian Models:** Incorporate prior knowledge
   - **Semi-Supervised Learning:** Leverage unlabeled data
   - **Multi-Task Learning:** Learn from related tasks (mobile penetration, internet usage)

---

## 9. Conclusions

### 9.1 Summary

Task 4 successfully implemented a machine learning framework for financial inclusion prediction, but the **limited data availability (n=4)** severely constrains model performance and reliability. All three regression models (Ridge, Random Forest, Gradient Boosting) showed similar poor performance with negative R² values, indicating they cannot capture meaningful patterns from such limited training data.

### 9.2 Key Takeaways

1. ✅ **Framework Established:** Complete ML pipeline created and ready for more data
2. ✅ **Models Trained:** 3 regression models successfully trained and evaluated
3. ✅ **Artifacts Saved:** Models, results, and metadata preserved for future use
4. ⚠️ **Data Limitation:** 4 data points insufficient for reliable ML predictions
5. ⚠️ **Production Readiness:** Models NOT recommended for operational use

### 9.3 Best Approach for Current Data

**Recommendation:** Use **Task 3's ETS time series model** instead of ML for predictions with current data availability. The ETS model achieved:

- MAE: 7.0 (71% better than ML's 24.5)
- RMSE: 8.6 (70% better than ML's 29.1)
- MAPE: 14.4% (vs ML's ~50%)

### 9.4 Next Steps

1. **Immediate:** Rely on Task 3 forecasts for 2025-2027 planning
2. **Short-term:** Collect annual data points to increase sample size
3. **Medium-term:** Re-train ML models when n ≥ 20 observations available
4. **Long-term:** Implement hybrid time series + ML approach

---

## 10. Technical Appendix

### 10.1 Libraries Used

- **Core:** pandas 2.3.3, numpy 2.4.1
- **ML:** scikit-learn 1.8.0
- **Visualization:** matplotlib 3.10.8, seaborn 0.13.2

### 10.2 Model Hyperparameters

**Ridge Regression:**

```python
Ridge(alpha=1.0, random_state=42)
```

**Random Forest:**

```python
RandomForestRegressor(
    n_estimators=100,
    max_depth=3,
    random_state=42
)
```

**Gradient Boosting:**

```python
GradientBoostingRegressor(
    n_estimators=100,
    max_depth=2,
    random_state=42
)
```

### 10.3 Data Processing Steps

1. Load unified dataset (43 records)
2. Filter observations (30 records)
3. Pivot to wide format (5 years × 11 indicators)
4. Create lag and change features
5. Merge event counts (empty in current data)
6. Remove target leakage features
7. Drop NaN rows → 4 complete samples
8. Temporal split (70-30) → 2 train, 2 test
9. Standardize features using StandardScaler
10. Train models and evaluate

---

## Appendix: Files Generated

### Reports

- `reports/task4/regression_results.csv`
- `reports/task4/feature_importance_regression.csv`
- `reports/task4/regression_predictions.png`
- `reports/task4/feature_importance.png`
- `reports/task4/TASK4_REPORT.md` (this file)

### Models

- `models/rf_regressor.pkl`
- `models/scaler.pkl`
- `models/ml_model_metadata.json`

### Notebook

- `notebooks/task4_machine_learning_models.ipynb` (24 cells)

---

**Report Generated:** February 3, 2026  
**Analysis By:** GitHub Copilot  
**Project:** Forecasting Financial Inclusion in Ethiopia  
**Task Status:** ✅ Complete (with data limitations noted)
