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
    

def find_nearby_stops(longitude = 5.947335, latitude = 49.50391):
    """
    Return stops and the buses/trains that stop at them using the Mobiliteit API.

    Returns:
    - list: A list of dictionaries with details about stops and the buses/trains stopping there.
    """
    max_no = 20
    radius = 500
    url = "https://cdt.hafas.de/opendata/apiserver/location.nearbystops"
    params = {
        "accessId": MOBILITEIT_API_KEY,
        "originCoordLong": longitude,
        "originCoordLat": latitude,
        "maxNo": max_no,
        "r": radius,
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Parse the response
        nearby_stops = []
        for item in data.get("stopLocationOrCoordLocation", []):
            stop = item.get("StopLocation")
            if stop:
                stop_info = {
                    "name": stop.get("name"),
                    "id": stop.get("id"),
                    "extId": stop.get("extId"),
                    "latitude": stop.get("lat"),
                    "longitude": stop.get("lon"),
                    "distance": stop.get("dist"),
                    "products": stop.get("products"),
                    "buses_or_trains": []
                }

                # Extract buses/trains stopping at the stop
                products = stop.get("productAtStop", [])
                for product in products:
                    stop_info["buses_or_trains"].append({
                        "name": product.get("name"),
                        "line": product.get("line"),
                        "category": product.get("catOut"),
                        "icon_background_color": product.get("icon", {}).get("backgroundColor", {}).get("hex"),
                        "icon_foreground_color": product.get("icon", {}).get("foregroundColor", {}).get("hex")
                    })

                nearby_stops.append(stop_info)

        return nearby_stops

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while querying the Mobiliteit API: {e}")
        return []
    except KeyError as e:
        print(f"Key error while parsing the response: {e}")
        return []
    
    
if __name__ == "__main__":
    # Example coordinates for Esch-sur-Alzette
    # longitude = 5.9717754
    # latitude = 49.508418
    nearby_stops = find_nearby_stops()

    for stop in nearby_stops:
        print(f"Stop: {stop['name']} (Distance: {stop['distance']} meters)")
        for bus_or_train in stop["buses_or_trains"]:
            print(f"  - {bus_or_train['name']} (Line: {bus_or_train['line']}, Category: {bus_or_train['category']})")