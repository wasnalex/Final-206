# Final Project - SI 206/ Fall 2024
# Group name: Popcorn
# Aleandra Wasington
# Olga Hamilton
# Weather and AirQuality APIs, SQL, and Visualizations
# Query weather
# This script calculates and displays the number of weather data records for each unique date 
# in the WeatherData table of the SQLite database WeatherAirQuality.db.

import sqlite3
import matplotlib.pyplot as plt

def count_weather_data_by_date():
    """
    Counts occurrences of each date in WeatherData and prints the results,
    then visualizes the data using a bar chart with a legend.
    """
    print("Function started") 
    results = []  # Initialize results to store data for visualization

    try:
        conn = sqlite3.connect("WeatherAirQuality.db")
        cur = conn.cursor()
        print("Connected to database") 

        # Execute the query
        cur.execute('''
        SELECT date, COUNT(*) AS occurrences
        FROM WeatherData
        GROUP BY date
        ORDER BY date
        ''')
        results = cur.fetchall()

        print(f"Query returned {len(results)} results")
        print("Weather Data Date Counts:")

        for date, count in results:
            print(f"{date}: {count}")

        # Visualization
        if results:
            dates = [row[0] for row in results]
            counts = [row[1] for row in results]

            plt.figure(figsize=(10, 6))  # Adjust figure size
            bars = plt.bar(dates, counts, color='red', label='Occurrences')  # Create bar chart and add label
            plt.xlabel('Date')
            plt.ylabel('Occurrences')
            plt.title('Weather Data Occurrences by Date')
            plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
            plt.legend(fontsize=10)  # Add legend
            plt.grid(True)
            plt.tight_layout()  # Adjust layout to prevent overlap

            # Add value labels on top of each bar
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                         f'{height}',
                         ha='center', va='bottom')

            plt.show()  # Display the plot
        else:
            print("No data to visualize.")

    except Exception as e:
        print(f"An error occurred: {e}")  # Print any exceptions
    finally:
        if conn:
            conn.close()
        print("Function finished") 

# Call the function
count_weather_data_by_date()
