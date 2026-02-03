"""
Script to generate images from CSV files in Task 3 report
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Define paths
task3_dir = 'reports/task3'
output_dir = task3_dir

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# 1. Generate image for account_ownership_forecast_2025_2027.csv
print("Generating forecast visualization...")
forecast_df = pd.read_csv(f'{task3_dir}/account_ownership_forecast_2025_2027.csv')

fig, ax = plt.subplots(figsize=(12, 7))

# Plot forecast with confidence intervals
ax.plot(forecast_df['year'], forecast_df['forecast'], 
        marker='o', linewidth=2.5, markersize=8, 
        color='#2E86AB', label='Forecast')

# Fill confidence interval
ax.fill_between(forecast_df['year'], 
                forecast_df['lower_ci'], 
                forecast_df['upper_ci'],
                alpha=0.3, color='#2E86AB', label='95% Confidence Interval')

# Add data points as annotations
for _, row in forecast_df.iterrows():
    ax.annotate(f"{row['forecast']:.1f}%", 
               xy=(row['year'], row['forecast']),
               xytext=(0, 10), textcoords='offset points',
               ha='center', fontsize=11, fontweight='bold')

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Account Ownership Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Account Ownership Forecast (2025-2027)\nExponential Smoothing Model', 
            fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3)
ax.set_ylim(50, 95)

plt.tight_layout()
plt.savefig(f'{output_dir}/account_ownership_forecast_visualization.png', 
            dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir}/account_ownership_forecast_visualization.png")
plt.close()

# 2. Generate image for model_performance_comparison.csv
print("\nGenerating model performance comparison...")
performance_df = pd.read_csv(f'{task3_dir}/model_performance_comparison.csv')

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

metrics = ['MAE', 'RMSE', 'MAPE']
colors = ['#A23B72', '#F18F01', '#C73E1D']

for idx, (ax, metric, color) in enumerate(zip(axes, metrics, colors)):
    bars = ax.bar(performance_df['Model'], performance_df[metric], 
                  color=color, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.2f}',
               ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel(metric, fontsize=12, fontweight='bold')
    ax.set_title(f'{metric} Comparison', fontsize=13, fontweight='bold')
    ax.tick_params(axis='x', rotation=0)
    ax.grid(axis='y', alpha=0.3)

plt.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{output_dir}/model_performance_comparison_visualization.png', 
            dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir}/model_performance_comparison_visualization.png")
plt.close()

# 3. Generate combined table image
print("\nGenerating table visualizations...")

# Forecast table
fig, ax = plt.subplots(figsize=(10, 3))
ax.axis('tight')
ax.axis('off')

# Format data for table
forecast_table_data = []
for _, row in forecast_df.iterrows():
    forecast_table_data.append([
        int(row['year']),
        f"{row['forecast']:.1f}%",
        f"{row['lower_ci']:.1f}% - {row['upper_ci']:.1f}%"
    ])

table = ax.table(cellText=forecast_table_data,
                colLabels=['Year', 'Forecast', '95% Confidence Interval'],
                cellLoc='center',
                loc='center',
                colWidths=[0.2, 0.3, 0.5])

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Style header
for i in range(3):
    table[(0, i)].set_facecolor('#2E86AB')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style cells
for i in range(1, len(forecast_table_data) + 1):
    for j in range(3):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#E8F4F8')
        else:
            table[(i, j)].set_facecolor('white')

plt.title('Account Ownership Forecast (2025-2027)', 
         fontsize=14, fontweight='bold', pad=20)
plt.savefig(f'{output_dir}/forecast_table.png', 
           dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir}/forecast_table.png")
plt.close()

# Performance table
fig, ax = plt.subplots(figsize=(10, 3))
ax.axis('tight')
ax.axis('off')

# Format data for table
perf_table_data = []
for _, row in performance_df.iterrows():
    perf_table_data.append([
        row['Model'],
        f"{row['MAE']:.2f}",
        f"{row['RMSE']:.2f}",
        f"{row['MAPE']:.2f}%"
    ])

table = ax.table(cellText=perf_table_data,
                colLabels=['Model', 'MAE', 'RMSE', 'MAPE'],
                cellLoc='center',
                loc='center',
                colWidths=[0.3, 0.23, 0.23, 0.24])

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Style header
for i in range(4):
    table[(0, i)].set_facecolor('#F18F01')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style cells - highlight best model
for i in range(1, len(perf_table_data) + 1):
    for j in range(4):
        if i == 2:  # ETS row (better performance)
            table[(i, j)].set_facecolor('#D4EDDA')
        else:
            table[(i, j)].set_facecolor('#F8D7DA')

plt.title('Model Performance Comparison', 
         fontsize=14, fontweight='bold', pad=20)
plt.savefig(f'{output_dir}/performance_table.png', 
           dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_dir}/performance_table.png")
plt.close()

print("\n" + "="*60)
print("All visualizations generated successfully!")
print("="*60)
print(f"\nGenerated files in {output_dir}/:")
print("  1. account_ownership_forecast_visualization.png")
print("  2. model_performance_comparison_visualization.png")
print("  3. forecast_table.png")
print("  4. performance_table.png")
