import requests
import matplotlib 
import sqlite3
import time 
from datetime import datetime
#This cowork request the weather for url
AP_key = "e2566028033342cebf212759240312"
location = ["Los Angeles"]           
days = 7
for locations in location:

    url = f"http://api.weatherapi.com/v1/forecast.json?key={AP_key}&q={locations}&days={days}"
    response = requests.get(url)
    
    if response.status_code == 200:
            print(f"Fetching data for {location}")
            data = response.json()

            # Check the structure of the data
            print(f"Sample data for {location}: {data['forecast']['forecastday'][0]}")

            for day in data["forecast"]["forecastday"]:
                for hour_data in day["hour"]:
                    date = hour_data["time"][:10]
                    hour = hour_data["time"][11:]
                    temp_c = hour_data["temp_c"]
                    condition = hour_data["condition"]["text"]
                    wind_mph = hour_data["wind_mph"]
                    humidity = hour_data["humidity"]

                    # Insert into database
                    cur.execute('''
                    INSERT INTO WeatherData (date, hour, temp_c, condition, wind_mph, humidity)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (date, hour, temp_c, condition, wind_mph, humidity))

            conn.commit()
    else:
            print(f"Failed to fetch data for {location}. Status Code: {response.status_code}")
    


    data["forecast"]["forecastday"][0]["hour"]

    def fetch_weather_data():
  

        for day in data["forecast"]["forecastday"]:
                for hour_data in day["hour"]:
                    date = hour_data["time"][:9]
                    hour = hour_data["time"][9:]
                    temp_c = hour_data["temp_c"]
                    condition = hour_data["condition"]["text"]
                    wind_mph = hour_data["wind_mph"]
                    humidity = hour_data["humidity"]

                # Insert into database
                    cur.execute('''
                    INSERT INTO WeatherData (date, hour, temp_c, condition, wind_mph, humidity)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (date, hour, temp_c, condition, wind_mph, humidity))

    conn.commit()
    

    # This function is useful for quickly checking the integrity 
#and basic structure of the WeatherData table.
def verify_weather_data():
    cur.execute("SELECT COUNT(*) FROM WeatherData")
    total_rows = cur.fetchone()[0]
    print(f"Total weather data rows: {total_rows}")

    cur.execute("SELECT * FROM WeatherData LIMIT 5")
    sample_rows = cur.fetchall()
    print("Sample weather data:", sample_rows)

# Call the function to verify data
verify_weather_data()



def check_duplicates():
    query = '''
    SELECT date, hour, COUNT(*)
    FROM WeatherData
    GROUP BY date, hour
    HAVING COUNT(*) > 1
    '''
    cur.execute(query)
    duplicates = cur.fetchall()
    if duplicates:
        print(f"Found duplicates: {duplicates}")
    else:
        print("No duplicates found.")

# Call the function
check_duplicates()



def remove_duplicates():
    query = '''
    DELETE FROM WeatherData
    WHERE ROWID NOT IN (
        SELECT MIN(ROWID)
        FROM WeatherData
        GROUP BY date, hour, location
    )
    '''
    cur.execute(query)
    conn.commit()
    print("Duplicates removed successfully.")

# Call the function