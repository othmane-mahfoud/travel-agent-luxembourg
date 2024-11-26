import os
import datetime
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_to_dict, messages_from_dict
from langchain_core.prompts import PromptTemplate

from langgraph.prebuilt import create_react_agent

from tools.weather import current_weather, weather_forecast
from tools.navigation import transportation_directions
from tools.events import event_tool
from tools.landmarks import landmark_tool
from tools.dining import dining_places_tool

from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Define the tools
tools = [
    Tool(name="Current Weather", func=current_weather, description="Get the current weather in Luxembourg."),
    Tool(name="Weather Forecast", func=weather_forecast, description="Get the 5-day weather forecast in Luxembourg."),
    Tool(name="Transportation Directions", func=transportation_directions, description="Provide directions using the Mobiliteit API."),
    Tool(name="Event Tool", func=event_tool, description="Provide information about events in Luxembourg."),
    Tool(name="Landmark Tool", func=landmark_tool, description="Retrieve information about landmarks and monuments in Luxembourg."),
    Tool(name="Dining Places Tool", func=dining_places_tool, description="Retrieve information about Restaurants, Coffee shops, Bars and other types of dining institutions in Luxembourg.")
]

# Create prompt to direct the agent
custom_prompt = """
You are an assistant that answers the question: {question} by using the most relevant tool.
If the user asks about current weather, ONLY use the Current Weather Tool and no other tool. 
If the user asks about weather forecast, ONLY use the Weather Forecast Tool and no other tool. 
If the user asks about events, activities, concerts etc., ONLY use the Event Tool and no other tool. 
If the user asks about directions, transportation or navigation, ONLY use the Transportation Directions Tool and no other tool.
If the user asks about landmarks, museums, monuments, parks etc. ONLY use the Landmark Tool and no other tool.
If the user asks about coffee shops, restaurant, bars, pubs etc. ONLY use the Dining Places Tool and no other tool.
If none of the tools are useful to answer the query, try to answer from your own knowledge base.
Never mix information from multiple tools UNLESS explicitly asked by the human.
"""

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0.5)

agent = create_react_agent(llm, tools=[current_weather, weather_forecast, transportation_directions, event_tool, landmark_tool, dining_places_tool])

history = ChatMessageHistory()
history.add_ai_message("Hi, ask me anything about places, event, weather or transportation in Luxembourg")
history.add_user_message("Will it rain in luxembourg tomorrow?")

messages = agent.invoke(history)
print(messages['messages'][-1].content)