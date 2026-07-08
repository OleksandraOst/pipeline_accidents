import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ===========================
# Page config & style
# ===========================

st.set_page_config(
    page_title="Pipeline Accidents Dashboard",
    layout="wide"
)

PLOT_TEMPLATE = "plotly_white"

st.title("🛢️ Pipeline Accidents in North America")


# ===========================
# Load data
# ===========================

@st.cache_data
def load_data():
    df_canada = pd.read_csv("data/final_df_canada.csv")
    df_usa = pd.read_csv("data/final_df_usa_2010_2024.csv")

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

    df["volume_capped"] = df["volume"].clip(upper=10_000)

    return df


df = load_data()

# ===========================
# Pipeline length assumptions (km)
# ===========================

PIPELINE_LENGTH_KM = {
    "USA": 3_000_000,
    "Canada": 840_000
}

NORMALIZATION_FACTOR = 10_000  # incidents per 10k km

# ===========================
# Global marker sizing
# ===========================

GLOBAL_MAX_VOLUME = df["volume_capped"].max()
SIZE_MAX = 18
SIZE_REF = 2.0 * GLOBAL_MAX_VOLUME / (SIZE_MAX ** 2)

# ===========================
# Sidebar filters
# ===========================

st.sidebar.header("Filters")

country_option = st.sidebar.selectbox(
    "Country",
    ["Canada", "USA", "Canada + USA"]
)

year_range = st.sidebar.slider(
    "Year range",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

volume_range = st.sidebar.slider(
    "Released volume (m³)",
    int(df["volume"].min()),
    int(df["volume"].max()),
    (int(df["volume"].min()), int(df["volume"].max()))
)

# ===========================
# Filter data
# ===========================

df_plot = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["volume"] >= volume_range[0]) &
    (df["volume"] <= volume_range[1])
]

if country_option != "Canada + USA":
    df_plot = df_plot[df_plot["country"] == country_option]

if len(df_plot) > 3000:
    df_plot = df_plot.sample(3000, random_state=42)

# ===========================
# MAP
# ===========================

st.subheader("🗺️ Spatial Distribution of Pipeline Incidents")

fig_map = px.scatter_mapbox(
    df_plot,
    lat="lat",
    lon="lon",
    color="volume",
    size="volume_capped",
    color_continuous_scale="Viridis",
    zoom=2,
    mapbox_style="carto-positron",
    height=650,
    template=PLOT_TEMPLATE,
    hover_data={
        "country": True,
        "year": True,
        "volume": ":,.0f",
        "lat": False,
        "lon": False
    }
)

fig_map.update_traces(
    marker=dict(
        sizemode="area",
        sizeref=SIZE_REF,
        sizemin=3
    )
)

fig_map.update_layout(
    coloraxis_colorbar_title="Released volume (m³)",
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig_map, width="stretch")

# ===========================
# SUMMARY
# ===========================

st.subheader("📊 Summary")

c1, c2, c3 = st.columns(3)
c1.metric("Incidents", f"{len(df_plot):,}")
c2.metric("Total volume (m³)", f"{df_plot['volume'].sum():,.0f}")
c3.metric("Year range", f"{year_range[0]} – {year_range[1]}")

# ===========================
# ANALYSIS
# ===========================

st.markdown("---")
st.header("📈 Comparative Analysis")

# ---------------------------
# Incidents per year (absolute)
# ---------------------------

st.subheader("Incidents per year (absolute)")

abs_year = (
    df.groupby(["year", "country"])
      .size()
      .reset_index(name="count")
)

fig_abs = px.line(
    abs_year,
    x="year",
    y="count",
    color="country",
    markers=True,
    template=PLOT_TEMPLATE
)

fig_abs.update_layout(
    yaxis_title="Number of incidents",
    xaxis_title="Year"
)

st.plotly_chart(fig_abs, width="stretch")

# ---------------------------
# Incidents per year (normalized)
# ---------------------------

st.subheader("Incidents per 10,000 km of pipeline")

norm_year = abs_year.copy()
norm_year["pipeline_km"] = norm_year["country"].map(PIPELINE_LENGTH_KM)
norm_year["incidents_per_10k_km"] = (
    norm_year["count"] / norm_year["pipeline_km"] * NORMALIZATION_FACTOR
)

fig_norm = px.line(
    norm_year,
    x="year",
    y="incidents_per_10k_km",
    color="country",
    markers=True,
    template=PLOT_TEMPLATE
)

fig_norm.update_layout(
    yaxis_title="Incidents per 10,000 km",
    xaxis_title="Year"
)

st.plotly_chart(fig_norm, width="stretch")

# ---------------------------
# Volume distribution
# ---------------------------

st.subheader("Distribution of released volumes")

fig_box = px.box(
    df,
    x="country",
    y="volume",
    log_y=True,
    template=PLOT_TEMPLATE,
    points="outliers"
)

fig_box.update_layout(
    yaxis_title="Released volume (m³, log scale)",
    xaxis_title=""
)

st.plotly_chart(fig_box, width="stretch")

# ---------------------------
# Cumulative released volume
# ---------------------------

st.subheader("Cumulative released volume")

cumulative_volume = (
    df.groupby(["year", "country"])["volume"]
      .sum()
      .groupby(level=1)
      .cumsum()
      .reset_index()
)

fig_cumulative = px.line(
    cumulative_volume,
    x="year",
    y="volume",
    color="country",
    template=PLOT_TEMPLATE
)

fig_cumulative.update_layout(
    yaxis_title="Cumulative volume (m³)",
    xaxis_title="Year"
)

st.plotly_chart(fig_cumulative, width="stretch")

# ===========================
# Interpretation
# ===========================

st.markdown(
    """
    ### Interpretation notes
    - Raw incident counts are higher in the USA due to a **larger and denser pipeline network**.
    - After normalization by pipeline length, **incident rates are more comparable**.
    - The USA reports many small spills; Canada shows a heavier tail in released volumes.
    
    **Assumptions**
    - Pipeline lengths are approximate and used for normalization only.
    - Results should be interpreted as **relative trends**, not precise risk estimates.
    """
)