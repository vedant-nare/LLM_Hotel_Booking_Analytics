from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np
from transformers import pipeline

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load LLM for answering questions (Change model to any open-source LLM)
qa_pipeline = pipeline("text-generation", model="NousResearch/Llama-2-7b-chat-hf")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Persistent storage
collection = chroma_client.get_or_create_collection(name="bookings")


def ingest_bookings(df):
    """
    Processes a DataFrame of bookings and adds them to ChromaDB as vector embeddings.
    
    Args:
        df (pd.DataFrame): The preprocessed hotel bookings DataFrame.
    """
    if df.empty:
        print("No data available for ingestion.")
        return
    
    # Convert each booking row into a descriptive text
    booking_texts = df.apply(lambda row: f"Booking in {row['country']}, price ${row['adr']}, {'canceled' if row['is_canceled'] else 'not canceled'}", axis=1)
    
    # Convert to list of dictionaries
    booking_data = [{"id": str(idx), "text": text} for idx, text in enumerate(booking_texts)]
    
    # Encode and store in ChromaDB
    for booking in booking_data:
        embedding = model.encode(booking["text"]).tolist()  # Convert numpy array to list
        collection.add(
            ids=[booking["id"]],
            embeddings=[embedding],
            metadatas=[{"text": booking["text"]}]
        )

    print(f"✅ Successfully added {len(booking_data)} bookings to the vector database.")


def search_booking(query: str, df, top_k: int = 3):
    """
    Searches for the most relevant booking details given a query and generates an answer using LLM.

    Args:
        query (str): The user query.
        df (pd.DataFrame): The hotel booking dataset.
        top_k (int): Number of results to retrieve.

    Returns:
        dict: The response from the LLM based on retrieved data.
    """
    if df.empty:
        return {"error": "No booking data available."}

    # Ingest data if not already ingested
    if collection.count() == 0:
        ingest_bookings(df)

    # Encode query into vector
    query_embedding = model.encode(query).tolist()

    # Search for most relevant bookings in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # Extract relevant booking details
    relevant_bookings = [meta["text"] for meta in results["metadatas"][0]] if results["ids"] else []

    # Create a context from retrieved bookings
    context = " ".join(relevant_bookings)

    # Generate an answer using LLM
    prompt = f"Using the following booking data:\n{context}\nAnswer the question: {query}"
    response = qa_pipeline(prompt, max_length=100)[0]["generated_text"]

    return {"question": query, "answer": response, "relevant_data": relevant_bookings}
