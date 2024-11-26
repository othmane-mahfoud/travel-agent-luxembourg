from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI
from tools.weather import current_weather, weather_forecast
from tools.navigation import transportation_directions

# Define the tools
tools = [
    Tool(name="Current Weather", func=current_weather, description="Get the current weather in Luxembourg."),
    Tool(name="Weather Forecast", func=weather_forecast, description="Get the 5-day weather forecast in Luxembourg."),
    Tool(name="Transportation Directions", func=transportation_directions, description="Provide directions using the Mobiliteit API.")
]

# Initialize the chat model
chat = ChatOpenAI(temperature=0.7)

# Create the agent with the tools
agent = initialize_agent(tools, chat, agent="zero-shot-react-description", verbose=True)

# Example usage
query_1 = "How can I go from Porte des Sciences to Luxembourg Monterey?"
query_2 = "What is the weather right now in Luxembourg?"

response_1 = agent.run(query_1)
response_2 = agent.run(query_2)

print("Agent Response 1:", response_1)
print("Agent Response 2:", response_2)