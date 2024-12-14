# Final Project - SI 206/ Fall 2024
# Group name: Popcorn
# Aleandra Wasington
# Olga Hamilton
# Weather and AirQuality APIs, SQL, and Visualizations

import sqlite3
import csv
# This script performs a join operation between two tables, WeatherData and AirQualityData, 
# in an SQLite database and writes the resulting data into a CSV file.
def join_weather_and_air_quality():
    """
    Performs a join query between WeatherData and AirQualityData
    using date and hour as the shared keys.
    Writes the results to a CSV file.
    """
    conn = sqlite3.connect("WeatherAirQuality.db")
    cur = conn.cursor()

    # Perform the join query
    cur.execute('''
        SELECT 
            w.date, 
            w.hour, 
            w.temp_c, 
            w.condition, 
            w.humidity, 
            a.aqi, 
            a.main_pollutant
        FROM WeatherData w
        JOIN AirQualityData a
        ON w.date = a.date AND w.hour = a.hour
    ''')
    results = cur.fetchall()

    # Write the joined data (Results) to a CSV file
    with open("WeatherAirQuality_JoinedData.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Hour", "Temperature (C)", "Condition", "Humidity", "AQI", "Main Pollutant"])
        writer.writerows(results)
        #if not results:
            #print("No weather data found.")
    print("Joined data written to WeatherAirQuality_JoinedData.csv successfully.")
    conn.close()
