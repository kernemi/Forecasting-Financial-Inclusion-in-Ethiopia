# Task 4: Machine Learning Models

This directory contains the results of Task 4: Machine Learning Models for Ethiopia Financial Inclusion prediction.

## Files in this Directory

### Results Files

- **`regression_results.csv`** - Performance metrics (MAE, RMSE, R²) for all regression models
- **`feature_importance_regression.csv`** - Feature importance scores from Random Forest model

### Visualizations

- **`regression_predictions.png`** - Predicted vs actual scatter plots for Ridge, Random Forest, and Gradient Boosting models
- **`feature_importance.png`** - Bar chart showing feature importance (all 0 due to limited data)

### Reports

- **`TASK4_REPORT.md`** - Comprehensive analysis report with methodology, results, and recommendations

## Key Findings

### Best Model

- **Random Forest Regressor** (marginally better RMSE: 29.14 vs 29.26)

### Performance Metrics

| Model             | MAE       | RMSE      | R²        |
| ----------------- | --------- | --------- | --------- |
| Ridge Regression  | 24.50     | 29.26     | -0.43     |
| **Random Forest** | **24.50** | **29.14** | **-0.41** |
| Gradient Boosting | 24.50     | 29.26     | -0.43     |

### Data Limitations

⚠️ **Critical Issue:** Only 4 data points available for training/testing

- Train size: 2 samples (2014, 2017)
- Test size: 2 samples (2021, 2024)
- Features: 10 (exceeds training samples)
- Result: Models cannot learn meaningful patterns

### Feature Importance

All features show 0% importance due to insufficient training data:

- ACC_FAYDA, ACC_MM_ACCOUNT, ACC_MOBILE_PEN
- AFF_DATA_INCOME, GEN_GAP_ACC, GEN_GAP_MOBILE
- GEN_MM_SHARE, USG_ACTIVE_RATE, USG_MPESA_ACTIVE, USG_MPESA_USERS

## Recommendations

### ⚠️ Production Use

**NOT RECOMMENDED** for production predictions due to:

- Negative R² (worse than mean baseline)
- Only 2 training samples
- High error rate (~50% MAPE)
- No feature differentiation

### ✅ Alternative Approach

**Use Task 3's ETS time series model instead:**

- ETS MAE: 7.0 (71% better)
- ETS RMSE: 8.6 (70% better)
- ETS MAPE: 14.4% (much more accurate)

### 🔄 Future Improvements

1. Collect more annual observations (target: 20-30 samples)
2. Fill historical data gaps
3. Re-train models when sufficient data available
4. Consider hybrid time series + ML approach

## Models Saved

Location: `../../models/`

- `rf_regressor.pkl` - Trained Random Forest Regressor
- `scaler.pkl` - StandardScaler for feature normalization
- `ml_model_metadata.json` - Model configuration and performance metrics

## Usage

### Load Saved Model

```python
import pickle
import pandas as pd

# Load model and scaler
with open('../../models/rf_regressor.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../../models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Prepare features (must match training features)
features = ['ACC_FAYDA', 'ACC_MM_ACCOUNT', 'ACC_MOBILE_PEN',
            'AFF_DATA_INCOME', 'GEN_GAP_ACC', 'GEN_GAP_MOBILE',
            'GEN_MM_SHARE', 'USG_ACTIVE_RATE', 'USG_MPESA_ACTIVE',
            'USG_MPESA_USERS']

# Scale and predict
X_scaled = scaler.transform(X[features])
predictions = model.predict(X_scaled)
```

⚠️ **Warning:** Predictions will have high uncertainty due to limited training data.

## Related Tasks

- **Task 3:** Time series forecasting (ARIMA, ETS) - **RECOMMENDED for current data**
- **Task 2:** Exploratory data analysis and feature understanding
- **Task 5:** Advanced forecasting methods (if applicable)

## Contact

For questions about this analysis, refer to:

- Comprehensive report: `TASK4_REPORT.md`
- Notebook: `../../notebooks/task4_machine_learning_models.ipynb`
- Project documentation: `../../README.md`
