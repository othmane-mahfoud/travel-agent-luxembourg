import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Ticketmaster API key from environment variables
TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')

def fetch_ticketmaster_events(country_code='LU', city=None, classification_name=None, size=100):
    """
    Fetch events from the Ticketmaster API.

    Parameters:
    - country_code (str): ISO country code to filter events (default is 'LU' for Luxembourg).
    - city (str): City name to filter events.
    - classification_name (str): Genre or sub-genre to filter events.
    - size (int): Number of events to retrieve (default is 100).

    Returns:
    - DataFrame: A pandas DataFrame containing event details.
    """
    # Base URL for the Ticketmaster Discovery API
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'

    # Parameters for the API request
    params = {
        'apikey': TICKETMASTER_API_KEY,
        'countryCode': country_code,
        'size': size
    }

    # Add optional filters if provided
    if city:
        params['city'] = city
    if classification_name:
        params['classificationName'] = classification_name

    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Check if events are present in the response
        if '_embedded' not in data or 'events' not in data['_embedded']:
            print("No events found.")
            return pd.DataFrame()  # Return an empty DataFrame

        events = data['_embedded']['events']

        # Extract relevant details for each event
        event_list = []
        for event in events:
            event_name = event.get('name', 'N/A')
            images = event.get('images', [])
            image_url = images[0]['url'] if images else 'N/A'
            dates = event.get('dates', {})
            start_date = dates.get('start', {}).get('localDate', 'N/A')
            start_time = dates.get('start', {}).get('localTime', 'N/A')
            classifications = event.get('classifications', [])
            if classifications:
                genre = classifications[0]['genre']['name'] if classifications[0].get('genre') else 'N/A'
                subgenre = classifications[0]['subGenre']['name'] if classifications[0].get('subGenre') else 'N/A'
            venue_info = event.get('_embedded', {}).get('venues', [{}])[0]
            venue_name = venue_info.get('name', 'N/A')
            city_name = venue_info.get('city', {}).get('name', 'N/A')
            address = venue_info.get('address', {}).get('line1', 'N/A')

            event_list.append({
                'Event Name': event_name,
                'Image URL': image_url,
                'Start Date': start_date,
                'Start Time': start_time,
                'Genre': genre,
                'Subgenre': subgenre,
                'Venue': venue_name,
                'City': city_name,
                'Address': address,
                'Description': f"{event_name} is a {genre}/{subgenre} event taking place in {city_name} at {venue_name} on the {start_date} at {start_time}"
            })

        # Convert the list of events to a pandas DataFrame
        df = pd.DataFrame(event_list)
        return df

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    
if __name__ == "__main__":
    ticketmaster_events = fetch_ticketmaster_events()
    ticketmaster_events_df = pd.DataFrame(ticketmaster_events)
    ticketmaster_events_df.to_csv("data/ticketmaster_events.csv", index=False)
