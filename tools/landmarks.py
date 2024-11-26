from langchain.tools import tool
from vector_store.landmarks import query_landmarks

@tool
def landmark_tool(query: str):
    """
    Tool for retrieving detailed landmark information in Luxembourg.

    Parameters:
    - query (str): User query.

    Returns:
    - str: Detailed information about landmarks.
    """
    landmarks = query_landmarks(query)
    if landmarks:
        response = "Here are some landmarks in Luxembourg:\n"
        for landmark in landmarks:
            response += (
                f"- {landmark.metadata.get('Name')} ({landmark.metadata.get('Category')}), located at {landmark.metadata.get('Formatted Address')}.\n"
                f"  Description: {landmark.metadata.get('Description')}\n"
                f"  Rating: {landmark.metadata.get('Rating')}\n"
                f"  Tips: {landmark.metadata.get('Tips')}\n"
            )
        return response
    else:
        return "I couldn't find any landmarks matching your query."
