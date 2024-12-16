# Final Project - SI 206/ Fall 2024
# Group name: Popcorn
# Aleandra Wasington
# Olga Hamilton
# Weather and AirQuality APIs, SQL, and Visualizations
# Weather API

import requests
import sqlite3
from datetime import datetime, timedelta

# Database setup
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

def create_date_table(date):
    """
    Creates a table for a specific date if it doesn't already exist.
    """
    table_name = f"WeatherData_{date.replace('-', '_')}"
    with sqlite3.connect("WeatherAirQuality.db") as conn:
        cur = conn.cursor()
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hour TEXT NOT NULL,
                temp_c REAL NOT NULL,
                condition TEXT NOT NULL,
                wind_mph REAL NOT NULL,
                humidity INTEGER NOT NULL
            )
        ''')
        conn.commit()
       # print("PRINT TABLE:",table_name )
    return table_name

def fetch_weather_data(location, api_key, start_date, end_date):
    """
    Fetches hourly weather forecast for each date in the range 12/2/2024 to 12/6/2024
    and stores it in the database.
    Stops after inserting up to 25 rows of data per day.
    """
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        url = f"http://api.weatherapi.com/v1/history.json?key={api_key}&q={location}&dt={date_str}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            table_name = create_date_table(date_str)
            row_count = 0  # Track rows inserted

            # limiting row to >= 25
            for hour_data in data["forecast"]["forecastday"][0]["hour"]:
                if row_count >= 25:
                    print(f"Row limit reached for {date_str}. Stopping insertion.")
                    break

                hour = hour_data["time"][11:]
                temp_c = hour_data["temp_c"]
                condition = hour_data["condition"]["text"]
                wind_mph = hour_data["wind_mph"]
                humidity = hour_data["humidity"]

                # Insert into the specific date's table
                cur.execute(f'''
                    INSERT INTO {table_name} (hour, temp_c, condition, wind_mph, humidity)
                    VALUES (?, ?, ?, ?, ?)
                ''', (hour, temp_c, condition, wind_mph, humidity))
                row_count += 1

            conn.commit()
            print(f"Weather data for {date_str} stored successfully in table {table_name}.")
        else:
            print(f"Failed to fetch weather data for {date_str}. Status Code: {response.status_code}, {response.text}")

        current_date += timedelta(days=1)

# Fetch weather data for 12/2/2024 - 12/6/2024
fetch_weather_data("Detroit, MI", "e2566028033342cebf212759240312", "2024-12-02", "2024-12-06")

conn.close()


