import os
from datetime import datetime

import mysql.connector
import requests


# --- Asetukset ---
API_KEY = os.environ.get("OWM_API_KEY")
CITY = "Tampere"

if not API_KEY:
    raise SystemExit("OWM_API_KEY ei ole asetettu ympäristömuuttujaksi")


DB_CONFIG = {
    "host": "localhost",
    "user": "appuser",
    "password": "TosiVahvaSalasana123!",
    "database": "exampledb",
}


def fetch_weather():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={API_KEY}&units=metric&lang=fi"
    )

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return temp, desc


def save_to_db(temp, desc):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Varmuuden vuoksi: luodaan taulu jos sitä ei ole
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city VARCHAR(50),
            temperature FLOAT,
            description VARCHAR(100),
            timestamp DATETIME
        )
        """
    )

    query = """
        INSERT INTO weather_data (city, temperature, description, timestamp)
        VALUES (%s, %s, %s, %s)
    """
    values = (CITY, temp, desc, datetime.now())

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()


def main():
    try:
        temp, desc = fetch_weather()
        save_to_db(temp, desc)
        print(f"OK: Tallennettu {CITY}: {temp} °C, {desc}")
    except Exception as e:
        print("VIRHE fetch_weather.py:", e)


if __name__ == "__main__":
    main()
