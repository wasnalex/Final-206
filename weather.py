import requests
import sqlite3

# Database setup
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

# Create table for Weather Data
cur.execute('''
CREATE TABLE IF NOT EXISTS WeatherData (
    date TEXT,
    hour TEXT,
    temp_c REAL,
    condition TEXT,
    wind_mph REAL,
    humidity INTEGER
)
''')

def fetch_weather_data(location, api_key, days=7):
    """
    Fetches hourly weather forecast and stores it in the database.
    """
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days={days}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for day in data["forecast"]["forecastday"]:
            for hour_data in day["hour"]:
                date = hour_data["time"][:10]
                hour = hour_data["time"][11:]
                temp_c = hour_data["temp_c"]
                condition = hour_data["condition"]["text"]
                wind_mph = hour_data["wind_mph"]
                humidity = hour_data["humidity"]

                # Insert data into the database
                cur.execute('''
                INSERT INTO WeatherData (date, hour, temp_c, condition, wind_mph, humidity)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (date, hour, temp_c, condition, wind_mph, humidity))
        conn.commit()
        print(f"Weather data for {location} stored successfully.")
    else:
        print(f"Failed to fetch weather data. Status Code: {response.status_code}, {response.text}")

# Fetch data for Detroit, MI
fetch_weather_data("Detroit, MI", "e2566028033342cebf212759240312")

conn.close()

