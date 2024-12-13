import requests
import sqlite3
from datetime import datetime, timedelta
import time

# Database setup
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

# Create the Dates table
cur.execute('''
CREATE TABLE IF NOT EXISTS Dates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE
)
''')

# Create the AirQualityData table
cur.execute('''
CREATE TABLE IF NOT EXISTS AirQualityData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER NOT NULL,
    hour TEXT NOT NULL,
    aqi INTEGER NOT NULL,
    main_pollutant TEXT NOT NULL,
    UNIQUE(date_id, hour, main_pollutant),
    FOREIGN KEY (date_id) REFERENCES Dates(id)
)
''')

def fetch_air_quality_data(city, state, country, api_key, current_date):
    """
    Fetches real-time air quality data for a specific date and stores it in the database.
    Limits to 25 entries per run and avoids duplicate data.
    """
    url = f"https://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Format the date
        date = current_date.strftime("%Y-%m-%d")

        # Insert date into Dates table
        cur.execute('''
            INSERT OR IGNORE INTO Dates (date) VALUES (?)
        ''', (date,))
        # Retrieve the date ID
        cur.execute('''
            SELECT id FROM Dates WHERE date = ?
        ''', (date,))
        date_id = cur.fetchone()[0]

        # Check how many rows already exist for this date
        cur.execute('''
            SELECT COUNT(*) FROM AirQualityData WHERE date_id = ?
        ''', (date_id,))
        existing_rows = cur.fetchone()[0]

        # Limit entries to 25 rows per run
        if existing_rows >= 25:
            print(f"Already stored 25 entries for {date}. Run again to fetch more data.")
            return

        # Process hourly data (simulated 24-hour data)
        row_count = 0
        for hour in range(existing_rows, 24):
            if row_count >= 25:
                break

            hour_time = f"{hour:02d}:00"
            pollution = data.get("data", {}).get("current", {}).get("pollution", {})
            if not pollution:
                print(f"No data available for {hour_time} on {date}")
                continue

            aqi = pollution.get("aqius", None)
            main_pollutant = pollution.get("mainus", None)

            # Skip if data is incomplete
            if aqi is None or main_pollutant is None:
                print(f"Incomplete data for {hour_time} on {date}")
                continue

            # Insert into AirQualityData table, referencing the date ID
            cur.execute('''
                INSERT OR IGNORE INTO AirQualityData (date_id, hour, aqi, main_pollutant)
                VALUES (?, ?, ?, ?)
            ''', (date_id, hour_time, aqi, main_pollutant))
            row_count += 1

        conn.commit()
        print(f"Stored {row_count} new entries for {date}.")
    else:
        print(f"Failed to fetch air quality data for {current_date.strftime('%Y-%m-%d')}. Status Code: {response.status_code}, {response.text}")

# Example loop to fetch data for a week
start_date = datetime(2024, 12, 2)
end_date = datetime(2024, 12, 8)

current_date = start_date
while current_date <= end_date:
    fetch_air_quality_data("Detroit", "Michigan", "USA", "c2e81695e-e960-4a33-8e44-0fbfc28099c9", current_date)
    current_date += timedelta(days=1)  # Move to the next day
    time.sleep(5)  # Adjust for testing or API rate limits

conn.close()

