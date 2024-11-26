import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Retrieve the OpenWeatherMap API key from environment variables
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenWeatherMap API key from environment variables
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_current_weather(location='Luxembourg'):
    """
    Fetch current weather data for a location.

    Parameters:
    - location (str): The city name (default is 'Luxembourg').

    Returns:
    - dict: A dictionary containing current weather attributes.
    """
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': location,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'min_temp': data['main']['temp_min'],
            'max_temp': data['main']['temp_max'],
            'description': data['weather'][0]['description']
        }
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_weather_forecast(location='Luxembourg'):
    """
    Fetch 5-day weather forecast data for a location (daily at 12:00:00).

    Parameters:
    - location (str): The city name (default is 'Luxembourg').

    Returns:
    - list[dict]: A list of dictionaries containing weather attributes for the next 5 days.
    """
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': location,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        forecast_list = []
        for item in data['list']:
            if '12:00:00' in item['dt_txt']:
                # Extract the day of the forecast
                forecast_day = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime('%A')
                forecast_list.append({
                    'day': forecast_day,
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'min_temp': item['main']['temp_min'],
                    'max_temp': item['main']['temp_max'],
                    'description': item['weather'][0]['description']
                })

        return forecast_list
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

