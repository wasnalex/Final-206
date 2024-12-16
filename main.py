import sqlite3
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

def calculate_averages():
    """
    Calculates the average AQI and temperature (temp_c) for each condition.
    """
    print("\nCalculating averages for each condition_id...")
    cur.execute('''
        SELECT 
            w.condition_id, 
            wc.condition, 
            AVG(w.aqi) AS avg_aqi, 
            AVG(w.temp_c) AS avg_temp_c
        FROM WeatherAirQualityData w
        JOIN WeatherConditions wc
        ON w.condition_id = wc.id
        GROUP BY w.condition_id
        ORDER BY w.condition_id
    ''')
    results = cur.fetchall()

    print("\nAverages by Condition:")
    print(f"{'Condition ID':<15}{'Condition':<20}{'Avg AQI':<10}{'Avg Temp (C)':<15}")
    for row in results:
        print(f"{row[0]:<15}{row[1]:<20}{row[2]:<10.2f}{row[3]:<15.2f}")

    return results
def write_to_text_file(results, filename="averages.txt"):
    """
    Writes the calculated averages to a text file.
    """
    with open(filename, "w") as file:
        file.write("Averages by Condition\n")
        file.write(f"{'Condition ID':<15}{'Condition':<20}{'Avg AQI':<10}{'Avg Temp (C)':<15}\n")
        file.write("=" * 60 + "\n")
        
        for row in results:
            file.write(f"{row[0]:<15}{row[1]:<20}{row[2]:<10.2f}{row[3]:<15.2f}\n")

    print(f"\nAverages have been written to {filename}")

# Run the calculations and write to a text file
averages = calculate_averages()
write_to_text_file(averages)


def plot_averages(data):
    """
    Plots the average AQI and temperature for each condition.
    """
    # Extract data for plotting
    conditions = [row[1] for row in data]
    avg_aqi = [row[2] for row in data]
    avg_temp = [row[3] for row in data]

    # Create a figure with two subplots
    fig, ax1 = plt.subplots()

    # Plot Avg AQI
    ax1.bar(conditions, avg_aqi, alpha=0.7, color='b', label='Avg AQI')
    ax1.set_xlabel("Conditions")
    ax1.set_ylabel("Avg AQI", color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Add Avg Temp as a line plot on a secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(conditions, avg_temp, color='r', marker='o', label='Avg Temp (°C)')
    ax2.set_ylabel("Avg Temp (°C)", color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # Add a title and legend
    fig.suptitle("Average AQI and Temperature by Condition")
    fig.tight_layout()
    plt.show()

# Run the calculation
averages = calculate_averages()

# Plot the results
plot_averages(averages)

# Close the database connection
conn.close()