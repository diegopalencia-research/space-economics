#!/usr/bin/env python3
"""
SYNTHETIC LAUNCH DATA GENERATOR
Based on real-world distributions from 1957-2024
Use this if Kaggle download fails
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

ORGANISATIONS = {
    'SpaceX': {'type': 'Commercial', 'country': 'USA', 'founded': 2002, 'start_year': 2010, 'share': 0.25},
    'CASC': {'type': 'State-Owned', 'country': 'CHN', 'founded': 1999, 'start_year': 1970, 'share': 0.20},
    'Roscosmos': {'type': 'Government', 'country': 'RUS', 'founded': 1992, 'start_year': 1957, 'share': 0.12},
    'ULA': {'type': 'Commercial', 'country': 'USA', 'founded': 2006, 'start_year': 2006, 'share': 0.08},
    'Arianespace': {'type': 'Commercial', 'country': 'FRA', 'founded': 1980, 'start_year': 1979, 'share': 0.07},
    'ISRO': {'type': 'Government', 'country': 'IND', 'founded': 1969, 'start_year': 1979, 'share': 0.06},
    'JAXA': {'type': 'Government', 'country': 'JPN', 'founded': 2003, 'start_year': 1975, 'share': 0.04},
    'Rocket Lab': {'type': 'Commercial', 'country': 'USA', 'founded': 2006, 'start_year': 2017, 'share': 0.04},
    'Northrop': {'type': 'Commercial', 'country': 'USA', 'founded': 2015, 'start_year': 1990, 'share': 0.03},
    'Blue Origin': {'type': 'Commercial', 'country': 'USA', 'founded': 2000, 'start_year': 2015, 'share': 0.02},
    'VKS RF': {'type': 'Government', 'country': 'RUS', 'founded': 1992, 'start_year': 1957, 'share': 0.05},
    'MHI': {'type': 'Commercial', 'country': 'JPN', 'founded': 1921, 'start_year': 1975, 'share': 0.03},
    'Other': {'type': 'Other', 'country': 'Various', 'founded': 1960, 'start_year': 1957, 'share': 0.01}
}

ROCKET_FAMILIES = {
    'SpaceX': ['Falcon 9', 'Falcon Heavy'],
    'CASC': ['Long March 2', 'Long March 3', 'Long March 4', 'Long March 5', 'Long March 11'],
    'Roscosmos': ['Soyuz', 'Proton', 'Angara'],
    'ULA': ['Atlas V', 'Delta IV', 'Vulcan'],
    'Arianespace': ['Ariane 5', 'Ariane 6', 'Vega'],
    'ISRO': ['PSLV', 'GSLV', 'LVM3'],
    'JAXA': ['H-IIA', 'H3', 'Epsilon'],
    'Rocket Lab': ['Electron'],
    'Northrop': ['Antares', 'Minotaur', 'Pegasus'],
    'Blue Origin': ['New Shepard', 'New Glenn'],
    'VKS RF': ['Soyuz-2', 'Rokot'],
    'MHI': ['H-IIA', 'H3'],
    'Other': ['Various']
}

ORBITS = ['LEO (General)', 'LEO (ISS)', 'LEO (Constellation)', 'SSO', 'MEO', 'GEO', 'TLI/Deep Space', 'Suborbital']

LOCATIONS = {
    'USA': ['Cape Canaveral, FL', 'Kennedy Space Center, FL', 'Vandenberg AFB, CA', 'Wallops, VA', 'Boca Chica, TX'],
    'CHN': ['Jiuquan', 'Taiyuan', 'Xichang', 'Wenchang'],
    'RUS': ['Baikonur Cosmodrome', 'Plesetsk Cosmodrome', 'Vostochny Cosmodrome'],
    'FRA': ['Kourou, Guiana Space Centre'],
    'IND': ['Satish Dhawan Space Centre'],
    'JPN': ['Tanegashima Space Center', 'Uchinoura Space Center']
}

def generate_launch_record(year, org):
    info = ORGANISATIONS[org]

    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    date_obj = datetime(year, month, day, hour, minute)
    date_str = date_obj.strftime('%a %b %d, %Y %H:%M UTC')

    rocket = random.choice(ROCKET_FAMILIES[org])
    mission_types = ['Communications', 'Navigation', 'Earth Observation', 'Technology Demo', 
                     'Crewed', 'Cargo Resupply', 'Scientific', 'Reconnaissance']
    mission = random.choice(mission_types)
    detail = f"{rocket} | {mission} Mission"

    country = info['country']
    location = random.choice(LOCATIONS.get(country, ['Unknown Launch Site']))

    if year < 1960:
        orbit = 'Suborbital'
    elif org == 'SpaceX' and year > 2019 and random.random() < 0.6:
        orbit = 'LEO (Constellation)'
    elif org in ['Arianespace', 'ULA'] and random.random() < 0.4:
        orbit = 'GEO'
    else:
        orbit = random.choices(ORBITS, weights=[30, 15, 20, 15, 5, 10, 3, 2])[0]

    base_cost = {
        'SpaceX': 50, 'CASC': 70, 'Roscosmos': 80, 'ULA': 150,
        'Arianespace': 120, 'ISRO': 35, 'JAXA': 90, 'Rocket Lab': 7,
        'Northrop': 60, 'Blue Origin': 0, 'VKS RF': 70, 'MHI': 90, 'Other': 50
    }

    cost = base_cost.get(org, 50)
    cost = cost * (1 + (year - 2000) * 0.02) * random.uniform(0.7, 1.3)
    if org == 'SpaceX' and 'Block 5' in detail:
        cost *= random.uniform(0.5, 0.8)
    if orbit == 'GEO':
        cost *= 1.5

    if year < 1965:
        success_prob = 0.60
    elif year < 1980:
        success_prob = 0.85
    elif year < 2000:
        success_prob = 0.92
    else:
        success_prob = 0.95

    if org == 'SpaceX' and year < 2016:
        success_prob -= 0.10
    elif org == 'Rocket Lab' and year < 2020:
        success_prob -= 0.15

    success = random.random() < success_prob
    status = 'Success' if success else random.choice(['Failure', 'Partial Failure'])
    rocket_status = 'StatusActive' if year > info['founded'] + 5 else 'StatusRetired'

    return {
        'organisation': org,
        'location': location,
        'datum': date_str,
        'detail': detail,
        'status_rocket': rocket_status,
        'rocket_cost': f"${cost:.1f} million" if cost > 0 else "Unknown",
        'status_mission': status,
        'year_launch': year,
        'month_launch': month,
        'org_type': info['type'],
        'org_country': info['country'],
        'rocket_family': rocket,
        'orbit_class': orbit,
        'cost_million': round(cost, 2) if cost > 0 else None,
        'success_flag': 1 if success else 0,
        'status_clean': status
    }

# Generate 4,500 records
records = []
for year in range(1957, 2025):
    if year < 1960:
        n = random.randint(5, 15)
    elif year < 1970:
        n = random.randint(60, 100)
    elif year < 1980:
        n = random.randint(80, 130)
    elif year < 1990:
        n = random.randint(90, 140)
    elif year < 2000:
        n = random.randint(70, 110)
    elif year < 2010:
        n = random.randint(60, 80)
    else:
        n = random.randint(80, 200)

    providers = list(ORGANISATIONS.keys())
    weights = [ORGANISATIONS[p]['share'] for p in providers]

    for _ in range(n):
        org = random.choices(providers, weights=weights)[0]
        if year < ORGANISATIONS[org]['start_year']:
            org = 'Roscosmos'
        records.append(generate_launch_record(year, org))

df = pd.DataFrame(records)
df.to_csv('data/raw/Space_Corrected.csv', index=False)
print(f"Generated {len(df)} synthetic launch records")
print(f"Date range: {df['year_launch'].min()} - {df['year_launch'].max()}")
print(f"Success rate: {df['success_flag'].mean():.1%}")
print(f"Organisations: {df['organisation'].nunique()}")
