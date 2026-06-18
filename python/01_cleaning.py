#!/usr/bin/env python3
"""
LAUNCH ECONOMICS CLEANING PIPELINE
Evidence System v1.0 | Aerospace Portfolio
"""

import pandas as pd
import sqlite3
import re
from datetime import datetime
import numpy as np

# ============================================================
# 1. LOAD RAW DATA
# ============================================================

df = pd.read_csv('data/raw/Space_Corrected.csv')

print(f"Raw shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# ============================================================
# 2. STANDARDIZE COLUMN NAMES
# ============================================================

df.columns = ['id', 'organisation', 'location', 'datum', 'detail', 
              'status_rocket', 'rocket_cost', 'status_mission']

# ============================================================
# 3. PARSE DATES
# ============================================================

def parse_space_date(date_str):
    """
    Handles formats like:
    - "Fri Aug 07, 2020 05:12 UTC"
    - "Thu Aug 06, 2020"
    - "Tue Dec 26, 2017 19:00 UTC"
    """
    if pd.isna(date_str):
        return None

    date_str = re.sub(r'^[A-Za-z]{3}\s+', '', str(date_str))

    patterns = [
        '%b %d, %Y %H:%M UTC',
        '%b %d, %Y %H:%M:%S UTC',
        '%b %d, %Y',
    ]

    for pattern in patterns:
        try:
            return datetime.strptime(date_str.strip(), pattern)
        except ValueError:
            continue

    return None

df['parsed_date'] = df['datum'].apply(parse_space_date)
df['year_launch'] = df['parsed_date'].dt.year
df['month_launch'] = df['parsed_date'].dt.month

# ============================================================
# 4. CLEAN COSTS
# ============================================================

def extract_cost(cost_str):
    """
    Extract numeric cost in millions from strings like:
    - "50.0" -> 50.0
    - "$50.0 million" -> 50.0
    - "Unknown" -> NULL
    """
    if pd.isna(cost_str) or str(cost_str).lower() in ['unknown', 'nan', '']:
        return np.nan

    numbers = re.findall(r'[\d.]+', str(cost_str))
    if numbers:
        val = float(numbers[0])
        if val > 10000:
            return val / 1000
        return val
    return np.nan

df['cost_million'] = df['rocket_cost'].apply(extract_cost)

# ============================================================
# 5. CLASSIFY ORGANISATIONS
# ============================================================

ORGANISATION_MAP = {
    'SpaceX': {'type': 'Commercial', 'country': 'USA', 'founded': 2002},
    'CASC': {'type': 'State-Owned', 'country': 'CHN', 'founded': 1999},
    'Roscosmos': {'type': 'Government', 'country': 'RUS', 'founded': 1992},
    'ULA': {'type': 'Commercial', 'country': 'USA', 'founded': 2006},
    'Arianespace': {'type': 'Commercial', 'country': 'FRA', 'founded': 1980},
    'NASA': {'type': 'Government', 'country': 'USA', 'founded': 1958},
    'ISRO': {'type': 'Government', 'country': 'IND', 'founded': 1969},
    'JAXA': {'type': 'Government', 'country': 'JPN', 'founded': 2003},
    'Northrop': {'type': 'Commercial', 'country': 'USA', 'founded': 2015},
    'Rocket Lab': {'type': 'Commercial', 'country': 'USA', 'founded': 2006},
    'Blue Origin': {'type': 'Commercial', 'country': 'USA', 'founded': 2000},
    'VKS RF': {'type': 'Government', 'country': 'RUS', 'founded': 1992},
    'MHI': {'type': 'Commercial', 'country': 'JPN', 'founded': 1921},
}

def classify_org(name):
    if pd.isna(name):
        return 'Unknown', 'Unknown', None

    for key, info in ORGANISATION_MAP.items():
        if key.lower() in str(name).lower():
            return info['type'], info['country'], info['founded']

    return 'Other', 'Unknown', None

df[['org_type', 'org_country', 'org_founded']] = df['organisation'].apply(
    lambda x: pd.Series(classify_org(x))
)

# ============================================================
# 6. EXTRACT ROCKET FAMILY
# ============================================================

def extract_rocket_family(detail_str):
    if pd.isna(detail_str):
        return 'Unknown'

    detail = str(detail_str)

    if 'Falcon' in detail:
        if 'Falcon 9' in detail:
            return 'Falcon 9'
        elif 'Falcon Heavy' in detail:
            return 'Falcon Heavy'
        return 'Falcon'

    if 'Soyuz' in detail:
        return 'Soyuz'

    if 'Long March' in detail or 'Chang Zheng' in detail:
        return 'Long March'

    if 'Ariane' in detail:
        return 'Ariane'

    if 'Atlas' in detail:
        return 'Atlas'

    if 'Delta' in detail:
        return 'Delta'

    if 'Proton' in detail:
        return 'Proton'

    if 'Electron' in detail:
        return 'Electron'

    if 'PSLV' in detail or 'GSLV' in detail:
        return 'ISRO LV'

    if 'H-II' in detail:
        return 'H-II'

    if 'Antares' in detail:
        return 'Antares'

    return 'Other'

df['rocket_family'] = df['detail'].apply(extract_rocket_family)

# ============================================================
# 7. INFER ORBIT CLASS
# ============================================================

def infer_orbit(detail_str, location_str):
    detail = str(detail_str).upper() if not pd.isna(detail_str) else ''
    location = str(location_str).upper() if not pd.isna(location_str) else ''

    if any(x in detail for x in ['GEO', 'GEOSTATIONARY', 'INTELSAT', 'INMARSAT', 'EUTELSAT', 'SES', 'HISPASAT']):
        return 'GEO'

    if any(x in detail for x in ['ISS', 'CREW DRAGON', 'SOYUZ MS', 'PROGRESS', 'CYGNUS', 'CRS']):
        return 'LEO (ISS)'

    if any(x in detail for x in ['SSO', 'POLAR', 'SUN-SYNCHRONOUS', 'FLOCK', 'SKYSAT']):
        return 'SSO'

    if any(x in detail for x in ['GPS', 'GLONASS', 'GALILEO', 'BEIDOU', 'MEO']):
        return 'MEO'

    if any(x in detail for x in ['MOON', 'LUNAR', 'MARS', 'TLI', 'VIKING', 'VOYAGER', 'PIONEER', 'NEW HORIZONS']):
        return 'TLI/Deep Space'

    if any(x in detail for x in ['SUBORBITAL', 'NEW SHEPARD', 'SARGE', '150 METER']):
        return 'Suborbital'

    if 'STARLINK' in detail:
        return 'LEO (Constellation)'

    if 'VANDENBERG' in location:
        return 'SSO'

    return 'LEO (General)'

df['orbit_class'] = df.apply(lambda row: infer_orbit(row['detail'], row['location']), axis=1)

# ============================================================
# 8. CLEAN SUCCESS FLAGS
# ============================================================

def clean_status(status):
    status = str(status).strip().lower()
    if 'success' in status and 'partial' not in status:
        return 'Success', 1, 0
    elif 'partial' in status:
        return 'Partial Failure', 0, 1
    elif 'prelaunch' in status:
        return 'Prelaunch Failure', 0, 0
    else:
        return 'Failure', 0, 0

status_clean = df['status_mission'].apply(clean_status)
df['status_clean'] = [x[0] for x in status_clean]
df['success_flag'] = [x[1] for x in status_clean]
df['partial_flag'] = [x[2] for x in status_clean]

# ============================================================
# 9. SAVE CLEAN DATA
# ============================================================

df.to_csv('data/clean/launches_clean.csv', index=False)
print(f"\nClean data saved: {df.shape}")
print(f"Date range: {df['year_launch'].min()} - {df['year_launch'].max()}")
print(f"Organisations: {df['organisation'].nunique()}")
print(f"Success rate: {df['success_flag'].mean():.1%}")

# ============================================================
# 10. LOAD TO SQLITE
# ============================================================

conn = sqlite3.connect('data/launch_economics.db')

df_sql = df[[
    'organisation', 'org_type', 'org_country', 'org_founded',
    'location', 'year_launch', 'month_launch',
    'rocket_family', 'orbit_class',
    'cost_million', 'success_flag', 'partial_flag', 'status_clean'
]].copy()

df_sql.to_sql('launches', conn, if_exists='replace', index=False)

print(f"\nSQLite database created: launch_economics.db")
print(f"Table 'launches' ready with {len(df_sql)} records")

conn.close()
