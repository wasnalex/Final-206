# Final Project - SI 206/ Fall 2024
# Group name: Popcorn
# Aleandra Wasington
# Olga Hamilton
# Weather and AirQuality APIs, SQL, and Visualizations
# pull all queries, and every file plus visualizations here

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
data = pd.read_csv("WeatherAirQuality_JoinedData.csv")

# Preview the data
print(data.head())

#Create the Visualizations
#Use Matplotlib to plot the data.

#1. Scatter Plot: Temperature vs. AQI
plt.figure(figsize=(10, 6))
plt.scatter(data['Temperature (C)'], data['AQI'], alpha=0.7, c='blue')
plt.title("Scatter Plot: Temperature vs AQI")
plt.xlabel("Temperature (°C)")
plt.ylabel("Air Quality Index (AQI)")
plt.grid(True)
plt.show()

#Bar Chart: Average AQI by Weather Condition
avg_aqi_condition = data.groupby("Condition")["AQI"].mean()

plt.figure(figsize=(12, 6))
avg_aqi_condition.plot(kind='bar', color='skyblue')
plt.title("Average AQI by Weather Condition")
plt.xlabel("Weather Condition")
plt.ylabel("Average AQI")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#Line Plot: AQI Over Time
# Ensure the 'Date' column is datetime
data['Date'] = pd.to_datetime(data['Date'])

# Sort data by Date and Hour for a smoother plot
data = data.sort_values(by=['Date', 'Hour'])

plt.figure(figsize=(12, 6))
plt.plot(data['Date'] + pd.to_timedelta(data['Hour'], unit='h'), data['AQI'], marker='o', linestyle='-', color='green')
plt.title("AQI Over Time")
plt.xlabel("Date and Hour")
plt.ylabel("Air Quality Index (AQI)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Save Plot as a File
plt.savefig("scatter_temperature_aqi.png", dpi=300)