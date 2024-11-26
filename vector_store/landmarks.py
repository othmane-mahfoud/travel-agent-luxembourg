import os
import shutil
import pandas as pd
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Load the CSV into a DataFrame
file_path = "data/foursquare_landmarks.csv"
landmarks_df = pd.read_csv(file_path, encoding="utf-8")

# Create Documents with metadata for ChromaDB
documents = []
for _, row in landmarks_df.iterrows():
    metadata = {
        "FSQ_ID": row["FSQ_ID"],
        "Name": row["Name"],
        "Category": row["Category"],
        "Icon": row["Icon"],
        "Latitude": row["Latitude"],
        "Longitude": row["Longitude"],
        "Region": row["Region"],
        "Formatted Address": row["Formatted Address"],
        "Description": row["Description"],
        "Phone Number": row["Phone Number"],
        "Rating": row["Rating"],
        "Price": row["Price"],
        "Tips": row["Tips"]
    }
    page_content = f"{row['Name']} - {row['Category']} located at {row['Formatted Address']} with a rating of {row['Rating']}. {row['Description']}."
    documents.append(Document(page_content=page_content, metadata=metadata))

# Initialize OpenAI embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.getenv("OPENAI_API_KEY"))

# Delete the existing vector store directory if it exists
persist_dir = "db/foursquare_landmarks"
if os.path.exists(persist_dir):
    shutil.rmtree(persist_dir)

# Create ChromaDB vector store
vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory=persist_dir
)

print("Landmark vector store created and persisted.")

def query_landmarks(query: str):
    """
    Query the vector store to retrieve landmark details.

    Parameters:
    - query (str): User query about landmarks.

    Returns:
    - list: A list of matching landmarks with metadata.
    """
    vector_store = Chroma(
        persist_directory="db/foursquare_landmarks",
        embedding_function=embedding_model
    )
    results = vector_store.similarity_search(query, k=50) 
    return results

