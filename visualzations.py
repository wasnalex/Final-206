import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("WeatherAirQuality.db")
cur = conn.cursor()

def plot_aqi_category_distribution():
    """
    Visualization 1: AQI Category Distribution by Day
    """
    print("Generating AQI Category Distribution by Day...")
    days = []
    category_counts = {1: [], 2: [], 3: [], 4: [], 5: []}

    # Loop through each day's table and count AQI categories
    for date in ["2024-12-02", "2024-12-03", "2024-12-04", "2024-12-05", "2024-12-06"]:
        table_name = f"AirQualityData_{date.replace('-', '_')}"
        cur.execute(f'''
            SELECT aqi_category, COUNT(*) 
            FROM {table_name} 
            GROUP BY aqi_category
        ''')
        data = cur.fetchall()
        days.append(date)
        for category, count in data:
            category_counts[category].append(count)

        # Ensure all categories have data (fill with 0 if missing)
        for category in category_counts.keys():
            if len(category_counts[category]) < len(days):
                category_counts[category].append(0)

    # Plot data
    plt.figure(figsize=(10, 6))
    for category, counts in category_counts.items():
        plt.bar(days, counts, label=f"Category {category}")

    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.title("AQI Category Distribution by Day")
    plt.legend(title="AQI Category")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_main_pollutants_distribution():
    """
    Visualization 2: Main Pollutants Distribution
    """
    print("Generating Main Pollutants Distribution...")
    pollutants = []
    counts = []

    # Loop through each day's table to count pollutants
    for date in ["2024-12-02", "2024-12-03", "2024-12-04", "2024-12-05", "2024-12-06"]:
        table_name = f"AirQualityData_{date.replace('-', '_')}"
        cur.execute(f'''
            SELECT main_pollutant, COUNT(*) 
            FROM {table_name} 
            GROUP BY main_pollutant
        ''')
        data = cur.fetchall()
        for pollutant, count in data:
            if pollutant in pollutants:
                idx = pollutants.index(pollutant)
                counts[idx] += count
            else:
                pollutants.append(pollutant)
                counts.append(count)

    # Plot data
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=pollutants, autopct="%1.1f%%", startangle=140)
    plt.title("Main Pollutants Distribution")
    plt.tight_layout()
    plt.show()


def plot_avg_aqi_by_hour():
    """
    Visualization 3: Average AQI Category by Hour
    """
    print("Generating Average AQI Category by Hour...")
    hours = list(range(24))
    avg_aqi = []

    # Calculate average AQI category for each hour across all days
    for hour in hours:
        hour_str = f"{hour:02d}:00"
        total = 0
        count = 0
        for date in ["2024-12-02", "2024-12-03", "2024-12-04", "2024-12-05", "2024-12-06"]:
            table_name = f"AirQualityData_{date.replace('-', '_')}"
            cur.execute(f'''
                SELECT AVG(aqi_category) 
                FROM {table_name} 
                WHERE hour = ?
            ''', (hour_str,))
            result = cur.fetchone()[0]
            if result:
                total += result
                count += 1
        avg_aqi.append(total / count if count > 0 else None)

    # Plot data
    plt.figure(figsize=(10, 6))
    plt.plot(hours, avg_aqi, marker="o", label="Average AQI Category")
    plt.xticks(hours)
    plt.xlabel("Hour")
    plt.ylabel("Average AQI Category")
    plt.title("Average AQI Category by Hour")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()


# Run visualizations
plot_aqi_category_distribution()
plot_main_pollutants_distribution()
plot_avg_aqi_by_hour()

# Close the database connection
conn.close()
