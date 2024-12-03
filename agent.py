import os
import datetime
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from tools.weather import current_weather, weather_forecast
from tools.navigation import transportation_directions, get_nearby_stops_tool
from tools.events import event_tool
from tools.landmarks import landmark_tool
from tools.dining import dining_places_tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2=os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT=os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT=os.getenv("LANGCHAIN_PROJECT")

# Define tools
tools = [
    Tool(name="current_weather", func=current_weather, description="Get the current weather in Luxembourg."),
    Tool(name="weather_forecast", func=weather_forecast, description="Get the 5-day weather forecast in Luxembourg."),
    Tool(name="transportation_directions", func=transportation_directions, description="Provide directions using the Mobiliteit API."),
    Tool(name="find_stops", func=get_nearby_stops_tool, description="Automatically retrieves nearby stops and available transportation without requiring location input."),
    Tool(name="event_tool", func=event_tool, description="Provide information about events in Luxembourg."),
    Tool(name="landmark_tool", func=landmark_tool, description="Retrieve information about landmarks and monuments in Luxembourg."),
    Tool(name="dining_places_tool", func=dining_places_tool, description="Retrieve information about restaurants, coffee shops, bars, pubs, and other dining institutions in Luxembourg.")
]

# Create prompt to guide the agent
custom_prompt = """
You are an assistant that answers user questions by using the most relevant tool.
You must answer accurately based on today's date: {today_date}.
If the user asks about current weather, ONLY use the Current Weather Tool and no other tool.
If the user asks about weather forecast, ONLY use the Weather Forecast Tool and no other tool.
If the user asks about events, activities, concerts etc., ONLY use the Event Tool and no other tool.
If the user asks about directions, transportation, or navigation, ONLY use the Transportation Directions Tool and no other tool.
If the user asks about landmarks, museums, monuments, parks, etc., ONLY use the Landmark Tool and no other tool.
If the user asks about coffee shops, restaurants, bars, pubs, etc., ONLY use the Dining Places Tool and no other tool.
Never mix information from multiple tools UNLESS explicitly asked by the human.
"""

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0.5)

# Initialize the agent
agent = create_react_agent(llm, tools=tools)

# Initialize conversation history
history = ChatMessageHistory()

if __name__ == "__main__":
    # Start the chatbot interaction
    print("Hi! Ask me anything about places, events, weather, or transportation in Luxembourg. Type 'bye!' to exit.")

    # Interactive loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye!":
            print("AI: Goodbye! Have a great day!")
            break

        # Add user's message to history
        history.add_user_message(user_input)

        # Use the agent to generate a response
        try:
            messages = agent.invoke(history)
            ai_response = messages["messages"][-1].content
            print(f"AI: {ai_response}")

            # Add AI's response to history
            history.add_ai_message(ai_response)
        except Exception as e:
            print(f"AI: Sorry, I encountered an error: {e}")
