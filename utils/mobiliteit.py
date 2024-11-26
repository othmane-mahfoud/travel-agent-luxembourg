import os
import pandas as pd
import requests

from dotenv import load_dotenv
from difflib import get_close_matches

# Load environment variables from .env file
load_dotenv(override=True)

# Retrieve the OpenWeatherMap API key from environment variables
MOBILITEIT_API_KEY = os.getenv('MOBILITEIT_API_KEY')

# function to find closest match for a stop name and return the id
def find_closest_stop(stop_name):
    """
    Finds the closest match for a given stop name in the stops.csv data and returns its stop_id.

    Parameters:
    - stop_name (str): The name of the stop to search for.
    - data (DataFrame): The DataFrame containing stop_id and stop_name.

    Returns:
    - dict: A dictionary with the closest match and corresponding stop_id.
            Returns None if no close match is found.
    """
    # Get stops data into a dataframe
    data = pd.read_csv("data/stops.txt", encoding='utf-8', dtype={"stop_id": str})
    
    # Ensure data has the required columns
    if "stop_name" not in data.columns or "stop_id" not in data.columns:
        raise ValueError("Data must contain 'stop_name' and 'stop_id' columns.")

    # Extract the list of stop names
    stop_names = data["stop_name"].tolist()
    for stop in stop_names:
        stop.lower()

    # Find the closest match using difflib
    closest_match = get_close_matches(stop_name.lower(), stop_names, n=1, cutoff=0.2)  # Adjust cutoff if needed

    if closest_match:
        matched_name = closest_match[0]
        # Retrieve the corresponding stop_id
        stop_id = data.loc[data["stop_name"] == matched_name, "stop_id"].values[0]
        return {"stop_name": matched_name, "stop_id": stop_id}
    else:
        return None


# Get available trips from start to dest
def get_transportation_details(start: str, dest: str):
    start_id = find_closest_stop(start).get("stop_id")
    start_name = find_closest_stop(start).get("stop_name")
    dest_id = str(find_closest_stop(dest).get("stop_id"))
    dest_name = find_closest_stop(dest).get("stop_name")

    payload = {}
    payload["accessId"] = MOBILITEIT_API_KEY
    payload["id"] = start_id
    payload["direction"] = dest_id
    payload["format"] = "json"
    payload["maxJourney"] = 3
    r = requests.get('https://cdt.hafas.de/opendata/apiserver/departureBoard', params=payload)
    response = r.json()
    try:
        response = requests.get('https://cdt.hafas.de/opendata/apiserver/departureBoard', params=payload)
        response.raise_for_status()
        data = response.json()

        trips = []
        
        if ("Departure" in data):
            departures = data["Departure"]
            for departure in departures:
                trips.append({ "bus_name": departure.get("name"), 
                              "departure_time": departure.get("time"), 
                              "real_time_departure_time": departure.get("rtTime"),
                              "departure_stop": departure.get("stop"),
                              "platform_number": departure.get("directionFlag"),
                              "direction_name": departure.get("direction")
                              })
            return trips
                
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying mobiliteit API: {e}")
        return None
    

message=get_transportation_details(start="Esch sur Alzette Guillaume Capus", dest="Porte des sciences")
print(message)