from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from tools.weather import current_weather, weather_forecast

# Define the tools
tools = [
    Tool(name="Current Weather", func=current_weather, description="Get the current weather in Luxembourg."),
    Tool(name="Weather Forecast", func=weather_forecast, description="Get the 5-day weather forecast in Luxembourg.")
]

# Initialize the chat model
chat = ChatOpenAI(temperature=0.7)

# Create the agent with the tools
agent = initialize_agent(tools, chat, agent="zero-shot-react-description", verbose=True)

# Example usage
query_1 = "What is the weather right now in Luxembourg?"
query_2 = "Will it be raining tomorrow in Luxembourg?"

response_1 = agent.run(query_1)
response_2 = agent.run(query_2)

print("Agent Response 1:", response_1)
print("Agent Response 2:", response_2)