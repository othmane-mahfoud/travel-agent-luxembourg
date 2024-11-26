from langchain.tools import tool
from vector_store.dining import query_dining_places

@tool
def dining_places_tool(query: str):
    """
    Tool for retrieving detailed dining places information in Luxembourg.

    Parameters:
    - query (str): User query.

    Returns:
    - str: Detailed information about dining places.
    """
    places = query_dining_places(query)
    if places:
        response = "Here are some coffee shops, restaurants, bars, pubs and other dining places in Luxembourg:\n"
        for place in places:
            response += (
                f"- {place.metadata.get('Name')} ({place.metadata.get('Category')}), located at {place.metadata.get('Formatted Address')}."
                f" with a Rating of {place.metadata.get('Rating')}"
                f" with a price level/range of {place.metadata.get('Price')}"
                f" and a tip: '{place.metadata.get('Tips')}'\n"
            )
        return response
    else:
        return "I couldn't find any dining places matching your query."
