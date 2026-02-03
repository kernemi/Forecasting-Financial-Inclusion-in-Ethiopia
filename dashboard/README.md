# Ethiopia Financial Inclusion Dashboard

Interactive Streamlit dashboard for visualizing forecasting and analysis results.

## 🚀 Quick Start

### Installation

1. **Install dependencies:**

   ```bash
   pip install streamlit plotly openpyxl
   ```

2. **Run the dashboard:**

   ```bash
   streamlit run dashboard/app.py
   ```

3. **Access the dashboard:**
   - Local URL: http://localhost:8501
   - Network URL: Will be displayed in terminal

## 📊 Dashboard Features

### 🏠 Overview Page

- **Key Performance Indicators (KPIs)**
  - Current account ownership (2024)
  - Forecast for 2027
  - Total observations and events
- **Historical Trend Visualization**
  - Combined historical + forecast chart
  - 95% confidence intervals
- **Key Insights**
  - Growth trajectory analysis
  - Best model performance summary

### 📈 Forecasting Page

- **Model Comparison**
  - ARIMA vs ETS performance metrics
  - Interactive bar charts
- **Best Model Highlight**
  - ETS model metrics card
  - Production recommendation
- **Detailed Forecasts Table**
  - 2025-2027 predictions
  - Confidence intervals
- **Uncertainty Visualization**
  - Interactive forecast chart with CI bands

### 🤖 ML Insights Page

- **Data Limitation Warning**
  - Clear notice about small dataset (n=4)
- **Regression Model Comparison**
  - MAE and R² visualizations
  - Ridge, Random Forest, Gradient Boosting
- **Performance Metrics Table**
  - Detailed model statistics
- **Feature Importance Analysis**
  - Top 10 features chart (when available)
  - Model insights cards

### 📊 Data Explorer Page

- **Interactive Filters**
  - Record type selection
  - Pillar filtering
  - Year range slider
- **Summary Statistics**
  - Filtered record counts
  - Observations vs events breakdown
- **Data Table**
  - Searchable, sortable table
  - Download CSV functionality
- **Distribution Charts**
  - Pie chart by pillar

### ℹ️ About Page

- **Project Overview**
  - All 5 tasks description
  - Key findings summary
- **Technology Stack**
  - Tools and libraries used
- **Data Sources**
  - Origin and credibility
- **Contact Information**

## 🎨 Features

### Interactive Visualizations

- **Plotly Charts:**
  - Hover tooltips
  - Zoom and pan
  - Download as PNG
  - Responsive design

### Data Exploration

- **Dynamic Filtering:**
  - Multi-select dropdowns
  - Range sliders
  - Real-time updates

### Export Capabilities

- **CSV Downloads:**
  - Filtered datasets
  - Custom queries

## 📁 File Structure

```
dashboard/
├── app.py              # Main dashboard application
└── README.md           # This file
```

## 🔧 Configuration

### Custom Styling

The dashboard uses custom CSS for:

- Header formatting
- Metric cards
- Insight boxes
- Warning notifications

### Layout

- **Wide mode** enabled by default
- **Sidebar navigation** for page selection
- **Responsive columns** for mobile compatibility

## 📊 Data Requirements

The dashboard expects the following files:

### Required Files:

1. `data/raw/ethiopia_fi_unified_data.xlsx` - Main dataset
2. `reports/task3/account_ownership_forecast_2025_2027.csv` - Forecasts
3. `reports/task3/model_performance_comparison.csv` - TS model metrics
4. `reports/task4/regression_results.csv` - ML model metrics
5. `reports/task4/feature_importance_regression.csv` - Feature importance

### Data Format:

- **Main dataset columns:**
  - fiscal_year, record_type, pillar, indicator, indicator_code
  - value_numeric, value_type, unit

- **Forecast columns:**
  - year, forecast, lower_ci, upper_ci

## 🎯 Usage Examples

### Running Locally

```bash
# From project root
streamlit run dashboard/app.py

# Custom port
streamlit run dashboard/app.py --server.port 8502

# With auto-reload
streamlit run dashboard/app.py --server.runOnSave true
```

### Deploying to Streamlit Cloud

1. Push to GitHub repository
2. Connect at https://streamlit.io/cloud
3. Select repository and branch
4. Specify `dashboard/app.py` as main file
5. Deploy!

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install streamlit plotly openpyxl pandas numpy

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔍 Troubleshooting

### Common Issues

**1. Module not found error:**

```bash
pip install -r requirements.txt
```

**2. Data file not found:**

- Ensure you're running from project root
- Check file paths in `load_data()` functions
- Verify all Task 3 and Task 4 files exist

**3. Port already in use:**

```bash
streamlit run dashboard/app.py --server.port 8502
```

**4. Visualization not rendering:**

- Clear browser cache
- Try different browser (Chrome recommended)
- Check browser console for errors

## 📈 Performance

### Optimization Features

- **@st.cache_data** decorator for data loading
- Efficient Plotly rendering
- Lazy loading of large datasets

### Expected Performance

- Initial load: < 3 seconds
- Page navigation: < 1 second
- Chart interactions: Real-time

## 🛠️ Customization

### Adding New Pages

1. Add new page option in sidebar radio
2. Create elif block for page content
3. Import required data/functions
4. Design visualizations

### Modifying Charts

- Edit Plotly figure parameters in `go.Figure()` calls
- Adjust colors, sizes, layouts
- Add/remove traces

### Changing Styles

- Modify CSS in `st.markdown()` at top
- Update color schemes
- Adjust card layouts

## 📚 Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Plotly Python:** https://plotly.com/python/
- **Pandas:** https://pandas.pydata.org/docs/

## 🚀 Future Enhancements

Potential improvements:

- [ ] Real-time data updates
- [ ] User authentication
- [ ] Export to PDF reports
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Advanced filtering options
- [ ] Comparative analysis tools
- [ ] What-if scenario modeling

## ⚠️ Notes

- Dashboard requires Python 3.8+
- Best viewed on desktop (1920x1080)
- Mobile responsive design included
- Internet connection needed for initial Plotly CDN

## 📝 Version History

- **v1.0.0** (Feb 2026) - Initial release
  - 5 pages (Overview, Forecasting, ML, Explorer, About)
  - Interactive Plotly visualizations
  - Data export functionality
  - Responsive design

---

**Project:** Forecasting Financial Inclusion in Ethiopia  
**Dashboard Version:** 1.0.0  
**Last Updated:** February 3, 2026
