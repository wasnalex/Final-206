import sqlite3
import csv

def write_analysis_results():
    """
    Queries data, performs calculations, and writes results to a CSV file.
    """
    conn = sqlite3.connect("WeatherAirQuality.db")
    cur = conn.cursor()

    # Perform calculations
    cur.execute("SELECT AVG(temp_c) FROM WeatherData")
    avg_temp = cur.fetchone()[0]

    cur.execute("SELECT AVG(aqi) FROM AirQualityData")
    avg_aqi = cur.fetchone()[0]

    cur.execute("SELECT condition, COUNT(*) FROM WeatherData GROUP BY condition ORDER BY COUNT(*) DESC LIMIT 1")
    most_frequent_condition = cur.fetchone()

    cur.execute("SELECT main_pollutant, COUNT(*) FROM AirQualityData GROUP BY main_pollutant ORDER BY COUNT(*) DESC LIMIT 1")
    most_frequent_pollutant = cur.fetchone()

    # Write results to a CSV file
    with open("WeatherAirQuality_AnalysisResults.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Average Temperature (C)", f"{avg_temp:.2f}"])
        writer.writerow(["Average AQI", f"{avg_aqi:.2f}"])
        writer.writerow(["Most Frequent Weather Condition", most_frequent_condition[0]])
        writer.writerow(["Most Frequent Main Pollutant", most_frequent_pollutant[0]])

    print("Analysis results written to WeatherAirQuality_AnalysisResults.csv successfully.")
    conn.close()
