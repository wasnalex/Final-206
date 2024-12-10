import requests
import sqlite3

url = "https://api.airvisual.com/v2/city"
params = {
    "city": "Santa Clara",
    "state": "California",
    "start_date": "2020-09-01",
    "end_date": "2020-09-30",
    "country": "USA",
    "key": "c10feb4c-d997-4b79-8b90-12071d06536b"  # Replace with your actual API key
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}, {response.text}")

# Set up database
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

# Create table
cur.execute('''
CREATE TABLE IF NOT EXISTS WeatherAirQualityData (
    date TEXT,
    hour TEXT,
    temp_c REAL,
    condition TEXT,
    wind_mph REAL,
    humidity INTEGER,
    aqi INTEGER,
    main_pollutant TEXT
)
''')

# Function to fetch data from APIs
def fetch_data(city, state, country, iqair_key, weather_key):
    # IQAir API
    iqair_url = f"https://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={iqair_key}"
    iqair_response = requests.get(iqair_url)
    
    if iqair_response.status_code == 200:
        iqair_data = iqair_response.json()
        aqi = iqair_data["data"]["current"]["pollution"]["aqius"]  # US AQI
        main_pollutant = iqair_data["data"]["current"]["pollution"]["mainus"]
    else:
        print(f"Failed to fetch air quality data for {city}. Status: {iqair_response.status_code}")
        return

        conn.commit()
    

# Close connection
conn.close()

# Function to fetch data from APIs
def fetch_data(city, state, country, iqair_key, weather_key):
# IQAir API
    iqair_url = f"https://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={iqair_key}"
    iqair_response = requests.get(iqair_url)

    if iqair_response.status_code == 200:
        iqair_data = iqair_response.json()
        aqi = iqair_data["data"]["current"]["pollution"]["aqius"] # US AQI
        main_pollutant = iqair_data["data"]["current"]["pollution"]["mainus"]
        date = iqair_data['data']['current']['pollution']['ts'][:10] 
        hour = iqair_data['data']['current']['pollution']['ts'][10:16] 
    else:
        print(f"Failed to fetch air quality data for {city}. Status: {iqair_response.status_code}")
        return

        conn.commit()


cur.execute('''
                    INSERT INTO WeatherAirQualityData (date, hour, aqi, main_pollant, iqair)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (date, hour, aqi, main_pollant, iqair))