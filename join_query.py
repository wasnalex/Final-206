# Final Project - SI 206/ Fall 2024
# Group name: Popcorn
# Aleandra Wasington
# Olga Hamilton
# Weather and AirQuality APIs, SQL, and Visualizations
import sqlite3
import csv

# Connect to the database
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

def combine_weather_air_data():
    """
    Combines data from WeatherData and AirQualityData using SELECT and JOIN
    and inserts the result into WeatherAirQualityData.
    """
    print("Combining data from WeatherData and AirQualityData...")

    # SQL JOIN query to combine the data
    cur.execute('''
        SELECT w.date, w.hour, w.temp_c, w.condition, w.wind_mph, w.humidity, 
               a.aqi AS aqi_category, a.main_pollutant
        FROM WeatherData w
        JOIN Dates d ON w.date = d.date
        JOIN AirQualityData a ON d.id = a.date_id AND w.hour = a.hour
    ''')
    combined_data = cur.fetchall()

    if not combined_data:
        print("No matching data found between WeatherData and AirQualityData.")
        return

    print(f"Found {len(combined_data)} rows to insert into WeatherAirQualityData.")

    # Insert combined data into WeatherAirQualityData table
    cur.executemany('''
        INSERT INTO WeatherAirQualityData 
        (date, hour, temp_c, condition, wind_mph, humidity, aqi_category, main_pollutant)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', combined_data)

    conn.commit()
    print(f"Inserted {len(combined_data)} rows into WeatherAirQualityData.")

def export_to_csv():
    """
    Exports data from WeatherAirQualityData to a CSV file.
    """
    print("Exporting WeatherAirQualityData to CSV...")

    # Fetch data from the combined table
    cur.execute("SELECT * FROM WeatherAirQualityData")
    data = cur.fetchall()

    if not data:
        print("No data found in WeatherAirQualityData to export.")
        return

    # Define the CSV file name
    csv_file = "WeatherAirQualityData.csv"

    # Write the data to a CSV file
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow(["id", "date", "hour", "temp_c", "condition", "wind_mph", "humidity", "aqi_category", "main_pollutant"])
        # Write the data
        writer.writerows(data)

    print(f"Data successfully exported to {csv_file}.")

# Combine data and export it to a CSV
combine_weather_air_data()
export_to_csv()

conn.close()

