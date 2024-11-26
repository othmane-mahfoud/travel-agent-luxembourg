import pandas as pd
from utils.foursquare import fetch_foursquare_places

# Define location (latitude, longitude) for Luxembourg City
location = '49.6117,6.1319'

# Fetch coffee shops and restaurants
dining_and_drinking_df = fetch_foursquare_places(category='13000', location=location)

# Save to a single CSV file
dining_and_drinking_df.to_csv('data/foursquare_dining.csv', index=False)

print("Data for coffee shops and restaurants has been saved to 'data/foursquare_places.csv'.")
