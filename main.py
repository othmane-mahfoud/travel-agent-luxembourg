import pandas as pd
from utils.foursquare import fetch_foursquare_places

# Define location (latitude, longitude) for Luxembourg City
location = '49.6117,6.1319'

# Fetch coffee shops and restaurants
landmarks_outdoors_df = fetch_foursquare_places(category='16000', location=location)

# Save to a single CSV file
landmarks_outdoors_df.to_csv('data/foursquare_landmarks.csv', index=False)

print("Data for coffee shops and restaurants has been saved to 'data/foursquare_landmarks.csv'.")
