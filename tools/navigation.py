from langchain.tools import tool
from utils.mobiliteit import get_transportation_details, find_nearby_stops

@tool
def transportation_directions(query: str):
    """
    Tool for fetching transportation directions using the Mobiliteit API.

    Parameters:
    - query (str): User query containing start and destination stops.

    Returns:
    - str: Directions or an error message.
    """
    try:
        # Parse the user query for start and destination stops
        if "to" not in query:
            return "Please specify the start and destination stops, e.g., 'How can I go from X to Y?'"

        parts = query.lower().split("to")
        start = parts[0].replace("how can i go from", "").strip()
        dest = parts[1].strip()

        # Fetch trip details
        trips = get_transportation_details(start=start, dest=dest)

        if trips:
            response = f"Based on information provided by Mobiliteit, here are the available trips from {start} to {dest}:\n"
            for trip in trips:
                response += (
                    f"- Wait at Platform {trip['platform_number']} for {trip['bus_name']} heading towards {trip['direction_name']}. "
                    f"Scheduled departure at {trip['departure_time']} "
                )
                if trip.get("real_time_departure_time"):
                    response += f"(real-time departure: {trip['real_time_departure_time']}).\n"
                else:
                    response += ".\n"
            return response
        else:
            return f"According to Mobiliteit, there are no possible trips from {start} to {dest}. Please try again with different stops."
    except Exception as e:
        return f"An error occurred while processing your request: {str(e)}"


@tool
def get_nearby_stops_tool(query: str) -> str:
    """
    This tool automatically fetches stops without requiring user-provided locations.
    
    Parameters:
    - query (str): User query containing question about stops.
    
     Returns:
    - str: bus stops and information about them
    """
    try:
        nearby_stops = find_nearby_stops(longitude = 5.947335, latitude = 49.50391)
        
        # Format the results
        if not nearby_stops:
            return "No nearby stops found for the given location."
        
        result = "Here are the nearby stops and the transportation options available:\n"
        for stop in nearby_stops:
            result += f"\n- **Stop Name**: {stop['name']} (Distance: {stop['distance']} meters)"
            for transport in stop["buses_or_trains"]:
                result += f"\n  - **{transport['name']}** (Line: {transport['line']}, Category: {transport['category']})"
        return result
    
    except Exception as e:
        return f"An error occurred while fetching nearby stops: {str(e)}"

