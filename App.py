# -------------------------
# IMPORTS (MUST BE FIRST)
# -------------------------
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Sustainability Dashboard", layout="wide")

st.title("🌍 Sustainability Data Dashboard")
st.markdown("Interactive dashboard for analysing World Bank sustainability data")

# -------------------------
# LOAD DATA
# -------------------------
file_path = r"C:\Users\Sashindhi Withanage\Desktop\DSPL ICW\WB_CCKP_Cleaned.csv"

@st.cache_data
def load_data():
    return pd.read_csv(file_path)

df = load_data()

# -------------------------
# AUTO-DETECT COLUMNS
# -------------------------
def find_column(keywords):
    for col in df.columns:
        for key in keywords:
            if key in col.lower():
                return col
    return None

country_col = find_column(["country"])
indicator_col = find_column(["indicator"])
year_col = find_column(["year"])
value_col = find_column(["value"])

# -------------------------
# ERROR CHECK
# -------------------------
if not all([country_col, indicator_col, year_col, value_col]):
    st.error("❌ Could not detect required columns.")
    st.write("Columns found:", df.columns)
    st.stop()

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("🔍 Filters")

country = st.sidebar.multiselect(
    "Select Country",
    options=df[country_col].dropna().unique(),
    default=df[country_col].dropna().unique()[:3]
)

indicator = st.sidebar.multiselect(
    "Select Indicator",
    options=df[indicator_col].dropna().unique(),
    default=df[indicator_col].dropna().unique()[:2]
)

filtered_df = df[
    (df[country_col].isin(country)) &
    (df[indicator_col].isin(indicator))
]

# -------------------------
# DATA PREVIEW
# -------------------------
st.subheader("📊 Dataset Preview")
st.dataframe(filtered_df.head())

# -------------------------
# CHART 1: LINE CHART
# -------------------------
st.subheader("📈 Trend Over Time")

fig1 = px.line(
    filtered_df,
    x=year_col,
    y=value_col,
    color=country_col
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# CHART 2: BAR CHART
# -------------------------
st.subheader("📊 Country Comparison (Latest Year)")

if not filtered_df.empty:
    latest_year = filtered_df[year_col].max()
    latest_df = filtered_df[filtered_df[year_col] == latest_year]

    fig2 = px.bar(
        latest_df,
        x=country_col,
        y=value_col,
        color=indicator_col,
        barmode="group"
    )
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# CHART 3: PIE CHART
# -------------------------
st.subheader("🥧 Distribution by Country")

pie_df = filtered_df.groupby(country_col)[value_col].mean().reset_index()

fig3 = px.pie(
    pie_df,
    names=country_col,
    values=value_col
)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# CHART 4: HISTOGRAM
# -------------------------
st.subheader("📊 Value Distribution")

fig4 = px.histogram(
    filtered_df,
    x=value_col,
    nbins=30
)
st.plotly_chart(fig4, use_container_width=True)

# -------------------------
# CHART 5: SCATTER PLOT
# -------------------------
st.subheader("🔍 Relationship Analysis")

fig5 = px.scatter(
    filtered_df,
    x=year_col,
    y=value_col,
    color=country_col,
    size=value_col
)
st.plotly_chart(fig5, use_container_width=True)

# -------------------------
# METRICS
# -------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_df))
col2.metric("Countries Selected", len(country))
col3.metric("Indicators Selected", len(indicator))

# -------------------------
# DOWNLOAD
# -------------------------
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)