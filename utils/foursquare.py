import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Foursquare API key from environment variables
FOURSQUARE_API_KEY = os.getenv('FOURSQUARE_API_KEY')

def fetch_foursquare_places(category, location, radius=1000, limit=50):
    """
    Fetch places from the Foursquare Places API.

    Parameters:
    - category (str): The category of places to search for (e.g., 'coffee shop', 'restaurant').
    - location (str): The latitude and longitude of the location as 'lat,lng'.
    - radius (int): Search radius in meters (default is 1000m).
    - limit (int): Maximum number of results to retrieve (default is 50).

    Returns:
    - DataFrame: A pandas DataFrame containing place details.
    """
    # Base URL for the Foursquare Places API
    url = 'https://api.foursquare.com/v3/places/search'

    # Headers for authentication
    headers = {
        'Authorization': FOURSQUARE_API_KEY
    }

    # Parameters for the API request
    params = {
        'categories': category,
        'll': location,
        'radius': radius,
        'limit': limit,
        'fields': 'fsq_id,name,categories,geocodes,location,description,tel,rating,price,tips'
    }

    try:
        # Make the API request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()
        results = data.get('results', [])

        # Extract relevant details for each place
        places_list = []
        for place in results:
            fsq_id = place.get('fsq_id', 'N/A')
            name = place.get('name', 'N/A')
            category_info = place.get('categories', [{}])[0]
            category_name = category_info.get('name', 'N/A')
            icon_info = category_info.get('icon', {})
            icon = f"{icon_info.get('prefix', '')}bg_64{icon_info.get('suffix', '')}"
            geocodes = place.get('geocodes', {}).get('main', {})
            latitude = geocodes.get('latitude', 'N/A')
            longitude = geocodes.get('longitude', 'N/A')
            region = place.get('location', {}).get('region', 'N/A')
            formatted_address = place.get('location', {}).get('formatted_address', 'N/A')
            description = place.get('description', 'N/A')
            tel = place.get('tel', 'N/A')
            rating = place.get('rating', 'N/A')
            price = place.get('price', 'N/A')
            if place.get('tips'):
                tips = '| '.join(tip['text'] for tip in place['tips'])
            else:
                tips = 'N/A'

            places_list.append({
                'FSQ_ID': fsq_id,
                'Name': name,
                'Category': category_name,
                'Icon': icon,
                'Latitude': latitude,
                'Longitude': longitude,
                'Region': region,
                'Formatted Address': formatted_address,
                'Description': description,
                'Phone Number': tel,
                'Rating': rating,
                'Price': price,
                'Tips': tips
            })

        # Convert the list of places to a pandas DataFrame
        df = pd.DataFrame(places_list)
        return df

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
