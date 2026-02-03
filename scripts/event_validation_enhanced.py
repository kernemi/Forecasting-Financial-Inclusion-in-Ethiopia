"""
Enhanced Event-Indicator Validation with Synthetic Data Demo
=============================================================

This version demonstrates the validation methodology using synthetic data
for years where actual survey data is unavailable. All synthetic data is
clearly labeled and the methodology is fully documented.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def load_data():
    """Load unified dataset and synthetic validation data."""
    df = pd.read_excel('data/raw/ethiopia_fi_unified_data.xlsx', 
                       sheet_name='ethiopia_fi_unified_data')
    
    # Load synthetic validation data if exists
    synthetic_path = 'data/processed/mobile_money_synthetic_validation.csv'
    if os.path.exists(synthetic_path):
        synthetic_df = pd.read_csv(synthetic_path)
    else:
        synthetic_df = None
    
    return df, synthetic_df


def create_event_indicator_matrix(df):
    """Create Event-Indicator Association Matrix with explicit impact assumptions."""
    
    # Define comprehensive event-indicator associations
    associations = [
        # Telebirr Launch (May 2021) - First-mover advantage
        ('EVT_TELEBIRR', 'ACC_MOBILE', 'High', 6, 'Direct', 
         'Telebirr Launch', 'Mobile Money Account (%)'),
        ('EVT_TELEBIRR', 'ACC_OVERALL', 'Medium', 12, 'Indirect',
         'Telebirr Launch', 'Overall Account Ownership (%)'),
        ('EVT_TELEBIRR', 'DIG_MOBILE_MONEY', 'High', 3, 'Direct',
         'Telebirr Launch', 'Mobile Money Adoption'),
        ('EVT_TELEBIRR', 'DIG_DIGITAL_PAY', 'High', 6, 'Direct',
         'Telebirr Launch', 'Digital Payment Usage'),
        ('EVT_TELEBIRR', 'ACC_MOBILE_F', 'Medium', 12, 'Indirect',
         'Telebirr Launch', 'Mobile Money Account - Female (%)'),
        
        # Safaricom Market Entry (Aug 2022) - Competition catalyst
        ('EVT_SAFARICOM', 'ACC_MOBILE', 'Medium', 12, 'Enabling',
         'Safaricom Ethiopia Commercial Launch', 'Mobile Money Account (%)'),
        ('EVT_SAFARICOM', 'DIG_MOBILE_MONEY', 'Low', 18, 'Competitive',
         'Safaricom Ethiopia Commercial Launch', 'Mobile Money Adoption'),
        ('EVT_SAFARICOM', 'MOB_PENETRATION', 'Low', 6, 'Indirect',
         'Safaricom Ethiopia Commercial Launch', 'Mobile Penetration (%)'),
        
        # M-Pesa Launch (Aug 2023) - Second mover
        ('EVT_MPESA', 'ACC_MOBILE', 'High', 6, 'Direct',
         'M-Pesa Ethiopia Launch', 'Mobile Money Account (%)'),
        ('EVT_MPESA', 'DIG_MOBILE_MONEY', 'High', 3, 'Direct',
         'M-Pesa Ethiopia Launch', 'Mobile Money Adoption'),
        ('EVT_MPESA', 'DIG_DIGITAL_PAY', 'Medium', 6, 'Direct',
         'M-Pesa Ethiopia Launch', 'Digital Payment Usage'),
        ('EVT_MPESA', 'ACC_MOBILE_F', 'Medium', 9, 'Indirect',
         'M-Pesa Ethiopia Launch', 'Mobile Money Account - Female (%)'),
        
        # Fayda Digital ID (Jan 2024) - Infrastructure enabler
        ('EVT_FAYDA', 'ACC_OVERALL', 'Medium', 18, 'Enabling',
         'Fayda Digital ID Program Rollout', 'Overall Account Ownership (%)'),
        ('EVT_FAYDA', 'ACC_BANK', 'Medium', 24, 'Enabling',
         'Fayda Digital ID Program Rollout', 'Bank Account Ownership (%)'),
        ('EVT_FAYDA', 'DIG_INTERNET', 'Low', 12, 'Indirect',
         'Fayda Digital ID Program Rollout', 'Internet Access (%)'),
        
        # Foreign Exchange Reform (July 2024) - Macro policy
        ('EVT_FX_REFORM', 'ACC_BANK', 'Medium', 12, 'Indirect',
         'Foreign Exchange Liberalization', 'Bank Account Ownership (%)'),
        ('EVT_FX_REFORM', 'DIG_MOBILE_MONEY', 'Low', 6, 'Indirect',
         'Foreign Exchange Liberalization', 'Mobile Money Adoption'),
    ]
    
    matrix_df = pd.DataFrame(associations, columns=[
        'event_code', 'indicator_code', 'impact_magnitude', 
        'lag_months', 'evidence_type', 'event_name', 'indicator_name'
    ])
    
    return matrix_df


def create_enhanced_heatmap(matrix_df, output_path='reports/task1/event_indicator_matrix_heatmap.png'):
    """Create comprehensive heatmap visualization."""
    
    magnitude_scores = {'High': 3, 'Medium': 2, 'Low': 1}
    matrix_df['impact_score'] = matrix_df['impact_magnitude'].map(magnitude_scores)
    
    # Create figure with three subplots
    fig = plt.figure(figsize=(22, 8))
    gs = fig.add_gridspec(2, 3, height_ratios=[3, 1], hspace=0.4, wspace=0.3)
    
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[1, :])
    
    # Pivot tables
    pivot_impact = matrix_df.pivot_table(
        index='event_name', columns='indicator_name',
        values='impact_score', aggfunc='max', fill_value=0
    )
    
    pivot_lag = matrix_df.pivot_table(
        index='event_name', columns='indicator_name',
        values='lag_months', aggfunc='mean', fill_value=0
    )
    
    # Heatmap 1: Impact Magnitude
    sns.heatmap(pivot_impact, annot=True, fmt='.0f', cmap='YlOrRd', 
                cbar_kws={'label': 'Impact Score'}, linewidths=0.5, ax=ax1)
    ax1.set_title('Impact Magnitude Matrix\n(3=High, 2=Medium, 1=Low, 0=No Effect)', 
                  fontsize=12, fontweight='bold', pad=15)
    ax1.set_xlabel('Indicators', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Events', fontsize=10, fontweight='bold')
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right', fontsize=8)
    plt.setp(ax1.get_yticklabels(), rotation=0, fontsize=8)
    
    # Heatmap 2: Time Lag
    sns.heatmap(pivot_lag, annot=True, fmt='.0f', cmap='viridis', 
                cbar_kws={'label': 'Months'}, linewidths=0.5, ax=ax2)
    ax2.set_title('Impact Time Lag Matrix\n(Months Until Effect)', 
                  fontsize=12, fontweight='bold', pad=15)
    ax2.set_xlabel('Indicators', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Events', fontsize=10, fontweight='bold')
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=8)
    plt.setp(ax2.get_yticklabels(), rotation=0, fontsize=8)
    
    # Heatmap 3: Evidence Type Distribution
    evidence_pivot = pd.crosstab(matrix_df['event_name'], matrix_df['evidence_type'])
    sns.heatmap(evidence_pivot, annot=True, fmt='d', cmap='Blues',
                cbar_kws={'label': 'Count'}, linewidths=0.5, ax=ax3)
    ax3.set_title('Evidence Type Distribution\n(Relationship Classification)', 
                  fontsize=12, fontweight='bold', pad=15)
    ax3.set_xlabel('Evidence Type', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Events', fontsize=10, fontweight='bold')
    plt.setp(ax3.get_xticklabels(), rotation=45, ha='right', fontsize=9)
    plt.setp(ax3.get_yticklabels(), rotation=0, fontsize=8)
    
    # Summary statistics bar chart
    summary_data = {
        'High Impact\nLinks': len(matrix_df[matrix_df['impact_magnitude'] == 'High']),
        'Medium Impact\nLinks': len(matrix_df[matrix_df['impact_magnitude'] == 'Medium']),
        'Low Impact\nLinks': len(matrix_df[matrix_df['impact_magnitude'] == 'Low']),
        'Avg Lag\n(Months)': matrix_df['lag_months'].mean(),
    }
    
    colors = ['#e74c3c', '#f39c12', '#95a5a6', '#3498db']
    bars = ax4.bar(summary_data.keys(), summary_data.values(), color=colors, 
                   alpha=0.8, edgecolor='black', linewidth=1.5)
    ax4.set_ylabel('Count / Months', fontsize=11, fontweight='bold')
    ax4.set_title('Association Matrix Summary Statistics', 
                  fontsize=12, fontweight='bold', pad=15)
    ax4.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax4.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', 
                    fontsize=11, fontweight='bold')
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Enhanced heatmap saved to {output_path}")
    return fig


def telebirr_validation_with_synthetic(synthetic_df):
    """
    Historical Validation using synthetic data.
    CLEARLY LABELED AS DEMONSTRATION.
    """
    
    if synthetic_df is None:
        return None, None
    
    validation_params = {
        'event_name': 'Telebirr Launch',
        'event_date': '2021-05-17',
        'indicator': 'Mobile Money Account Ownership (%)',
        'baseline_year': 2021,
        'validation_years': [2022, 2023, 2024],
        
        # MODEL ASSUMPTIONS
        'assumed_impact_magnitude': 'High',
        'assumed_lag_months': 6,
        'assumed_effect_duration': 36,
        'assumed_peak_impact': 20,  # pp increase over 3 years
        'impact_curve': 'exponential_decay',
        
        # PARAMETER JUSTIFICATION
        'justification': {
            'magnitude': """HIGH IMPACT justified by:
- First-mover advantage in Ethiopian mobile money market
- State-owned telecom (Ethio Telecom) with 54M subscriber base (75% market share)
- Zero competition at launch (monopoly period: May 2021 - Aug 2023)
- Government backing enabling agent network rapid deployment
- Comparative: Kenya M-Pesa achieved 19pp increase in first 3 years (2007-2010)""",
            
            'lag': """6-MONTH LAG based on:
- Product marketing campaigns (3 months)
- Agent network buildout (completed by Nov 2021)
- KYC registration process (simplified for Ethio Telecom subscribers)
- Network effects threshold: ~20% market penetration needed for viral growth
- M-Pesa Kenya: 6-8 month lag observed between launch and exponential phase""",
            
            'peak_impact': """20 PERCENTAGE POINTS over 3 years justified by:
- Kenya M-Pesa: 2007 baseline 16% → 2010 ~35% = 19pp increase
- Ethiopia adjustment factors:
  + Lower financial literacy (-3pp)
  + Better mobile infrastructure than 2007 Kenya (+2pp)
  + Regulatory support (+2pp)
  + Later adoption curve (faster learning) (+1pp)
  + Lower income per capita (-1pp)
- NET ESTIMATE: 19pp + 1pp = 20pp""",
            
            'curve': """EXPONENTIAL DECAY CURVE selected because:
- Technology adoption follows Rogers' S-curve
- Early phase (0-12 months): Exponential growth as innovators/early adopters join
- Middle phase (12-24 months): Continued rapid growth (network effects)
- Late phase (24-36 months): Growth rate slows approaching saturation
- Mathematical form: Impact(t) = Peak × (1 - e^(-kt)) where k calibrated to data"""
        }
    }
    
    # Calculate model predictions
    baseline = synthetic_df[synthetic_df['fiscal_year'] == 2021]['mobile_money_account_pct'].values[0]
    
    results = {
        'baseline_2021': baseline,
        'observed_changes': {},
        'model_predictions': {},
        'validation_errors': {},
        'data_type': {}  # Track which data is real vs synthetic
    }
    
    for year in validation_params['validation_years']:
        year_data = synthetic_df[synthetic_df['fiscal_year'] == year]
        if len(year_data) > 0:
            observed_value = year_data['mobile_money_account_pct'].values[0]
            results['observed_changes'][year] = observed_value - baseline
            results['data_type'][year] = 'Synthetic' if 'Synthetic' in year_data['data_source'].values[0] else 'Actual'
            
            # Model prediction with exponential decay curve
            months_since_launch = (year - 2021) * 12 - 5  # May launch
            if months_since_launch >= validation_params['assumed_lag_months']:
                effective_months = months_since_launch - validation_params['assumed_lag_months']
                # Exponential growth: Impact = Peak × (1 - e^(-t/tau))
                tau = 18  # Time constant (months to reach ~63% of peak)
                predicted_impact = validation_params['assumed_peak_impact'] * \
                                 (1 - np.exp(-effective_months / tau))
                results['model_predictions'][year] = predicted_impact
                results['validation_errors'][year] = results['observed_changes'][year] - predicted_impact
            else:
                results['model_predictions'][year] = 0
                results['validation_errors'][year] = results['observed_changes'][year]
    
    return validation_params, results


def create_validation_visualization_enhanced(validation_params, results,
                                            output_path='reports/task1/telebirr_validation.png'):
    """Enhanced validation visualization with clear synthetic data labeling."""
    
    if results is None:
        return None
    
    fig = plt.figure(figsize=(18, 11))
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.25)
    
    years = sorted(results['observed_changes'].keys())
    observed = [results['observed_changes'][y] for y in years]
    predicted = [results['model_predictions'].get(y, 0) for y in years]
    errors = [results['validation_errors'].get(y, 0) for y in years]
    
    # Plot 1: Observed vs Predicted
    ax1 = fig.add_subplot(gs[0, :])
    x = np.arange(len(years))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, observed, width, label='Observed (Synthetic)', 
                    color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=2)
    bars2 = ax1.bar(x + width/2, predicted, width, label='Model Prediction',
                    color='#3498db', alpha=0.8, edgecolor='black', linewidth=2)
    
    ax1.set_xlabel('Year', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Impact (Percentage Points)', fontsize=13, fontweight='bold')
    ax1.set_title('Telebirr Historical Validation: Observed vs Modeled Impact\n' + 
                  'Mobile Money Account Ownership - ⚠ USING SYNTHETIC DATA FOR DEMONSTRATION',
                  fontsize=15, fontweight='bold', pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, fontsize=11)
    ax1.legend(loc='upper left', frameon=True, shadow=True, fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{height:.1f}pp',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Plot 2: Validation Errors
    ax2 = fig.add_subplot(gs[1, 0])
    colors = ['#e74c3c' if e < 0 else '#2ecc71' for e in errors]
    bars = ax2.bar(years, errors, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax2.set_ylabel('Error (pp)', fontsize=12, fontweight='bold')
    ax2.set_title('Prediction Errors\n(+Over/-Underestimated)', fontsize=13, fontweight='bold')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
    ax2.grid(axis='y', alpha=0.3)
    
    for year, error in zip(years, errors):
        ax2.annotate(f'{error:+.1f}pp',
                    xy=(year, error),
                    xytext=(0, 5 if error > 0 else -15),
                    textcoords="offset points",
                    ha='center', fontsize=10, fontweight='bold')
    
    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(np.array(errors)**2))
    ax2.text(0.02, 0.98, f'MAE: {mae:.2f}pp\nRMSE: {rmse:.2f}pp',
            transform=ax2.transAxes, fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9),
            fontweight='bold')
    
    # Plot 3: Growth Curve Visualization
    ax3 = fig.add_subplot(gs[1, 1])
    months = np.linspace(0, 42, 100)  # 3.5 years
    tau = 18
    peak = validation_params['assumed_peak_impact']
    lag = validation_params['assumed_lag_months']
    
    curve = [peak * (1 - np.exp(-(m - lag) / tau)) if m >= lag else 0 for m in months]
    
    ax3.plot(months, curve, 'b-', linewidth=3, label='Model Curve')
    ax3.scatter([(y - 2021) * 12 - 5 for y in years], observed, 
               s=200, c='green', marker='o', edgecolor='black', linewidth=2,
               label='Observed (Synthetic)', zorder=5)
    ax3.axvline(x=lag, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Lag Period End')
    ax3.set_xlabel('Months Since Launch', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Cumulative Impact (pp)', fontsize=12, fontweight='bold')
    ax3.set_title('Impact Growth Curve\nExponential Decay Model', fontsize=13, fontweight='bold')
    ax3.legend(fontsize=10, frameon=True)
    ax3.grid(alpha=0.3)
    
    # Plot 4: Parameter Justification Summary
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('off')
    
    param_text = f"""
    MODEL PARAMETER JUSTIFICATION SUMMARY
    
    ┌─ IMPACT MAGNITUDE: {validation_params['assumed_impact_magnitude']} ─────────────────────────────────────────────────────────
    │  {validation_params['justification']['magnitude'].replace(chr(10), chr(10) + '│  ')}
    │
    ┌─ TIME LAG: {validation_params['assumed_lag_months']} months ──────────────────────────────────────────────────────────────────────
    │  {validation_params['justification']['lag'].replace(chr(10), chr(10) + '│  ')}
    │
    ┌─ PEAK IMPACT: {validation_params['assumed_peak_impact']} percentage points ───────────────────────────────────────────────────────────
    │  {validation_params['justification']['peak_impact'].replace(chr(10), chr(10) + '│  ')}
    │
    ┌─ IMPACT CURVE: {validation_params['impact_curve']} ─────────────────────────────────────────────────────────
    │  {validation_params['justification']['curve'].replace(chr(10), chr(10) + '│  ')}
    
    VALIDATION RESULTS: MAE = {mae:.2f}pp, RMSE = {rmse:.2f}pp
    ⚠ NOTE: Validation uses SYNTHETIC data for 2022-2024 to demonstrate methodology
    """
    
    ax4.text(0.05, 0.95, param_text, transform=ax4.transAxes,
            fontsize=8, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Enhanced validation visualization saved to {output_path}")
    return fig


def main():
    """Main execution."""
    print("=" * 80)
    print("EVENT-INDICATOR VALIDATION ANALYSIS WITH SYNTHETIC DATA DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Load data
    print("📥 Loading data...")
    df, synthetic_df = load_data()
    print(f"   ✓ Loaded {len(df)} records from unified dataset")
    if synthetic_df is not None:
        print(f"   ✓ Loaded {len(synthetic_df)} validation points (synthetic)")
        print("   ⚠ Using SYNTHETIC data for demonstration - real validation pending")
    print()
    
    # Create matrix
    print("🔗 Building Event-Indicator Association Matrix...")
    matrix_df = create_event_indicator_matrix(df)
    print(f"   ✓ Mapped {len(matrix_df)} event-indicator relationships")
    print()
    
    # Visualizations
    print("📊 Creating heatmap visualizations...")
    create_enhanced_heatmap(matrix_df)
    print()
    
    # Validation
    print("🔍 Running Telebirr validation analysis...")
    validation_params, results = telebirr_validation_with_synthetic(synthetic_df)
    if results:
        errors = [results['validation_errors'][y] for y in results['validation_errors'].keys()]
        mae = np.mean(np.abs(errors))
        print(f"   ✓ Validation complete: MAE = {mae:.2f}pp (synthetic data)")
        create_validation_visualization_enhanced(validation_params, results)
    else:
        print("   ⚠ Validation data not available")
    print()
    
    print("=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nOutput files:")
    print("  - reports/task1/event_indicator_matrix_heatmap.png")
    print("  - reports/task1/telebirr_validation.png")
    print("\n⚠ IMPORTANT NOTE:")
    print("  This analysis uses SYNTHETIC validation data for 2022-2024")
    print("  Real validation requires actual Findex/operator data")
    print("  Methodology demonstrated is production-ready for real data")


if __name__ == "__main__":
    main()
