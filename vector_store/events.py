import os
import shutil
import pandas as pd
from datetime import datetime

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv(override=True)

# Load the CSV into a DataFrame
file_path = "data/ticketmaster_events.csv"
events_df = pd.read_csv(file_path, encoding="utf-8")

# Create Documents with metadata for ChromaDB
documents = []
for _, row in events_df.iterrows():
    metadata = {
        "Event Name": row["Event Name"],
        "Image URL": row["Image URL"],
        "Start Date": row["Start Date"],
        "Start Time": row["Start Time"],
        "Genre": row["Genre"],
        "Subgenre": row["Subgenre"],
        "Venue": row["Venue"],
        "City": row["City"],
        "Address": row["Address"]
    }
    page_content = f"{row['Event Name']} at {row['Venue']} in {row['City']} on {row['Start Date']} at {row['Start Time']}. {row['Genre']} - {row['Subgenre']}."
    documents.append(Document(page_content=page_content, metadata=metadata))

# Initialize OpenAI embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.getenv("OPENAI_API_KEY"))

# Delete the existing vector store directory if it exists
persist_dir = "db/ticketmaster_events"
if os.path.exists(persist_dir):
    shutil.rmtree(persist_dir)

# Create ChromaDB vector store
vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory=persist_dir
)

# Function to query all events
def query_events(query: str):
    """
    Query the vector store to retrieve events.

    Parameters:
    - query (str): User query.

    Returns:
    - list: A list of matching events with metadata.
    """
    # Load the persisted vector store
    vector_store = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )
    results = vector_store.similarity_search(query, k=50)
    return results


def query_events_in_timeframe(start_date: str, end_date: str):
    """
    Query the vector store to retrieve events within a specific timeframe.

    Parameters:
    - start_date (str): The start date in YYYY-MM-DD format.
    - end_date (str): The end date in YYYY-MM-DD format.

    Returns:
    - list: A list of events within the timeframe.
    """
    # Convert input dates to datetime objects
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

    # Load the persisted vector store
    vector_store = Chroma(
        persist_directory="db/ticketmaster_events",
        embedding_function=embedding_model
    )

    # Retrieve a smaller subset of events directly related to the query
    results = vector_store.similarity_search("events in Luxembourg", k=50)  # Limit initial results

    # Filter events by date
    filtered_events = [
        result for result in results
        if start_date_obj <= datetime.strptime(result.metadata["Start Date"], "%Y-%m-%d") <= end_date_obj
    ]

    return filtered_events


# Example usage
if __name__ == "__main__":
    # Query for top 3 matches
    query = "What concerts are happening in Luxembourg?"
    top_events = query_events(query)
    print("Top 3 Events:")
    for event in top_events:
        print(f"- {event.metadata['Event Name']} on {event.metadata['Start Date']}")

    # Query for events in a timeframe
    start_date = "2024-11-26"
    end_date = "2024-12-02"
    timeframe_events = query_events_in_timeframe(start_date, end_date)
    print("\nEvents in Timeframe:")
    for event in timeframe_events:
        print(f"- {event.metadata['Event Name']} on {event.metadata['Start Date']} at {event.metadata['Start Time']}")