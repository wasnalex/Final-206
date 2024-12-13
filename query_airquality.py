def count_air_quality_data_by_date():
    """
    Counts occurrences of each date in AirQualityData and prints the results.
    """
    conn = sqlite3.connect("WeatherAirQuality.db")
    cur = conn.cursor()

    cur.execute('''
        SELECT date, COUNT(*) AS occurrences
        FROM AirQualityData
        GROUP BY date
        ORDER BY date
    ''')
    results = cur.fetchall()

    print("Air Quality Data Date Counts:")
    for date, count in results:
        print(f"{date}: {count}")
    conn.close()

