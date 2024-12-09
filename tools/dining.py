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
        response = "Here are some restaurants, coffee shops, bars, pubs and other dining places in Luxembourg:\n"
        for place in places:
            response += (
                f"- {place.metadata.get('Name')} ({place.metadata.get('Category')}), located at {place.metadata.get('Formatted Address')}. "
                f"with the Image URL {place.metadata.get('Image URL')}"
                f"with a Rating of {place.metadata.get('Rating')} "
                f"with a price level/range of {place.metadata.get('Price Level')} "
                f"with the following reviews: '{place.metadata.get('Reviews')}'\n"
            )
        return response
    else:
        return "I couldn't find any dining places matching your query."
