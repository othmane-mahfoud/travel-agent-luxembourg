import datetime
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from tools.weather import current_weather, weather_forecast
from tools.navigation import transportation_directions
from tools.events import event_tool
from tools.landmarks import landmark_tool

# Define the tools
tools = [
    Tool(name="Current Weather", func=current_weather, description="Get the current weather in Luxembourg."),
    Tool(name="Weather Forecast", func=weather_forecast, description="Get the 5-day weather forecast in Luxembourg."),
    Tool(name="Transportation Directions", func=transportation_directions, description="Provide directions using the Mobiliteit API."),
    Tool(name="Event Tool", func=event_tool, description="Provide information about events in Luxembourg."),
    Tool(name="Landmark Tool", func=landmark_tool, description="Retrieve information about landmarks and monuments in Luxembourg.")
]

# Initialize the chat model
chat = ChatOpenAI(temperature=0)

# Create prompt to direct the agent
custom_prompt = f"""
You are an assistant that answers user questions by using the most relevant tool. 
You must know that today is {datetime.date.today()}.
If the user asks about current weather, ONLY use the Current Weather Tool and no other tool. 
If the user asks about weather forecast, ONLY use the Weather Forecast Tool and no other tool. 
If the user asks about events, activities, concerts etc., ONLY use the Event Tool and no other tool. 
If the user asks about directions, transportation or navigation, ONLY use the Transportation Directions Tool and no other tool.
If the user asks about landmarks, museums, monuments, parks etc. ONLY use the Landmark Tool and no other tool.
If none of the tools are useful to answer the query, try to answer from your own knowledge base.
Never mix information from multiple tools UNLESS explicitly asked by the human.
"""

# Create the agent with the tools
agent = initialize_agent(tools, chat, agent="zero-shot-react-description", verbose=True, prefix=custom_prompt)

# Test the agent
query = "Can you give me some tips about Pont Grande-Duchesse Charlotte"
response = agent.invoke(query)
print("Agent Response:", response)