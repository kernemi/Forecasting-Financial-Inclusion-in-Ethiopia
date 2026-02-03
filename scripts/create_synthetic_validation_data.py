"""
Create Synthetic Validation Data for Telebirr Impact Analysis
==============================================================

Since actual mobile money account ownership data for 2022-2024 is limited,
this script creates a synthetic validation dataset based on:
1. Known baseline (2021 data)
2. Industry reports (Telebirr 54M users by 2024)
3. Kenya M-Pesa growth patterns
4. Economic theory (S-curve adoption)

This synthetic data is CLEARLY LABELED and used solely for demonstrating
the validation methodology that would be applied when real data becomes available.
"""

import pandas as pd
import numpy as np

# Create synthetic but realistic validation data
synthetic_data = {
    'fiscal_year': [2021, 2022, 2023, 2024],
    'mobile_money_account_pct': [
        16.0,  # Baseline (approximate from data)
        22.5,  # +6.5pp (rapid initial adoption)
        28.8,  # +12.8pp cumulative (network effects kicking in)
        34.2   # +18.2pp cumulative (approaching saturation)
    ],
    'telebirr_users_millions': [
        5.0,   # Launch year (partial)
        28.0,  # Rapid growth
        42.0,  # Continued expansion
        54.0   # Reported 2024 figure
    ],
    'data_source': [
        'Findex 2021 (actual)',
        'Synthetic (based on Telebirr reports + Kenya M-Pesa pattern)',
        'Synthetic (interpolated)',
        'Synthetic (Telebirr 54M users reported, ownership estimated)'
    ]
}

df = pd.DataFrame(synthetic_data)

# Save for use in validation
df.to_csv('data/processed/mobile_money_synthetic_validation.csv', index=False)

print("✓ Synthetic validation data created")
print("\nData preview:")
print(df.to_string(index=False))
print("\n⚠ WARNING: This data is SYNTHETIC for demonstration purposes")
print("Real validation should use actual survey/administrative data")
