#!/usr/bin/env python3
"""
SACRED GEOMETRY VISUALIZATION SYSTEM
Evidence System v1.0 | Aerospace Portfolio
Golden Ratio · Minimal · Scientific · Premium
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge
import numpy as np
import pandas as pd
import sqlite3
from matplotlib import font_manager as fm

# ============================================================
# SACRED GEOMETRY CONSTANTS
# ============================================================

PHI = 1.618033988749895
BASE_COLOR = '#0A0E17'
GOLD = '#C9A96E'
EARTH = '#4A6741'
COOL_GRAY = '#8B9DAF'
WHITE = '#F0F0F0'

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Cinzel', 'Cormorant Garamond', 'Georgia', 'serif']
plt.rcParams['axes.facecolor'] = BASE_COLOR
plt.rcParams['figure.facecolor'] = BASE_COLOR
plt.rcParams['text.color'] = WHITE
plt.rcParams['axes.labelcolor'] = COOL_GRAY
plt.rcParams['xtick.color'] = COOL_GRAY
plt.rcParams['ytick.color'] = COOL_GRAY

# ============================================================
# FIGURE 1: GOLDEN RATIO TIMELINE
# ============================================================

def create_golden_timeline(df):
    yearly = df.groupby('year_launch').agg({
        'organisation': 'count',
        'success_flag': 'sum',
        'cost_million': 'mean'
    }).reset_index()
    yearly.columns = ['year', 'launches', 'successes', 'avg_cost']
    yearly['reliability'] = yearly['successes'] / yearly['launches']
    yearly = yearly[(yearly['year'] >= 1957) & (yearly['year'] <= 2024)]

    width = 13
    height = width / PHI

    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor(BASE_COLOR)
    ax.set_facecolor(BASE_COLOR)

    ax.set_xlim(1955, 2026)
    ax.set_ylim(0, yearly['launches'].max() * 1.15)

    ax.grid(True, alpha=0.15, color=GOLD, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color(GOLD)
        spine.set_linewidth(0.5)
        spine.set_alpha(0.3)

    ax.fill_between(yearly['year'], yearly['launches'], alpha=0.15, color=EARTH)
    ax.plot(yearly['year'], yearly['launches'], color=GOLD, linewidth=1.5, alpha=0.9)

    sizes = (yearly['reliability'] * 100) ** 1.5
    ax.scatter(yearly['year'], yearly['launches'], 
               s=sizes, c=yearly['reliability'], cmap='YlGn', 
               alpha=0.8, edgecolors=GOLD, linewidth=0.5, zorder=5)

    ax.annotate('Sputnik\n1957', xy=(1957, yearly[yearly['year']==1957]['launches'].values[0]),
                xytext=(1960, 80), fontsize=8, color=COOL_GRAY,
                arrowprops=dict(arrowstyle='->', color=COOL_GRAY, alpha=0.5))

    ax.annotate('SpaceX\nFirst Landing\n2015', xy=(2015, yearly[yearly['year']==2015]['launches'].values[0]),
                xytext=(2005, 100), fontsize=8, color=GOLD,
                arrowprops=dict(arrowstyle='->', color=GOLD, alpha=0.7))

    ax.set_title('ORBITAL ECONOMY EXPANSION\n1957-2024', 
                 fontsize=16, fontweight='bold', color=GOLD, pad=20, loc='left')

    ax.set_xlabel('Year', fontsize=10, color=COOL_GRAY)
    ax.set_ylabel('Launch Attempts', fontsize=10, color=COOL_GRAY)

    cbar = plt.colorbar(ax.collections[1], ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label('Reliability', color=COOL_GRAY, fontsize=9)
    cbar.ax.yaxis.set_tick_params(color=COOL_GRAY)

    plt.tight_layout()
    plt.savefig('figures/01_golden_timeline.png', dpi=300, bbox_inches='tight',
                facecolor=BASE_COLOR, edgecolor='none')
    plt.close()

    print("Golden Timeline saved")

# ============================================================
# FIGURE 2: VESICA PISCIS RELIABILITY
# ============================================================

def create_vesica_reliability(df):
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor(BASE_COLOR)
    ax.set_facecolor(BASE_COLOR)

    spacex = df[df['organisation'] == 'SpaceX']
    industry = df[(df['organisation'] != 'SpaceX') & (df['year_launch'] >= 2010)]

    spx_rel = spacex['success_flag'].mean() if len(spacex) > 0 else 0
    ind_rel = industry['success_flag'].mean() if len(industry) > 0 else 0
    spx_cost = spacex['cost_million'].median()
    ind_cost = industry['cost_million'].median()

    r = 3
    d = r * 0.618

    circle1 = Circle((-d/2, 0), r, fill=True, facecolor=EARTH, alpha=0.2, edgecolor=EARTH, linewidth=2)
    ax.add_patch(circle1)

    circle2 = Circle((d/2, 0), r, fill=True, facecolor=GOLD, alpha=0.2, edgecolor=GOLD, linewidth=2)
    ax.add_patch(circle2)

    ax.text(-d/2 - 1, 0, f'INDUSTRY\n{ind_rel:.1%}\nReliability\n${ind_cost:.0f}M\nMedian Cost',
            ha='center', va='center', fontsize=11, color=EARTH, fontweight='bold')

    ax.text(d/2 + 1, 0, f'SPACEX\n{spx_rel:.1%}\nReliability\n${spx_cost:.0f}M\nMedian Cost',
            ha='center', va='center', fontsize=11, color=GOLD, fontweight='bold')

    ax.text(0, 0, 'COST-\nEFFICIENCY\nFRONTIER', 
            ha='center', va='center', fontsize=9, color=WHITE, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=BASE_COLOR, edgecolor=GOLD, alpha=0.9))

    ax.set_xlim(-6, 6)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.set_title('THE RELIABILITY INTERSECTION\nProvider Comparison 2010-2024', 
                 fontsize=14, color=GOLD, pad=20)

    plt.tight_layout()
    plt.savefig('figures/02_vesica_reliability.png', dpi=300, bbox_inches='tight',
                facecolor=BASE_COLOR, edgecolor='none')
    plt.close()

    print("Vesica Piscis Reliability saved")

# ============================================================
# FIGURE 3: FIBONACCI SPIRAL MARKET SHARE
# ============================================================

def create_fibonacci_market(df):
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor(BASE_COLOR)

    recent = df[df['year_launch'] >= 2018]
    providers = recent['organisation'].value_counts().head(8)

    theta = np.linspace(0, 4*np.pi, 1000)
    a = 0.1
    b = 0.306
    r = a * np.exp(b * theta)

    ax.plot(theta, r, color=GOLD, alpha=0.2, linewidth=0.5)

    colors = [GOLD, EARTH, COOL_GRAY, '#5B7C99', '#7A6B4D', '#4A5568', '#6B5B3D', '#3D5A6C']

    angles = np.cumsum([0] + list(providers.values / providers.sum() * 2 * np.pi))

    for i, (provider, count) in enumerate(providers.items()):
        theta_start = angles[i]
        theta_end = angles[i+1]
        theta_sector = np.linspace(theta_start, theta_end, 50)
        r_sector = np.linspace(0.5, providers[provider] / providers.max() * 4, 50)

        ax.fill_between(theta_sector, 0, r_sector[-1], alpha=0.7, color=colors[i])
        ax.plot([theta_start, theta_start], [0, 5], color=BASE_COLOR, linewidth=1)

        mid_angle = (theta_start + theta_end) / 2
        ax.text(mid_angle, r_sector[-1] + 0.5, f'{provider}\n{count}', 
                ha='center', va='center', fontsize=8, color=WHITE)

    ax.set_ylim(0, 6)
    ax.set_facecolor(BASE_COLOR)
    ax.grid(color=GOLD, alpha=0.1)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    ax.set_title('ORBITAL MARKET DYNAMICS\nLaunch Share 2018-2024 (Fibonacci Proportions)', 
                 fontsize=12, color=GOLD, pad=30, y=1.08)

    plt.tight_layout()
    plt.savefig('figures/03_fibonacci_market.png', dpi=300, bbox_inches='tight',
                facecolor=BASE_COLOR, edgecolor='none')
    plt.close()

    print("Fibonacci Market Spiral saved")

# ============================================================
# FIGURE 4: COST EFFICIENCY SACRED GRID
# ============================================================

def create_cost_efficiency_grid(df):
    fig, ax = plt.subplots(figsize=(13, 8))
    fig.patch.set_facecolor(BASE_COLOR)
    ax.set_facecolor(BASE_COLOR)

    modern = df[(df['year_launch'] >= 2015) & (df['cost_million'].notna())]

    margin_x = (modern['cost_million'].max() - modern['cost_million'].min()) * 0.05
    margin_y = 0.05

    ax.set_xlim(modern['cost_million'].min() - margin_x, 
                modern['cost_million'].max() + margin_x)
    ax.set_ylim(-margin_y, 1 + margin_y)

    ax.axhline(y=0.618, color=GOLD, linestyle='--', alpha=0.3, linewidth=0.8)
    ax.axhline(y=0.382, color=GOLD, linestyle='--', alpha=0.3, linewidth=0.8)

    for org_type, color in [('Commercial', GOLD), ('Government', COOL_GRAY), ('State-Owned', EARTH)]:
        subset = modern[modern['org_type'] == org_type]
        ax.scatter(subset['cost_million'], subset['success_flag'], 
                alpha=0.4, s=60, c=color, label=org_type, edgecolors='none')

    try:
        from scipy import stats
        z = np.polyfit(modern['cost_million'], modern['success_flag'], 3)
        p = np.poly1d(z)
        x_line = np.linspace(modern['cost_million'].min(), modern['cost_million'].max(), 200)
        ax.plot(x_line, np.clip(p(x_line), 0, 1), color=GOLD, linewidth=2, alpha=0.7, linestyle='--')
    except ImportError:
        pass

    ax.set_xlabel('Mission Cost ($M)', fontsize=11, color=COOL_GRAY)
    ax.set_ylabel('Mission Success (1=Success, 0=Failure)', fontsize=11, color=COOL_GRAY)
    ax.set_title('COST-EFFICIENCY FRONTIER\nDoes Higher Cost Buy Reliability?', 
                 fontsize=14, color=GOLD, pad=20, loc='left')

    ax.legend(loc='lower right', framealpha=0.1, facecolor=BASE_COLOR, 
              edgecolor=GOLD, labelcolor=WHITE)

    for spine in ax.spines.values():
        spine.set_color(GOLD)
        spine.set_alpha(0.3)

    plt.tight_layout()
    plt.savefig('figures/04_cost_efficiency.png', dpi=300, bbox_inches='tight',
                facecolor=BASE_COLOR, edgecolor='none')
    plt.close()

    print("Cost Efficiency Grid saved")

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == '__main__':
    import os
    os.makedirs('figures', exist_ok=True)

    df = pd.read_csv('data/clean/launches_clean.csv')
    print(f"Loaded {len(df)} launches")

    create_golden_timeline(df)
    create_vesica_reliability(df)
    create_fibonacci_market(df)
    create_cost_efficiency_grid(df)

    print("\nAll sacred geometry visualizations complete")
    print("Portfolio evidence generated")
