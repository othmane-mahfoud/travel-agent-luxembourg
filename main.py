import pandas as pd
from utils.weather import get_current_weather, get_weather_forecast

current_weather = get_current_weather(location='Luxembourg')
print("Current Weather:", current_weather)

forecast = get_weather_forecast(location='Luxembourg')
for day in forecast:
    print(day)


