import sqlite3

# Connect to the database
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

def initialize_database():
    """
    Initializes the database by creating necessary tables if they don't exist.
    """
    # Create WeatherConditions table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS WeatherConditions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition TEXT NOT NULL UNIQUE
        )
    ''')
    print("Created WeatherConditions table.")

    # Create WeatherAirQualityData table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS WeatherAirQualityData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date Date NOT NULL,
            hour HOUR NOT NULL,
            temp_c REAL,
            wind_mph REAL,
            humidity INTEGER,
            aqi INTEGER,
            main_pollutant TEXT,
            condition_id INTEGER
        )
    ''')
    print("Created WeatherAirQualityData table.")

    # Populate WeatherConditions if empty
    cur.execute("SELECT COUNT(*) FROM WeatherConditions")
    if cur.fetchone()[0] == 0:
        conditions = [("Cloudy",), ("Overcast",), ("Partly Cloudy",), ("Mist",)]
        cur.executemany("INSERT INTO WeatherConditions (condition) VALUES (?)", conditions)
        conn.commit()
        print("Populated WeatherConditions table.")

def verify_weatherdata_structure():
    """
    Prints the structure of the WeatherData table to debug missing columns.
    """
    cur.execute("PRAGMA table_info(WeatherData)")
    columns = cur.fetchall()
    print("\nWeatherData table structure:")
    for column in columns:
        print(column)

def combine_weather_air_data():
    """
    Combines data from WeatherData and AirQualityData by matching date and hour,
    maps condition_id using WeatherConditions, and inserts up to 100 rows into WeatherAirQualityData.
    """
    print("\nCombining data from WeatherData and AirQualityData...")

    # Debugging: Print WeatherData rows to verify contents
    cur.execute("SELECT * FROM WeatherData LIMIT 10")
    weather_data_sample = cur.fetchall()
    print("\nSample data from WeatherData:")
    for row in weather_data_sample:
        print(row)

    # Combine data and insert into WeatherAirQualityData
    cur.execute('''
        INSERT INTO WeatherAirQualityData (hour, temp_c, wind_mph, humidity, aqi, main_pollutant, condition_id)
        SELECT 
            w.hour,
            w.temp_c,
            w.wind_mph,
            w.humidity,
            a.aqi,
            a.main_pollutant,
            w.condition_id
        FROM WeatherData w
        JOIN Dates d ON w.date = d.date
        JOIN AirQualityData a ON a.date_id = d.id AND w.hour = a.hour
        WHERE w.condition_id IS NOT NULL
        LIMIT 100
    ''')
    conn.commit()
    print("Inserted up to 100 rows into WeatherAirQualityData.")

def verify_table_structure():
    """
    Prints the structure of WeatherAirQualityData to verify the schema.
    """
    cur.execute("PRAGMA table_info(WeatherAirQualityData)")
    columns = cur.fetchall()
    print("\nUpdated WeatherAirQualityData table structure:")
    for column in columns:
        print(column)

def verify_data():
    """
    Prints sample data from WeatherAirQualityData to verify the inserted rows.
    """
    cur.execute("SELECT * FROM WeatherAirQualityData LIMIT 10")
    rows = cur.fetchall()
    print("\nSample data from WeatherAirQualityData:")
    for row in rows:
        print(row)

# Initialize database and tables
initialize_database()

# Debug: Verify structure of WeatherData
verify_weatherdata_structure()

# Combine data from WeatherData and AirQualityData
combine_weather_air_data()

# Verify table structure and sample data
verify_table_structure()
verify_data()

# Close the database connection
conn.close()
