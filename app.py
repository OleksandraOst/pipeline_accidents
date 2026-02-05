import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Pipeline Accidents Map",
    layout="wide"
)

st.title("🛢️ Pipeline Accidents in North America")
st.markdown(
    "Interactive map of crude oil pipeline incidents with year and volume filtering. "
    "Marker size reflects spill magnitude relative to the full dataset."
)

# ---------------------------
# Load data
# ---------------------------

@st.cache_data
def load_data():
    df_canada = pd.read_csv("data/final_df_canada.csv")
    df_usa = pd.read_csv("data/final_df_usa_2010_2024.csv")

    # Standardize columns
    df_canada = df_canada.rename(columns={
        "Latitude": "lat",
        "Longitude": "lon",
        "Released volume (m3)": "volume",
        "Year": "year"
    })
    df_canada["country"] = "Canada"

    df_usa = df_usa.rename(columns={
        "LOCATION_LATITUDE": "lat",
        "LOCATION_LONGITUDE": "lon",
        "RELEASE M3": "volume",
        "IYEAR": "year"
    })
    df_usa["country"] = "USA"

    df = pd.concat([df_canada, df_usa], ignore_index=True)

    df["year"] = df["year"].astype(int)
    df = df.dropna(subset=["lat", "lon", "volume"])

    # Cap volume ONLY for marker sizing (performance + readability)
    df["volume_capped"] = df["volume"].clip(upper=10_000)

    return df


df = load_data()

# ---------------------------
# GLOBAL size reference (key fix)
# ---------------------------

GLOBAL_MAX_VOLUME = df["volume_capped"].max()

# Plotly sizing formula recommendation
SIZE_MAX = 18
SIZE_REF = 2.0 * GLOBAL_MAX_VOLUME / (SIZE_MAX ** 2)

# ---------------------------
# Sidebar controls
# ---------------------------

st.sidebar.header("Filters")

country_option = st.sidebar.selectbox(
    "Country",
    ["Canada", "USA", "Canada + USA"]
)

# Year slider
min_year = int(df["year"].min())
max_year = int(df["year"].max())

year_range = st.sidebar.slider(
    "Year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Volume slider (filter only — does NOT affect size scale)
min_vol = int(df["volume"].min())
max_vol = int(df["volume"].max())

volume_range = st.sidebar.slider(
    "Released volume (m³)",
    min_value=min_vol,
    max_value=max_vol,
    value=(min_vol, max_vol)
)

# ---------------------------
# Filter data
# ---------------------------

df_plot = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["volume"] >= volume_range[0]) &
    (df["volume"] <= volume_range[1])
]

if country_option != "Canada + USA":
    df_plot = df_plot[df_plot["country"] == country_option]

# Sample if too many points (performance safeguard)
MAX_POINTS = 3000
if len(df_plot) > MAX_POINTS:
    df_plot = df_plot.sample(MAX_POINTS, random_state=42)

# ---------------------------
# Map
# ---------------------------

fig = px.scatter_mapbox(
    df_plot,
    lat="lat",
    lon="lon",
    color="volume",
    size="volume_capped",
    color_continuous_scale="Viridis",
    zoom=2,
    mapbox_style="carto-positron",
    hover_data={
        "country": True,
        "year": True,
        "volume": ":,.0f",
        "lat": False,
        "lon": False
    },
    height=720
)

# 🔒 Lock marker size to GLOBAL scale
fig.update_traces(
    marker=dict(
        sizemode="area",
        sizeref=SIZE_REF,
        sizemin=3
    )
)

fig.update_layout(
    coloraxis_colorbar_title="Released volume (m³)",
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Summary stats
# ---------------------------

st.subheader("📊 Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Number of incidents", f"{len(df_plot):,}")
col2.metric(
    "Total volume released (m³)",
    f"{df_plot['volume'].sum():,.0f}"
)
col3.metric(
    "Year range",
    f"{year_range[0]} – {year_range[1]}"
)
