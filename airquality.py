# Final Project - SI 206/ Fall 2024
# Group name: Popcorn
# Aleandra Wasington
# Olga Hamilton
# Weather and AirQuality APIs, SQL, and Visualizations
# AirQuality APIs

import requests
import sqlite3
from datetime import datetime, timedelta
import time

# Database setup
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

def create_date_table(date):
    """
    Creates a table for a specific date if it doesn't already exist.
    """
    table_name = f"AirQualityData_{date.replace('-', '_')}"
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hour TEXT NOT NULL,
            aqi_category INTEGER NOT NULL,
            main_pollutant TEXT NOT NULL
        )
    ''')
    conn.commit()
    print("PRINT TABLE:",table_name )
    return table_name

def aqi_to_category(aqi):
    """
    Maps AQI values to categories (1-5).
    """
    if aqi <= 50:
        return 1  # Good
    elif aqi <= 100:
        return 2  # Moderate
    elif aqi <= 150:
        return 3  # Unhealthy for Sensitive Groups
    elif aqi <= 200:
        return 4  # Unhealthy
    else:
        return 5  # Very Unhealthy

def fetch_air_quality_data(city, state, country, api_key, current_date):
    """
    Fetches real-time air quality data for a specific date and stores it in the database.
    Simulates hourly data with a limit of 25 entries per run.
    """
    url = f"https://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        date = current_date.strftime("%Y-%m-%d")
        table_name = create_date_table(date)

        # Check how many rows already exist for this date
        cur.execute(f'''
            SELECT COUNT(*) FROM {table_name}
        ''')
        existing_rows = cur.fetchone()[0]
        print(f"Existing rows in {table_name}: {existing_rows}")

        if existing_rows >= 24:
            print(f"All 24 entries already stored for {date}.")
            return

        row_count = 0
        print(f"Simulating data for {date}. Starting from hour: {existing_rows}")
        for hour in range(existing_rows, 24):
            if row_count >= 25:  # Limit to 25 rows per run
                break

            hour_time = f"{hour:02d}:00"
            pollution = data.get("data", {}).get("current", {}).get("pollution", {})
            print(f"Pollution data for {hour_time}: {pollution}")
            if not pollution:
                print(f"No data available for {hour_time} on {date}")
                continue

            aqi = pollution.get("aqius", None)
            main_pollutant = pollution.get("mainus", None)

            if aqi is None or main_pollutant is None:
                print(f"Incomplete data for {hour_time} on {date}")
                continue

            # Convert AQI to category ID
            aqi_category = aqi_to_category(aqi)

            # Insert into the specific date's table
            cur.execute(f'''
                INSERT INTO {table_name} (hour, aqi_category, main_pollutant)
                VALUES (?, ?, ?)
            ''', (hour_time, aqi_category, main_pollutant))
            row_count += 1

        conn.commit()
        print(f"Stored {row_count} new entries for {date} in table {table_name}.")
    else:
        print(f"Failed to fetch air quality data for {current_date.strftime('%Y-%m-%d')}. Status Code: {response.status_code}, {response.text}")

# Example loop to fetch data for a week
start_date = datetime(2024, 12, 2)
end_date = datetime(2024, 12, 6)

current_date = start_date
while current_date <= end_date:
    fetch_air_quality_data("Detroit", "Michigan", "USA", "2e81695e-e960-4a33-8e44-0fbfc28099c9", current_date)
    current_date += timedelta(days=1)
    time.sleep(5)

conn.close()

