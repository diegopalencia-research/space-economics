#!/usr/bin/env python3
"""
STREAMLIT EVIDENCE DASHBOARD
Launch Economics & Reliability Intelligence
Sacred Geometry · Aerospace · Minimal · Premium
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ============================================================
# SACRED GEOMETRY THEME CONFIG
# ============================================================

st.set_page_config(
    page_title="Launch Economics Intelligence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    .main {
        background-color: #0A0E17;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: #C9A96E !important;
        letter-spacing: 0.05em;
    }

    .stMetric {
        background-color: rgba(201, 169, 110, 0.05);
        border: 1px solid rgba(201, 169, 110, 0.2);
        border-radius: 8px;
        padding: 1rem;
    }

    .stMetric label {
        color: #8B9DAF !important;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .stMetric .css-1xarl3l {
        color: #C9A96E !important;
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
    }

    div[data-testid="stMarkdownContainer"] p {
        font-family: 'Inter', sans-serif;
        color: #F0F0F0;
    }

    .css-1d391kg, .css-1lcbmhc {
        background-color: #0A0E17;
    }

    .stSelectbox label, .stSlider label {
        color: #8B9DAF !important;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.7rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv('data/clean/launches_clean.csv')
    return df

df = load_data()

# ============================================================
# HEADER
# ============================================================

col_title, col_logo = st.columns([3, 1])

with col_title:
    st.markdown("""
    <h1 style='font-size: 2.5rem; margin-bottom: 0;'>LAUNCH ECONOMICS</h1>
    <p style='color: #8B9DAF; font-family: Inter; font-size: 0.9rem; letter-spacing: 0.15em; margin-top: 0.5rem;'>
        RELIABILITY INTELLIGENCE · EVIDENCE SYSTEM v1.0
    </p>
    """, unsafe_allow_html=True)

with col_logo:
    st.markdown("""
    <div style='text-align: right;'>
        <svg width="80" height="80" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="none" stroke="#C9A96E" stroke-width="0.5" opacity="0.6"/>
            <circle cx="50" cy="50" r="30" fill="none" stroke="#C9A96E" stroke-width="0.5" opacity="0.4"/>
            <circle cx="50" cy="50" r="15" fill="none" stroke="#C9A96E" stroke-width="0.5" opacity="0.3"/>
            <line x1="50" y1="5" x2="50" y2="95" stroke="#C9A96E" stroke-width="0.3" opacity="0.3"/>
            <line x1="5" y1="50" x2="95" y2="50" stroke="#C9A96E" stroke-width="0.3" opacity="0.3"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# FILTERS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    year_range = st.slider("ERA", 1957, 2024, (2010, 2024))

with col2:
    orbit_filter = st.selectbox("ORBIT CLASS", 
                                ['All'] + sorted(df['orbit_class'].dropna().unique().tolist()))

with col3:
    org_filter = st.selectbox("PROVIDER", 
                              ['All'] + sorted(df['organisation'].dropna().unique().tolist()))

with col4:
    status_filter = st.selectbox("MISSION STATUS", 
                                   ['All', 'Success', 'Failure', 'Partial Failure'])

# Apply filters
filtered = df[(df['year_launch'] >= year_range[0]) & (df['year_launch'] <= year_range[1])]

if orbit_filter != 'All':
    filtered = filtered[filtered['orbit_class'] == orbit_filter]
if org_filter != 'All':
    filtered = filtered[filtered['organisation'] == org_filter]
if status_filter != 'All':
    filtered = filtered[filtered['status_clean'] == status_filter]

# ============================================================
# KPI CARDS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns([1, 1, 1, 1, 1])

with kpi1:
    st.metric("TOTAL LAUNCHES", f"{len(filtered):,}")
with kpi2:
    st.metric("RELIABILITY", f"{filtered['success_flag'].mean():.1%}")
with kpi3:
    avg_cost = filtered['cost_million'].median()
    st.metric("MEDIAN COST", f"${avg_cost:.1f}M" if not pd.isna(avg_cost) else "N/A")
with kpi4:
    st.metric("ACTIVE PROVIDERS", f"{filtered['organisation'].nunique()}")
with kpi5:
    top_org = filtered['organisation'].value_counts().index[0] if len(filtered) > 0 else "N/A"
    st.metric("MARKET LEADER", top_org)

st.markdown("---")

# ============================================================
# MAIN VISUALIZATIONS
# ============================================================

tab1, tab2, tab3 = st.tabs(["📊 TIMELINE", "🎯 PROVIDER INTELLIGENCE", "💰 COST ANALYSIS"])

# ----------------------------------------------------------
# TAB 1: TIMELINE
# ----------------------------------------------------------
with tab1:
    col_left, col_right = st.columns([2, 1])

    with col_left:
        yearly = filtered.groupby('year_launch').agg({
            'organisation': 'count',
            'success_flag': 'sum'
        }).reset_index()
        yearly.columns = ['Year', 'Launches', 'Successes']
        yearly['Reliability'] = yearly['Successes'] / yearly['Launches']

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=yearly['Year'], y=yearly['Launches'],
            fill='tozeroy', fillcolor='rgba(74, 103, 65, 0.15)',
            line=dict(color='#C9A96E', width=1.5),
            name='Launch Volume'
        ))

        fig.add_trace(go.Scatter(
            x=yearly['Year'], y=yearly['Reliability'] * yearly['Launches'].max(),
            mode='lines', line=dict(color='#8B9DAF', width=1, dash='dot'),
            name='Reliability (scaled)'
        ))

        fig.update_layout(
            plot_bgcolor='#0A0E17',
            paper_bgcolor='#0A0E17',
            font=dict(family='Inter', color='#F0F0F0'),
            xaxis=dict(gridcolor='rgba(201, 169, 110, 0.1)', showline=True, linecolor='#C9A96E'),
            yaxis=dict(gridcolor='rgba(201, 169, 110, 0.1)', showline=True, linecolor='#C9A96E'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                       bgcolor='rgba(10, 14, 23, 0.8)', bordercolor='#C9A96E', borderwidth=0.5),
            margin=dict(l=60, r=40, t=80, b=60),
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("""
        <h3 style='font-size: 1rem;'>ORBITAL INSIGHT</h3>
        <p style='color: #8B9DAF; font-size: 0.85rem; line-height: 1.6;'>
            The launch economy exhibits two distinct regimes: 
            <span style='color: #C9A96E;'>pre-2015</span> government-led 
            periodicity and <span style='color: #C9A96E;'>post-2015</span> 
            commercial exponential growth. SpaceX's reusability paradigm 
            shifted the cost structure from linear to logarithmic decay.
        </p>
        <br>
        <h3 style='font-size: 1rem;'>KEY SIGNAL</h3>
        <p style='color: #8B9DAF; font-size: 0.85rem; line-height: 1.6;'>
            Reliability and launch cadence are now <em>inversely correlated</em> 
            with cost — a reversal of the 1960s-2000s pattern where higher 
            expenditure predicted success.
        </p>
        """, unsafe_allow_html=True)

# ----------------------------------------------------------
# TAB 2: PROVIDER INTELLIGENCE
# ----------------------------------------------------------
with tab2:
    col_a, col_b = st.columns([1, 1])

    with col_a:
        provider_stats = filtered.groupby('organisation').agg({
            'success_flag': ['count', 'sum', 'mean'],
            'cost_million': 'median'
        }).reset_index()
        provider_stats.columns = ['Provider', 'Total', 'Successes', 'Reliability', 'MedianCost']
        provider_stats = provider_stats[provider_stats['Total'] >= 3]
        provider_stats = provider_stats.sort_values('Reliability', ascending=True)

        fig = go.Figure(go.Bar(
            y=provider_stats['Provider'],
            x=provider_stats['Reliability'],
            orientation='h',
            marker=dict(
                color=provider_stats['Reliability'],
                colorscale=[[0, '#4A6741'], [0.5, '#8B9DAF'], [1, '#C9A96E']],
                showscale=False
            ),
            text=[f"{r:.1%}" for r in provider_stats['Reliability']],
            textposition='outside',
            textfont=dict(color='#F0F0F0', size=10)
        ))

        fig.update_layout(
            plot_bgcolor='#0A0E17', paper_bgcolor='#0A0E17',
            font=dict(family='Inter', color='#F0F0F0'),
            xaxis=dict(gridcolor='rgba(201, 169, 110, 0.1)', tickformat='.0%'),
            yaxis=dict(gridcolor='rgba(201, 169, 110, 0.1)'),
            margin=dict(l=120, r=40, t=60, b=60),
            height=400,
            title=dict(text='RELIABILITY BY PROVIDER (min. 3 launches)', font=dict(size=12, color='#C9A96E'))
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        orbit_stats = filtered.groupby(['orbit_class', 'status_clean']).size().unstack(fill_value=0)

        fig = go.Figure()

        for status in orbit_stats.columns:
            color = '#C9A96E' if status == 'Success' else '#4A6741' if status == 'Partial Failure' else '#8B9DAF'
            fig.add_trace(go.Bar(
                name=status,
                x=orbit_stats.index,
                y=orbit_stats[status],
                marker_color=color,
                opacity=0.85
            ))

        fig.update_layout(
            barmode='stack',
            plot_bgcolor='#0A0E17', paper_bgcolor='#0A0E17',
            font=dict(family='Inter', color='#F0F0F0'),
            xaxis=dict(gridcolor='rgba(201, 169, 110, 0.1)'),
            yaxis=dict(gridcolor='rgba(201, 169, 110, 0.1)'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02,
                       bgcolor='rgba(10, 14, 23, 0.8)', bordercolor='#C9A96E'),
            margin=dict(l=60, r=40, t=80, b=60),
            height=400,
            title=dict(text='OUTCOME DISTRIBUTION BY ORBIT', font=dict(size=12, color='#C9A96E'))
        )

        st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# TAB 3: COST ANALYSIS
# ----------------------------------------------------------
with tab3:
    st.markdown("""
    <h3 style='font-size: 1.2rem; margin-bottom: 1rem;'>COST-EFFICIENCY FRONTIER</h3>
    """, unsafe_allow_html=True)

    cost_data = filtered[(filtered['cost_million'].notna()) & (filtered['year_launch'] >= 2015)]

    fig = px.scatter(
        cost_data,
        x='cost_million',
        y='success_flag',
        color='org_type',
        size='year_launch',
        hover_data=['organisation', 'rocket_family', 'orbit_class'],
        color_discrete_map={
            'Commercial': '#C9A96E',
            'Government': '#8B9DAF',
            'State-Owned': '#4A6741'
        },
        opacity=0.6
    )

    fig.update_layout(
        plot_bgcolor='#0A0E17', paper_bgcolor='#0A0E17',
        font=dict(family='Inter', color='#F0F0F0'),
        xaxis=dict(gridcolor='rgba(201, 169, 110, 0.1)', title='Mission Cost ($M)'),
        yaxis=dict(gridcolor='rgba(201, 169, 110, 0.1)', title='Success', tickformat='.0%'),
        legend=dict(title='Provider Type', bgcolor='rgba(10, 14, 23, 0.8)', bordercolor='#C9A96E'),
        margin=dict(l=60, r=40, t=60, b=60),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <p style='color: #8B9DAF; font-size: 0.85rem; margin-top: 1rem;'>
        <strong>INTERPRETATION:</strong> Each point is a mission. Size indicates recency. 
        The frontier shows that commercial providers (gold) now cluster in the 
        high-reliability, low-cost quadrant — a structural shift from the 
        government-era pattern where cost and reliability were positively correlated.
    </p>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #8B9DAF; font-family: Inter; font-size: 0.75rem; letter-spacing: 0.1em;'>
    EVIDENCE SYSTEM v1.0 · AEROSPACE PORTFOLIO · BUILT WITH SACRED GEOMETRY PRINCIPLES<br>
    DATA: JONATHAN MCDOWELL / NEXTSPACEFLIGHT · ANALYSIS: PROTOCOL DICE™
</p>
""", unsafe_allow_html=True)
