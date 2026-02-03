# Visualization Placeholder

This file serves as a placeholder for: **events_timeline.png**

## What this visualization shows:

This is a 2-panel figure that will be generated when running the Task 1 notebook:

### Panel 1: Events Timeline Scatter Plot

- Scatter plot with dates on X-axis, event categories on Y-axis
- Color-coded by category (policy, product_launch, infrastructure, market_entry, milestone)
- Event labels show first 20 characters of event name
- Shows chronological distribution of events

### Panel 2: Events Distribution by Year and Category

- Stacked bar chart showing events per year
- Each bar segment represents an event category
- Color-matched to Panel 1
- Reveals event clustering patterns (e.g., 2021-2022 peak)

## Key Events Visible:

- **2021-05:** Telebirr Launch (product_launch) - Red
- **2022-08:** Safaricom Market Entry (market_entry) - Orange
- **2023-08:** M-Pesa Launch (product_launch) - Red
- **2024-03:** Digital > ATM Milestone (milestone) - Purple

## To Generate:

Run the Task 1 Jupyter notebook:

```bash
jupyter notebook notebooks/task1_data_exploration_enrichment.ipynb
```

The visualization will be automatically saved to this location.
