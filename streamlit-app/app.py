import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

DB_USER = "exampleuser"
DB_PASS = "koivunen"  # sama kuin DB:ssä
DB_NAME = "exampledb"
DB_HOST = "localhost"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")

st.title("Global Temperature Analysis")

@st.cache_data
def load_data():
    query = """
        SELECT Year, Mean, Source
        FROM global_temp
        WHERE Source = 'GCAG'
        ORDER BY Year;
    """
    df = pd.read_sql(query, engine)
    return df

df = load_data()

st.subheader("Global temperature anomalies (°C)")
st.dataframe(df)

st.subheader("Warming over time (since 1880)")
fig = px.line(df, x="Year", y="Mean", title="Global temperature anomaly (°C)")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Last 50 years")
last_50 = df[df["Year"] >= df["Year"].max() - 50]
st.line_chart(last_50.set_index("Year")["Mean"])

st.subheader("Basic statistics (all years)")
st.write(df["Mean"].describe())

st.markdown(
    """
---
**Data source:**  
Global temperature time series from [datasets/global-temp](https://github.com/datasets/global-temp),  
based on NOAA and NASA GISTEMP records.
    """
)
