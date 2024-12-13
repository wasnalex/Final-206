import sqlite3

def count_weather_data_by_date():
    """
    Counts occurrences of each date in WeatherData and prints the results.
    """
    conn = sqlite3.connect("WeatherAirQuality.db")
    cur = conn.cursor()

    cur.execute('''
        SELECT date, COUNT(*) AS occurrences
        FROM WeatherData
        GROUP BY date
        ORDER BY date
    ''')
    results = cur.fetchall()

    print("Weather Data Date Counts:")
    for date, count in results:
        print(f"{date}: {count}")
    conn.close()
