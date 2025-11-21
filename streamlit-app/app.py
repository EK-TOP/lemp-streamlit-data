import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import mysql.connector

DB_USER = st.secrets["db_user"]
DB_PASS = st.secrets["db_pass"]
DB_NAME = st.secrets["db_name"]
DB_HOST = "localhost"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")

st.title("Global Temperature Analysis")

@st.cache_data
def load_global_temp():
    query = """
        SELECT Year, Mean, Source
        FROM global_temp
        WHERE Source = 'GCAG'
        ORDER BY Year;
    """
    df = pd.read_sql(query, engine)
    return df

@st.cache_data
def load_weather_data():
    query = """
        SELECT city, temperature, description, timestamp
        FROM weather_data
        ORDER BY timestamp DESC
        LIMIT 50;
    """
    df = pd.read_sql(query, engine)
    return df

#Global temp -osio

df = load_global_temp()

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

#Säädata OpenWeather + cronista

st.header("Paikallinen Tampereen sää")

try:
    wdf = load_weather_data()

    if wdf.empty:
        st.info("weather_data-taulu on tyhjä. Odota cron-skriptin ensimmäistä ajokertaa.")
    else:
        st.subheader("Viimeisimmät säähavainnot")
        st.dataframe(wdf)

        latest = wdf.iloc[0]

        st.subheader("Viimeisin havainto")
        st.write(f"**Kaupunki:** {latest['city']}")
        st.write(f"**Lämpötila:** {latest['temperature']} °C")
        st.write(f"**Kuvaus:** {latest['description']}")
        st.write(f"**Aikaleima:** {latest['timestamp']}")

except Exception as e:
    st.error(f"Säädatan lukeminen epäonnistui: {e}")

@st.cache_data
def load_weather_data():
    conn = mysql.connector.connect(
        host="localhost",
        user=st.secrets["db_user"],        # sama kuin global-tempille
        password=st.secrets["db_pass"],
        database=st.secrets["db_name"]     # tässä samassa kannassa weather_data
    )

    query = """
        SELECT city, temperature, description, timestamp
        FROM weather_data
        ORDER BY timestamp DESC
        LIMIT 50;
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df
