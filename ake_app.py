#!/usr/bin/env python
# coding: utf-8

# In[3]:


# app.py → Soil & Water Conservation Programme | FINAL LEGACY VERSION | By Aklilu Abera Dana
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

st.set_page_config(page_title="Soil & Water Conservation", page_icon="leaf", layout="wide", initial_sidebar_state="expanded")

# ================= CLEAN & PROFESSIONAL DESIGN =================
st.markdown("""
<style>
    .main {background:#f8fffa; padding:0 2rem;}
    
    .project-title {
        background:linear-gradient(135deg,#1e4d2b,#2e8b57);
        padding:3.2rem 2rem;
        text-align:center;
        color:white;
        border-radius:0 0 50px 50px;
        margin:-3rem -3rem 6rem -3rem;
        box-shadow:0 25px 70px rgba(0,0,0,0.38);
    }
    .project-title h1 {font-size:5rem; margin:0; font-weight:900; letter-spacing:4px;}
    .project-title p {font-size:1.7rem; margin:14px 0 0; opacity:0.96;}

    .section-title {
        font-size:2.8rem;
        color:#1e4d2b;
        font-weight:900;
        text-align:center;
        margin:6rem 0 4rem;
        padding-bottom:12px;
        border-bottom:6px solid #2e8b57;
        display:inline-block;
        width:auto;
        left:50%;
        transform:translateX(-50%);
        position:relative;
    }

    .chart-container {
        background:white;
        border-radius:28px;
        padding:2.5rem;
        margin:2rem 0;
        box-shadow:0 20px 70px rgba(0,0,0,0.14);
        border:4px solid #2e8b57;
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2.5rem;
        margin: 3rem 0 5rem 0;
    }
    .kpi-item {
        background:white;
        border-radius:26px;
        padding:2.4rem;
        text-align:center;
        box-shadow:0 18px 60px rgba(0,0,0,0.14);
        border:6px solid #2e8b57;
        transition:all 0.4s ease;
    }
    .kpi-item:hover {
        transform:translateY(-14px);
        border-color:#1e4d2b;
        box-shadow:0 45px 110px rgba(46,139,87,0.4);
    }
    .kpi-value {
        font-size:3.6rem;
        font-weight:900;
        color:#1e4d2b;
        margin:0;
    }
    .kpi-label {
        font-size:1.35rem;
        color:#2e8b57;
        font-weight:800;
        margin-top:12px;
        letter-spacing:1.2px;
    }

    .footer {
        background:#1e4d2b;
        color:white;
        text-align:center;
        padding:6rem;
        margin-top:12rem;
        border-radius:60px;
        font-size:1.6rem;
    }
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("""
<div class="project-title">
    <h1>Soil & Water Conservation Programme</h1>
    <p>Wolaita Zone • Real-Time Monitoring Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ================= DATA =================
@st.cache_data
def load_data():
    swc = pd.read_csv("data/swc_structures_2025.csv")
    fodder = pd.read_csv("data/fodder_sites_2025.csv")
    return swc, fodder

swc, fodder = load_data()
kebele_geojson = "data/kebele_boundaries.geojson"

# ================= FILTERS =================
st.sidebar.header("Filters")
selected_woreda = st.sidebar.selectbox("Woreda", ["All"] + sorted(swc['woreda'].unique()))
selected_year = st.sidebar.selectbox("Construction Year", ["All"] + sorted(swc['construction_year'].unique(), reverse=True))
structure_filter = st.sidebar.multiselect("Structure Type", swc['structure_type'].unique(),
                                         default=["Stone-faced soil bund", "Fanya juu terrace", "Check dam (stone)"])

df_swc = swc.copy()
fodder_filtered = fodder.copy()
if selected_woreda != "All":
    df_swc = df_swc[df_swc['woreda'] == selected_woreda]
    fodder_filtered = fodder[fodder['woreda'] == selected_woreda]
if selected_year != "All":
    df_swc = df_swc[df_swc['construction_year'] == selected_year]
if structure_filter:
    df_swc = df_swc[df_swc['structure_type'].isin(structure_filter)]

# ================= FULLY INTERACTIVE MAP — WOREDA NAME ON ALL GREEN BOXES =================
st.markdown("<div class='section-title'>Field Implementation Map</div>", unsafe_allow_html=True)
m = folium.Map(location=[6.85, 37.75], zoom_start=11, tiles="CartoDB positron")

# KEBELE BOUNDARIES — NOW WITH RICH HOVER SHOWING WOREDA + KEBELE NAME
folium.GeoJson(
    kebele_geojson,
    style_function=lambda x: {
        'fillColor': '#90ee90',
        'color': '#1e4d2b',
        'weight': 2.5,
        'fillOpacity': 0.26
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['woreda', 'kebele'],  # Make sure these exact column names exist in your GeoJSON
        aliases=['Woreda:', 'Kebele:'],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #1e4d2b;
            color: white;
            font-family: Arial;
            font-weight: bold;
            font-size: 14px;
            padding: 12px;
            border-radius: 10px;
            border: 3px solid #2e8b57;
            box-shadow: 0 6px 16px rgba(0,0,0,0.5);
        """,
        max_width=800
    )
).add_to(m)

# SWC Structures — unchanged
for _, r in df_swc.sample(n=min(3000, len(df_swc)), random_state=42).iterrows():
    folium.CircleMarker(
        location=[r.latitude, r.longitude],
        radius=7.5,
        color="#0d6efd",
        fillColor="#3b82f6",
        fillOpacity=0.94,
        tooltip=f"""
        <div style="font-family: Arial; font-size: 13px; padding: 8px; background: #1e4d2b; color: white; border-radius: 6px; min-width: 180px;">
            <b>Woreda:</b> {r.woreda}<br>
            <b>Type:</b> {r.structure_type}<br>
            <b>Year:</b> {r.construction_year}<br>
            <b>Soil Saved:</b> {r.soil_saved_ton_per_year:,.0f} tons/yr<br>
            <b>Farms Protected:</b> {r.farms_protected}
        </div>
        """
    ).add_to(m)

# Fodder Sites — unchanged
for _, r in fodder_filtered.iterrows():
    folium.Marker(
        location=[r.latitude, r.longitude],
        icon=folium.Icon(color="darkgreen", icon="leaf", prefix="fa"),
        tooltip=f"""
        <div style="font-family: Arial; font-size: 13px; padding: 10px; background: #1e4d2b; color: white; border-radius: 8px; min-width: 200px; box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
            <b style="font-size:14px;">Fodder Development Site</b><br>
            <b>Woreda:</b> {r.woreda}<br>
            <b>Households Reached:</b> {r.households_reached:,}<br>
            <b>Area Covered:</b> {r.area_ha:.2f} ha<br>
            <b>Est. Beneficiaries:</b> {r.households_reached * 5:,} people
        </div>
        """
    ).add_to(m)

st_folium(m, width=1480, height=780)

# ================= KEY PROGRAMME ACHIEVEMENTS — UNCHANGED =================
st.markdown("<div class='section-title'>Key Programme Achievements</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<h3 style='text-align:center; color:#1e4d2b; font-weight:900; font-size:2.2rem; margin:1.5rem 0 2rem 0;'>SWC Structures & Soil Conservation Impact by Woreda</h3>", unsafe_allow_html=True)
    
    impact = df_swc.groupby('woreda').agg({'id':'count','soil_saved_ton_per_year':'sum'}).round(0).sort_values('id', ascending=False).reset_index()
    
    fig_bar = px.bar(
        impact, x='woreda', y='id',
        color='soil_saved_ton_per_year',
        color_continuous_scale=["#e8f5e8","#c8e6c9","#a5d6a7","#81c784","#66bb6a","#43a047","#2e7d32","#1b5e20"],
        text='id'
    )
    fig_bar.update_traces(
        textposition='outside',
        textfont=dict(size=19, color='#000000', family="Arial Black", weight="bold"),
        marker_line=dict(width=3, color="#ffffff")
    )
    fig_bar.update_layout(
        height=750,
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            title="<b>Soil Saved (tons/year)</b>",
            title_font=dict(size=18, color="#000000", family="Arial Black"),
            font=dict(size=16, color="#000000", family="Arial", weight="bold"),
            bgcolor="rgba(255,255,255,0.98)",
            bordercolor="#2e8b57",
            borderwidth=4
        ),
        xaxis=dict(title="Woreda", title_font=dict(size=19, color="#1e4d2b"), tickfont=dict(size=16, color="#1e4d2b")),
        yaxis=dict(title="Number of Structures", title_font=dict(size=19, color="#1e4d2b"), tickfont=dict(size=16, color="#1e4d2b")),
        xaxis_tickangle=30,
        margin=dict(t=80)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.markdown("<h3 style='text-align:center; color:#1e4d2b; font-weight:900; font-size:2.2rem; margin:1.5rem 0 2rem 0;'>Structure Type Distribution</h3>", unsafe_allow_html=True)
    
    top_types = df_swc['structure_type'].value_counts().head(8)
    fig_pie = px.pie(
        values=top_types.values, names=top_types.index,
        hole=0.6,
        color_discrete_sequence=["#1b5e20","#2e7d32","#43a047","#66bb6a","#81c784","#a5d6a7","#c8e6c9","#e8f5e8"]
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=23, color='white', family="Arial Bold"),
        marker=dict(line=dict(color='white', width=5))
    )
    fig_pie.update_layout(
        height=750,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(font=dict(size=17, color="#000000"), bgcolor="white", bordercolor="#2e8b57", borderwidth=3)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ================= KPIs =================
st.markdown("<div class='section-title'>Key Performance Indicators</div>", unsafe_allow_html=True)
st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)

metrics = [
    (f"{len(df_swc):,}", "Total SWC Structures Built"),
    (f"{df_swc['farms_protected'].sum():,}", "Farms Protected"),
    (f"{df_swc['soil_saved_ton_per_year'].sum():,.0f}", "Annual Soil Saved (tons)"),
    (f"{df_swc['soil_saved_ton_per_year'].sum()*5:,.0f}", "5-Year Projection"),
    (f"{len(fodder_filtered):,}", "Fodder Sites"),
    (f"{fodder_filtered['households_reached'].sum():,}", "Households Reached"),
    (f"{fodder_filtered['area_ha'].sum():.1f}", "Fodder Area (ha)")
]

for value, label in metrics:
    st.markdown(f"""
    <div class="kpi-item">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<div class="footer">
    <h3>RCBDIA • Wolaita Zone</h3>
    <p>Developed by Aklilu Abera Dana</p>
    <p>Transforming Landscapes. Empowering Communities.</p>
</div>
""", unsafe_allow_html=True)


# In[ ]:




