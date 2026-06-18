#!/usr/bin/env python3
"""
EXPLORATORY DATA ANALYSIS
Evidence System v1.0 | Aerospace Portfolio
"""

import pandas as pd
import numpy as np
import sqlite3

df = pd.read_csv('data/clean/launches_clean.csv')

print("=" * 60)
print("LAUNCH ECONOMICS EDA")
print("=" * 60)

print(f"\nTotal Records: {len(df):,}")
print(f"Date Range: {df['year_launch'].min():.0f} - {df['year_launch'].max():.0f}")
print(f"Organisations: {df['organisation'].nunique()}")
print(f"Rocket Families: {df['rocket_family'].nunique()}")
print(f"Orbit Classes: {df['orbit_class'].nunique()}")

print("\n--- SUCCESS RATE BY ORGANISATION (min 10 launches) ---")
success_by_org = df.groupby('organisation').agg({
    'success_flag': ['count', 'sum', 'mean']
}).round(3)
success_by_org.columns = ['Total', 'Successes', 'Rate']
success_by_org = success_by_org[success_by_org['Total'] >= 10].sort_values('Rate', ascending=False)
print(success_by_org.head(15))

print("\n--- LAUNCH VOLUME BY DECADE ---")
df['decade'] = (df['year_launch'] // 10) * 10
print(df.groupby('decade')['organisation'].count())

print("\n--- COST DISTRIBUTION ---")
print(df['cost_million'].describe())

print("\n--- ORBIT CLASS BREAKDOWN ---")
print(df['orbit_class'].value_counts())

print("\n--- ROCKET FAMILY (Top 10) ---")
print(df['rocket_family'].value_counts().head(10))

# Save EDA summary
with open('reports/eda_summary.txt', 'w') as f:
    f.write("LAUNCH ECONOMICS EDA SUMMARY\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Total Records: {len(df):,}\n")
    f.write(f"Date Range: {df['year_launch'].min():.0f} - {df['year_launch'].max():.0f}\n")
    f.write(f"Overall Success Rate: {df['success_flag'].mean():.1%}\n")
    f.write(f"Records with Cost Data: {df['cost_million'].notna().sum():,} ({df['cost_million'].notna().mean():.1%})\n")
    f.write("\nTop 5 Providers by Volume:\n")
    f.write(str(df['organisation'].value_counts().head(5)) + "\n")
