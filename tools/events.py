import datetime
from langchain.tools import tool
from vector_store.events import query_events, query_events_in_timeframe

# @tool
# def event_tool(query: str):
#     """
#     Tool to fetch and process event-related queries, including detailed event information.

#     Parameters:
#     - query (str): User's natural language query about events.

#     Returns:
#     - str: A response based on the query.
#     """
#     # Handle specific queries for detailed event information
#     if "more information about" in query.lower():
#         # Extract the event name from the query
#         event_name = query.lower().replace("more information about", "").strip()
#         # Fetch all events with similar names
#         events = query_events(event_name)
#         if events:
#             # Get the first matching event
#             event = events[0]  # Assume the first result is the best match
#             return (
#                 f"{event.metadata['Event Name']} is a {event.metadata['Genre']}/{event.metadata['Subgenre']} "
#                 f"concert that will be taking place at {event.metadata['Venue']}, {event.metadata['Address']} "
#                 f"on {event.metadata['Start Date']} at {event.metadata['Start Time']}."
#             )
#         else:
#             return f"I couldn't find any specific information about {event_name}."

#     # Handle time-bound queries (this week, tomorrow, this weekend)
#     elif "this week" in query.lower():
#         # Define the start and end of the week
#         today = datetime.date.today()
#         end_of_week = today + datetime.timedelta(days=(6 - today.weekday()))
#         events = query_events_in_timeframe(today.isoformat(), end_of_week.isoformat())
#         if events:
#             response = "This week there are the following events:\n"
#             response += ", ".join(f"{event.metadata['Event Name']}" for event in events)
#             return response
#         else:
#             return "There are no events scheduled for this week."

#     elif "tomorrow" in query.lower():
#         # Define tomorrow's date
#         today = datetime.date.today()
#         tomorrow = today + datetime.timedelta(days=1)
#         events = query_events_in_timeframe(tomorrow.isoformat(), tomorrow.isoformat())
#         if events:
#             response = "Tomorrow there are the following events:\n"
#             response += ", ".join(f"{event.metadata['Event Name']}" for event in events)
#             return response
#         else:
#             return "There are no events scheduled for tomorrow."

#     elif "this weekend" in query.lower():
#         # Define the weekend's start and end dates
#         today = datetime.date.today()
#         saturday = today + datetime.timedelta(days=(5 - today.weekday()))
#         sunday = saturday + datetime.timedelta(days=1)
#         events = query_events_in_timeframe(saturday.isoformat(), sunday.isoformat())
#         if events:
#             response = "This weekend there are the following events:\n"
#             response += ", ".join(f"{event.metadata['Event Name']}" for event in events)
#             return response
#         else:
#             return "There are no events scheduled for this weekend."

#     # Handle general queries about upcoming events
#     else:
#         events = query_events(query)
#         if events:
#             response = "There are many upcoming events in Luxembourg, such as:\n"
#             response += ", ".join(f"{event.metadata['Event Name']}" for event in events[:5])  # Limit to 5 events
#             return response
#         else:
#             return "I couldn't find any upcoming events in Luxembourg."

@tool
def event_tool(query: str):
    """
    tool for event-related queries which provides detailed event information
    about event such as name start date/time, genre, venue and address.

    Parameters:
    - query (str): User's query about events in general or a specific event.

    Returns:
    - str: A detailed response containing event information.
    """

    events = query_events(query)
    if events:
        response = "Here are some upcoming events in Luxembourg:\n"
        for event in events:
            response += (
                f"- {event.metadata['Event Name']} on {event.metadata['Start Date']} at {event.metadata['Start Time']} "
                    f"({event.metadata.get('Genre')}/{event.metadata.get('Subgenre')}), at {event.metadata['Venue']}, {event.metadata['Address']} "
                        f"with the description: {event.metadata.get('Description')} "
                            f"Image of the event: {event.metadata.get('Image URL')} \n"
            )
        return response
    else:
        return "I couldn't find any events matching your query."
