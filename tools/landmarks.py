from langchain.tools import tool
from vector_store.landmarks import query_landmarks

@tool
def landmark_tool(query: str):
    """
    Tool for retrieving detailed information about tourist attractions, landmarks, monuments, parks and views in Luxembourg.

    Parameters:
    - query (str): User query.

    Returns:
    - str: detailed information about tourist attractions, landmarks, monuments, parks and views in Luxembourg
    """
    landmarks = query_landmarks(query)
    if landmarks:
        response = "Here are some tourist attractions in Luxembourg:\n"
        for landmark in landmarks:
            response += (
                f"- {landmark.metadata.get('Name')} ({landmark.metadata.get('Category')}), located at {landmark.metadata.get('Address')}.\n"
                f"  Image URL: {landmark.metadata.get('Image URL', 'No Image Available')}\n"
                f"  Rating: {landmark.metadata.get('Rating')}\n"
                f"  Reviews: {landmark.metadata.get('Reviews')}\n"
            )
        return response
    else:
        return "I couldn't find any landmarks matching your query."
