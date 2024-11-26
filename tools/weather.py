from langchain_core.tools import tool
from utils.weather import get_current_weather, get_weather_forecast

@tool
def current_weather(query: str):
    """
    Tool for fetching the current weather in Luxembourg.

    Example queries:
    - "What is the weather right now in Luxembourg?"
    """
    data = get_current_weather(location='Luxembourg')
    if data:
        return (
            f"The current temperature in Luxembourg is {data['temperature']}°C, "
            f"feels like {data['feels_like']}°C. "
            f"The weather is described as '{data['description']}', "
            f"with a minimum temperature of {data['min_temp']}°C and a maximum of {data['max_temp']}°C."
        )
    return "I'm unable to fetch the current weather at the moment."

@tool
def weather_forecast(query: str):
    """
    Tool for fetching the 5-day weather forecast in Luxembourg.

    Example queries:
    - "What will the weather be tomorrow in Luxembourg?"
    - "Will it rain in the coming days?"
    """
    forecast_data = get_weather_forecast(location='Luxembourg')
    if forecast_data:
        forecast_summary = "Here is the 5-day weather forecast for Luxembourg:\n"
        for day in forecast_data:
            forecast_summary += (
                f"- {day['day']}: {day['description']} with a temperature of {day['temperature']}°C "
                f"(feels like {day['feels_like']}°C). Min: {day['min_temp']}°C, Max: {day['max_temp']}°C.\n"
            )
        return forecast_summary
    return "I'm unable to fetch the weather forecast at the moment."
