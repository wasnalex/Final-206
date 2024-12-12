import requests
import sqlite3
import time
from datetime import datetime, timedelta

# Database setup
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

# Create table for Air Quality Data
cur.execute('''
CREATE TABLE IF NOT EXISTS AirQualityData (
    date TEXT,
    hour TEXT,
    aqi INTEGER,
    main_pollutant TEXT
)
''')

def fetch_air_quality_data(city, state, country, api_key, current_date):
    """
    Fetches real-time air quality data and stores it in the database.
    """
    url = f"https://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pollution = data["data"]["current"]["pollution"]
        aqi = pollution["aqius"]
        main_pollutant = pollution["mainus"]

        # Use the current_date and format it
        date = current_date.strftime("%Y-%m-%d")
        hour = current_date.strftime("%H:%M")

        # Insert into the database
        cur.execute('''
        INSERT INTO AirQualityData (date, hour, aqi, main_pollutant)
        VALUES (?, ?, ?, ?)
        ''', (date, hour, aqi, main_pollutant))
        conn.commit()
        print(f"Air quality data for {city} on {date} at {hour} stored successfully.")
    else:
        print(f"Failed to fetch air quality data. Status Code: {response.status_code}")

# Set start and end dates
start_date = datetime(2024, 12, 2)
end_date = datetime(2024, 12, 8)
current_date = start_date

# Fetch data for each hour between start and end dates
while current_date <= end_date:
    fetch_air_quality_data("Detroit", "Michigan", "USA", "c10feb4c-d997-4b79-8b90-12071d06536b", current_date)
    current_date += timedelta(hours=1)
    time.sleep(5)  # Adjust for testing (use longer sleep time in production)

conn.close()

