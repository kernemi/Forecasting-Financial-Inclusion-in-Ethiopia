# Notebooks

This folder contains Jupyter notebooks for the Ethiopia Financial Inclusion Forecasting project.

## Notebooks Overview

1. **task1_data_exploration_enrichment.ipynb**
   - Load and understand the unified data schema
   - Explore observations, events, and impact links
   - Enrich dataset with additional data points
   - Generate data enrichment log and visualizations

2. **task2_exploratory_data_analysis.ipynb** (Coming soon)
   - Dataset overview and temporal coverage
   - Access (account ownership) analysis
   - Usage (digital payments) analysis
   - Infrastructure and enablers analysis
   - Event timeline and correlation analysis

3. **task3_event_impact_modeling.ipynb** (Coming soon)
   - Build event-indicator association matrix
   - Model impact relationships
   - Validate against historical data

4. **task4_forecasting.ipynb** (Coming soon)
   - Forecast Access (Account Ownership) for 2025-2027
   - Forecast Usage (Digital Payments) for 2025-2027
   - Generate confidence intervals and scenarios

## Running the Notebooks

1. Install dependencies:

   ```bash
   pip install -r ../requirements.txt
   ```

2. Launch Jupyter:

   ```bash
   jupyter notebook
   ```

3. Run notebooks in order (task1 → task2 → task3 → task4)

## Output Locations

- **Processed Data:** `../data/processed/`
- **Visualizations:** `../reports/task[N]/`
- **Models:** `../models/`
