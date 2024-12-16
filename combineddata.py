import sqlite3

# Connect to the database
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

def remove_conditions_column():
    """
    Removes the 'conditions' column from WeatherAirQualityData.
    """
    print("Creating a new table without the 'conditions' column...")

    # Step 1: Create a new table without the 'conditions' column
    cur.execute('''
        CREATE TABLE WeatherAirQualityData_new AS
        SELECT 
            id, 
            hour, 
            temp_c, 
            wind_mph, 
            humidity, 
            aqi, 
            main_pollutant, 
            condition_id
        FROM WeatherAirQualityData
    ''')
    print("Created new table WeatherAirQualityData_new without 'conditions' column.")

    # Step 2: Drop the old table
    cur.execute("DROP TABLE WeatherAirQualityData")
    print("Dropped old table WeatherAirQualityData.")

    # Step 3: Rename the new table to the original table name
    cur.execute("ALTER TABLE WeatherAirQualityData_new RENAME TO WeatherAirQualityData")
    print("Renamed WeatherAirQualityData_new to WeatherAirQualityData.")

    conn.commit()

# Remove the 'conditions' column
remove_conditions_column()

# Verify the structure of the updated table
def verify_table_structure():
    cur.execute("PRAGMA table_info(WeatherAirQualityData)")
    columns = cur.fetchall()
    print("\nUpdated WeatherAirQualityData table structure:")
    for column in columns:
        print(column)

verify_table_structure()

# Close the database connection
conn.close()

