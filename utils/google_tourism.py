import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time

load_dotenv(override=True)

# Load API Key and configuration
API_KEY = os.getenv("GOOGLE_API_KEY")
location = '49.6112809,6.1236146'  # Luxembourg coordinates
radius = 20000  # 20 km radius

# Function to fetch places for a specific type
def get_places(place_type):
    nearby_search_url = (
        f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        f'?location={location}&radius={radius}&type={place_type}&key={API_KEY}'
    )
    all_results = []
    while nearby_search_url:
        response = requests.get(nearby_search_url)
        data = response.json()
        results = data.get('results', [])
        all_results.extend(results)

        # Handle pagination with next_page_token
        next_page_token = data.get('next_page_token')
        if next_page_token:
            time.sleep(2)  # Delay required by Google API
            nearby_search_url = (
                f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
                f'?pagetoken={next_page_token}&key={API_KEY}'
            )
        else:
            nearby_search_url = None  # No more pages
    return all_results

# Function to fetch detailed reviews using Place Details API
def get_place_details(place_id):
    fields = 'reviews'
    details_url = (
        f'https://maps.googleapis.com/maps/api/place/details/json'
        f'?place_id={place_id}&fields={fields}&key={API_KEY}'
    )
    response = requests.get(details_url)
    return response.json().get('result', {})

# Function to extract image URL from the response
def extract_image_url(photos):
    if photos:
        photo_reference = photos[0]['photo_reference']
        return (
            f'https://maps.googleapis.com/maps/api/place/photo'
            f'?maxwidth=400&photoreference={photo_reference}&key={API_KEY}'
        )
    return 'None'

# Function to extract reviews (text from first 3 reviews)
def extract_reviews(reviews):
    if not reviews:
        return 'None'
    review_texts = [review.get('text', 'No review text') for review in reviews[:3]]
    return ' | '.join(review_texts)

# Main function to fetch data for all types
def fetch_places_data():
    all_places_data = []
    types = [
        'tourist_attraction', 'observation_deck', 'monument', 'historical_place', 'museum',
        'botanical_garden', 'garden', 'historical_landmark',
        'national_park', 'park', 'plaza'
    ]

    for place_type in types:
        print(f"Fetching data for type: {place_type}")
        places = get_places(place_type)
        print(f"Fetched {len(places)} {place_type}s")
        
        for place in places:
            place_id = place.get('place_id', 'None')
            name = place.get('name', 'None')
            address = place.get('vicinity', 'None')
            geometry = place['geometry']['location']
            latitude = geometry['lat']
            longitude = geometry['lng']
            rating = place.get('rating', 'None')
            types = place.get('types', [])
            image_url = extract_image_url(place.get('photos', []))

            # Fetch reviews using Place Details API
            details = get_place_details(place_id)
            reviews = extract_reviews(details.get('reviews', []))

            all_places_data.append({
                'Name': name,
                'Category': ', '.join(types),
                'Type': place_type,
                'Image URL': image_url,
                'Latitude': latitude,
                'Longitude': longitude,
                'Address': address,
                'Rating': rating,
                'Reviews': reviews
            })

    # Combine results into a single DataFrame and remove duplicates
    all_places_df = pd.DataFrame(all_places_data).drop_duplicates(subset=["Name", "Address"])
    return all_places_df

# Save the data to a CSV file
if __name__ == '__main__':
    places_df = fetch_places_data()
    places_df.to_csv("data/google_tourism.csv", index=False)
    print(places_df.head())
    print(places_df.shape)
    print("Google Places Data with Reviews Successfully Saved")
