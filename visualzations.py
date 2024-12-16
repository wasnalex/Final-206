import sqlite3

# Connect to the database
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

def combine_weather_air_data_by_hour():
    """
    Combines data from WeatherData and AirQualityData by matching only the hour
    and inserts up to 100 rows into WeatherAirQualityData.
    """
    print("Combining data from WeatherData and AirQualityData by hour...")

    # Drop and recreate WeatherAirQualityData table to ensure clean insertion
    cur.execute('''
        DROP TABLE IF EXISTS WeatherAirQualityData
    ''')

    cur.execute('''
        CREATE TABLE WeatherAirQualityData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hour TEXT NOT NULL,
            temp_c REAL,
            condition TEXT,
            wind_mph REAL,
            humidity INTEGER,
            aqi INTEGER,
            main_pollutant TEXT
        )
    ''')

    # Debugging: Verify sample data from WeatherData
    cur.execute("SELECT hour, temp_c, condition FROM WeatherData LIMIT 10")
    weather_sample = cur.fetchall()
    print("WeatherData sample:", weather_sample)

    # Debugging: Verify sample data from AirQualityData
    cur.execute("SELECT hour, aqi, main_pollutant FROM AirQualityData LIMIT 10")
    air_sample = cur.fetchall()
    print("AirQualityData sample:", air_sample)

    # Debugging: Check JOIN results to verify the match on hour
    cur.execute('''
        SELECT 
            w.hour, w.temp_c, w.condition, w.wind_mph, w.humidity,
            a.aqi, a.main_pollutant
        FROM WeatherData w
        JOIN AirQualityData a 
            ON w.hour = a.hour
        LIMIT 10
    ''')
    join_results = cur.fetchall()
    print("Sample JOIN Results:", join_results)

    try:
        # Combine data and insert into WeatherAirQualityData
        cur.execute('''
            INSERT INTO WeatherAirQualityData (hour, temp_c, condition, wind_mph, humidity, aqi, main_pollutant)
            SELECT 
                w.hour, 
                w.temp_c, 
                w.condition, 
                w.wind_mph, 
                w.humidity, 
                a.aqi, 
                a.main_pollutant
            FROM WeatherData w
            JOIN AirQualityData a 
                ON w.hour = a.hour
            LIMIT 100
        ''')
        conn.commit()

        # Fetch and print inserted data for verification
        cur.execute("SELECT * FROM WeatherAirQualityData LIMIT 10")
        data = cur.fetchall()

        if data:
            print("Sample data inserted into WeatherAirQualityData:")
            for row in data:
                print(row)
        else:
            print("No data inserted into WeatherAirQualityData.")
    except Exception as e:
        print("Error occurred:", e)

# Combine data and populate WeatherAirQualityData table
combine_weather_air_data_by_hour()

# Close the database connection
conn.close()

