import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Steel Plants Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

df = pd.read_csv('NonZeroCapacityPlantsCleaned.csv')

st.title("Steel Plants Over The World Dashboard")
st.markdown("Explore plant capacity, geographic distribution, and other metrics.")

st.sidebar.header("Filter Options")

company_options = sorted(df['Owner'].dropna().unique().tolist())
selected_company = st.sidebar.multiselect(
    "Select Company",
    options=company_options,
    default=[]
)

area_options = sorted(df['Country/area'].dropna().unique().tolist())
selected_country = st.sidebar.multiselect(
    "Select Country/area",
    options=area_options,
    default=[]
)

min_val = int(df['total_capacity'].min()) if 'total_capacity' in df.columns else 0
max_val = int(df['total_capacity'].max()) if 'total_capacity' in df.columns else 50000

min_cap, max_cap = st.sidebar.slider(
    "Capacity Range",
    min_value=min_val,
    max_value=max_val,
    value=(min_val, max_val),
    step=500
)

filtered_df = df.copy()

if 'total_capacity' in filtered_df.columns:
    filtered_df = filtered_df[
        (filtered_df['total_capacity'] >= min_cap) & 
        (filtered_df['total_capacity'] <= max_cap)
    ]

if selected_company:
    filtered_df = filtered_df[filtered_df['Owner'].isin(selected_company)]

if selected_country:
    filtered_df = filtered_df[filtered_df['Country/area'].isin(selected_country)]



col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Plants", value='1293')
with col2:
    working_plants = len(filtered_df)
    st.metric(label="Working Plants", value=working_plants)
    
    total_cap = filtered_df['total_capacity'].sum() if 'total_capacity' in filtered_df.columns else 0
    st.metric(label="Total Capacity, ttpa", value=f"{total_cap:,.0f}")
with col3:
    st.metric(label="Countries Covered", value=filtered_df['Country/area'].nunique())

st.divider()

st.subheader("Steel Plant Locations")
st.map(filtered_df) 

st.caption("Data sources: litpop, gem-download | Built with Streamlit")