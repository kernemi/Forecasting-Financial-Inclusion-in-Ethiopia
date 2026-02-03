# Task 3: Time Series Forecasting - Outputs

This folder contains outputs from Task 3: Time Series Forecasting analysis of Ethiopia's financial inclusion metrics.

## Files

### Reports

- **`TASK3_REPORT.md`**: Comprehensive analysis report with methodology, results, and recommendations

### Data Outputs

- **`account_ownership_forecast_2025_2027.csv`**: Point forecasts and 95% confidence intervals for 2025-2027
- **`model_performance_comparison.csv`**: Model evaluation metrics (MAE, RMSE, MAPE)

### Visualizations

- **`acf_pacf_analysis.png`**: Autocorrelation and partial autocorrelation plots
- **`model_validation.png`**: Train/test validation comparison (ARIMA vs ETS)
- **Forecast visualization**: Generated in notebook (Ethiopia Account Ownership Forecast 2025-2027)

## Quick Results

**Best Model**: Exponential Smoothing (ETS)

- MAE: 7.0%
- RMSE: 8.6%
- MAPE: 14.4%

**Forecasts** (Account Ownership %):

- 2025: 61.0% (95% CI: 55.9% - 66.1%)
- 2026: 70.2% (95% CI: 63.0% - 77.4%)
- 2027: 79.4% (95% CI: 70.6% - 88.2%)

## Source Notebook

All analysis code is in: `notebooks/task3_time_series_forecasting.ipynb`

To reproduce:

```bash
cd notebooks
jupyter notebook task3_time_series_forecasting.ipynb
```

## Data Source

Input data: `data/raw/ethiopia_fi_unified_data.xlsx`

- Sheet: `ethiopia_fi_unified_data`
- Indicator: ACC_OWNERSHIP (Account Ownership Rate)
- Historical period: 2014-2024 (4 data points)
