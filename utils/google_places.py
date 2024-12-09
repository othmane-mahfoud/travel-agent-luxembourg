import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time

load_dotenv(override=True)

API_KEY = os.getenv("GOOGLE_API_KEY")
location = '49.6112809,6.1236146'
radius = 20000
keywords = ['restaurant', 'fast-food', 'coffee shop', 'pub', 'bar']  # List of keywords to iterate over

# Step 1: Perform Nearby Search
def get_nearby_places(keyword):
    nearby_search_url = (
        f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        f'?location={location}&radius={radius}&keyword={keyword}&key={API_KEY}'
    )
    all_results = []
    while nearby_search_url:
        response = requests.get(nearby_search_url)
        data = response.json()
        results = data.get('results', [])
        all_results.extend(results)
        
        # Check if there is a next page
        next_page_token = data.get('next_page_token')
        if next_page_token:
            time.sleep(2)  # Required delay before using the next_page_token
            nearby_search_url = (
                f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
                f'?pagetoken={next_page_token}&key={API_KEY}'
            )
        else:
            nearby_search_url = None  # No more pages
            
    return all_results

# Step 2: Get Place Details
def get_place_details(place_id):
    fields = 'name,formatted_address,geometry,photos,types,formatted_phone_number,rating,price_level,reviews'
    place_details_url = (
        f'https://maps.googleapis.com/maps/api/place/details/json'
        f'?place_id={place_id}&fields={fields}&key={API_KEY}'
    )
    response = requests.get(place_details_url)
    return response.json().get('result', {})

# Step 3: Extract Desired Information
def extract_image_url(photos):
    if photos:
        photo_reference = photos[0]['photo_reference']
        return (
            f'https://maps.googleapis.com/maps/api/place/photo'
            f'?maxwidth=400&photoreference={photo_reference}&key={API_KEY}'
        )
    return 'None'

def extract_reviews(reviews):
    if not reviews:
        return 'None'
    review_texts = [review.get('text', 'No review text') for review in reviews[:3]]
    return ' | '.join(review_texts)

# Main Function
def fetch_places_data():
    all_places_data = []

    for keyword in keywords:  # Iterate over the keywords
        print(f"Fetching data for keyword: {keyword}")
        places = get_nearby_places(keyword)
        
        for place in places:
            place_id = place['place_id']
            details = get_place_details(place_id)
            
            # Extract details
            name = details.get('name', 'None')
            address = details.get('formatted_address', 'None')
            geometry = details.get('geometry', {}).get('location', {})
            latitude = geometry.get('lat', 'None')
            longitude = geometry.get('lng', 'None')
            types = details.get('types', [])
            phone_number = details.get('formatted_phone_number', 'None')
            rating = details.get('rating', 'None')
            price_level = details.get('price_level', 'None')
            reviews = extract_reviews(details.get('reviews', []))
            image_url = extract_image_url(details.get('photos', []))

            # Append data
            all_places_data.append({
                'Name': name,
                'Category': ', '.join(types),
                'Keyword': keyword,
                'Image URL': image_url,
                'Latitude': latitude,
                'Longitude': longitude,
                'Formatted Address': address,
                'Description': None,
                'Phone Number': phone_number,
                'Rating': rating,
                'Price Level': 2 if 'None' else price_level,
                'Reviews': reviews
            })

    # Combine all results into a DataFrame
    all_places_df = pd.DataFrame(all_places_data).drop_duplicates(subset=["Name", "Formatted Address"])
    return all_places_df

# Run the script and print results
if __name__ == '__main__':
    places_df = fetch_places_data()
    places_df.to_csv("data/google_places.csv", index=False)
    print(places_df.shape)
    print("Google Places Data Successfully Saved")
