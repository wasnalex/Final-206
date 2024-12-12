import sqlite3

def query_weather_data():
    """
    Queries and analyzes weather data from the WeatherData table.
    """
    conn = sqlite3.connect("WeatherAirQuality.db")
    cur = conn.cursor()

    # Total records in WeatherData
    cur.execute("SELECT COUNT(*) FROM WeatherData")
    total_records = cur.fetchone()[0]
    print(f"Total Weather Records: {total_records}")

    # Average temperature
    cur.execute("SELECT AVG(temp_c) FROM WeatherData")
    avg_temp = cur.fetchone()[0]
    print(f"Average Temperature: {avg_temp:.2f}°C")

    # Count of weather conditions
    cur.execute("SELECT condition, COUNT(*) FROM WeatherData GROUP BY condition ORDER BY COUNT(*) DESC")
    condition_counts = cur.fetchall()
    print("Weather Condition Counts:")
    for condition, count in condition_counts:
        print(f"{condition}: {count}")

    # Close connection
    conn.close()

if __name__ == "__main__":
    query_weather_data()
