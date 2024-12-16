# Final Project - SI 206/ Fall 2024
# Group name: Popcorn
# Aleandra Wasington
# Olga Hamilton
# Weather and AirQuality APIs, SQL, and Visualizations

import sqlite3
import matplotlib.pyplot as plt

def count_air_quality_data_by_date():
    """
    Counts occurrences of each date in AirQualityData, prints the results,
    and visualizes AQI trends over time using a line chart.
    """
    print("Function started") 
    results = []  # Initialize results to store data for visualization

    try:
        # Connect to the database
        conn = sqlite3.connect("WeatherAirQuality.db")
        cur = conn.cursor()
        print("Connected to database") 

        # Execute the query to get date and count of occurrences
        cur.execute('''
            SELECT date, COUNT(*) AS occurrences
            FROM AirQualityData
            GROUP BY date
            ORDER BY date
        ''')
        results = cur.fetchall()

        print(f"Query returned {len(results)} results")
        print("Air Quality Data Date Counts:")

        # Print results
        for date, count in results:
            print(f"{date}: {count}") 

        # Visualization
        if results:
            # Extract dates and counts
            dates = [row[0] for row in results]
            counts = [row[1] for row in results]

            # Plot the line chart
            plt.figure(figsize=(12, 6))
            plt.plot(dates, counts, marker='o', linestyle='-', color='blue', label='AQI Occurrences')
            plt.xlabel('Date')
            plt.ylabel('Occurrences')
            plt.title('Air Quality Data Occurrences Over Time')
            plt.xticks(rotation=45, ha='right')  # Rotate date labels for better readability
            plt.legend()
            plt.tight_layout()  # Adjust layout to prevent overlap
            plt.grid(True)  # Add a grid for better readability
            plt.show()
        else:
            print("No data to visualize.")

    except Exception as e:
        print(f"An error occurred: {e}")  # Print any exceptions
    finally:
        if conn:
            conn.close()
        print("Function finished") 

# Call the function
count_air_quality_data_by_date()
