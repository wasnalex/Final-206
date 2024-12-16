# Final Project - SI 206/ Fall 2024
# Group name: Popcorn
# Aleandra Wasington
# Olga Hamilton
# Weather and AirQuality APIs, SQL, and Visualizations





# Connect to the database
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

def fetch_condition_data():
    """
    Fetches condition_id counts from the WeatherAirQualityData table.
    """
    cur.execute('''
        SELECT condition_id, COUNT(*) as count
        FROM WeatherAirQualityData
        GROUP BY condition_id
        ORDER BY condition_id
    ''')
    rows = cur.fetchall()
    return rows

def plot_condition_frequencies(data):
    """
    Plots a bar chart of condition frequencies.
    """
    # Extract condition_ids and counts
    condition_ids = [row[0] for row in data]
    counts = [row[1] for row in data]

    # Map condition_ids to condition names (assuming the mapping is known)
    condition_names = {
        1: "Cloudy",
        2: "Overcast",
        3: "Partly Cloudy",
        4: "Mist"
    }
    labels = [condition_names.get(cond_id, f"ID {cond_id}") for cond_id in condition_ids]

    # Create the bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(labels, counts, alpha=0.7)
    plt.title("Frequency of Weather Conditions")
    plt.xlabel("Condition")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Fetch data and plot the graph
data = fetch_condition_data()
plot_condition_frequencies(data)

# Close the database connection
conn.close()


import sqlite3
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

def fetch_temp_aqi_data():
    """
    Fetches temperature and AQI data from the WeatherAirQualityData table.
    """
    cur.execute('''
        SELECT temp_c, aqi
        FROM WeatherAirQualityData
        WHERE temp_c IS NOT NULL AND aqi IS NOT NULL
    ''')
    rows = cur.fetchall()
    return rows

def plot_temp_vs_aqi(data):
    """
    Plots a scatter plot of Temperature vs. AQI.
    """
    # Extract temperatures and AQI values
    temperatures = [row[0] for row in data]
    aqi_values = [row[1] for row in data]

    # Create the scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(temperatures, aqi_values, alpha=0.7, edgecolors='k')
    plt.title("Temperature vs. AQI")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Air Quality Index (AQI)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

# Fetch data and plot the graph
data = fetch_temp_aqi_data()
plot_temp_vs_aqi(data)

# Close the database connection
conn.close()
