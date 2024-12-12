from weather import fetch_weather_data
from air_quality import fetch_air_quality_data

# Orchestrate data fetching
fetch_weather_data("Detroit, MI", "e2566028033342cebf212759240312")
fetch_air_quality_data("Detroit", "Michigan", "USA", "c10feb4c-d997-4b79-8b90-12071d06536b")

# Include visualization calls
# Add functions from visualizations.py to generate charts
