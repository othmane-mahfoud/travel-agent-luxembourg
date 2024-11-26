import os
import shutil
import pandas as pd

from dotenv import load_dotenv

from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

# Load environment variables
load_dotenv(override=True)

# Load the CSV into a DataFrame
file_path = "data/ticketmaster_events.csv"
events_df = pd.read_csv(file_path, encoding="utf-8")

# Check for missing or malformed data
print(events_df.head())

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
    persist_directory="db/ticketmaster_events"
)

# Persist the vector store
vector_store.persist()

def query_events(query: str):
    """
    Query the vector store to retrieve relevant events.

    Parameters:
    - query (str): User query.

    Returns:
    - list: A list of matching events with metadata.
    """
    # Load the persisted vector store
    vector_store = Chroma(
        persist_directory="db/ticketmaster_events",
        embedding_function=embedding_model
    )
    results = vector_store.similarity_search(query, k=3)  # Retrieve top 5 matches
    return results

# Example query
query = "What concerts are happening in Luxembourg?"
results = query_events(query)

# Display results
for result in results:
    print(f"Event: {result.metadata['Event Name']}")
    print(f"Date: {result.metadata['Start Date']} at {result.metadata['Start Time']}")
    print(f"Venue: {result.metadata['Venue']}, {result.metadata['City']}")
    print(f"Genre: {result.metadata['Genre']} ({result.metadata['Subgenre']})")
    print("---")
    
# for result in results:
#     print(result.metadata.keys())  # Display all metadata keys for each result