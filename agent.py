import datetime
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from tools.weather import current_weather, weather_forecast
from tools.navigation import transportation_directions
from tools.events import event_tool

# Define the tools
tools = [
    Tool(name="Current Weather", func=current_weather, description="Get the current weather in Luxembourg."),
    Tool(name="Weather Forecast", func=weather_forecast, description="Get the 5-day weather forecast in Luxembourg."),
    Tool(name="Transportation Directions", func=transportation_directions, description="Provide directions using the Mobiliteit API."),
    Tool(name="Event Tool", func=event_tool, description="Provide information about events in Luxembourg.")
]

# Initialize the chat model
chat = ChatOpenAI(temperature=0)

# Create prompt to direct the agent
custom_prompt = f"""
You are an assistant that answers user questions by using the most relevant tool. 
You must know that today is {datetime.date.today()}.
If the user asks about current weather, use the Current Weather Tool. 
If the user asks about weather forecast, use the Weather Forecast Tool. 
If the user asks about events, activities, concerts etc., use the Event Tool. 
If the user asks about directions, transportation or navigation, use the Transportation Directions Tool.
If none of the tools are useful to answer the query, try to answer from your own knowledge base.
Do not mix information unless explicitly asked.
"""

# Create the agent with the tools
agent = initialize_agent(tools, chat, agent="zero-shot-react-description", verbose=True, prefix=custom_prompt)

# Test the agent
query = "what is today's date?"
response = agent.invoke(query)
print("Agent Response:", response)