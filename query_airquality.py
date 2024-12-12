import sqlite3

def query_air_quality_data():
    """
    Queries and analyzes air quality data from the AirQualityData table.
    """
    conn = sqlite3.connect("WeatherAirQuality.db")
    cur = conn.cursor()

    # Total records in AirQualityData
    cur.execute("SELECT COUNT(*) FROM AirQualityData")
    total_records = cur.fetchone()[0]
    print(f"Total Air Quality Records: {total_records}")

    # Average AQI
    cur.execute("SELECT AVG(aqi) FROM AirQualityData")
    avg_aqi = cur.fetchone()[0]
    print(f"Average AQI: {avg_aqi:.2f}")

    # Most frequent main pollutant
    cur.execute("SELECT main_pollutant, COUNT(*) FROM AirQualityData GROUP BY main_pollutant ORDER BY COUNT(*) DESC LIMIT 1")
    most_frequent_pollutant = cur.fetchone()
    if most_frequent_pollutant:
        print(f"Most Frequent Main Pollutant: {most_frequent_pollutant[0]} ({most_frequent_pollutant[1]} occurrences)")

    # Close connection
    conn.close()

if __name__ == "__main__":
    query_air_quality_data()
