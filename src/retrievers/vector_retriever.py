from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Connect to Qdrant (running locally)
client = QdrantClient(host="localhost", port=6333)

# Load the same embedding model used in Day 3
model = SentenceTransformer("all-MiniLM-L6-v2")

def vector_search(query, top_k=3):
    # Convert query to vector
    query_vector = model.encode(query).tolist()
    
    # Search Qdrant
    hits = client.search(
        collection_name="docs",
        query_vector=query_vector,
        limit=top_k
    )
    
    # Return matching texts
    return [hit.payload["text"] for hit in hits]

if __name__ == "__main__":
    query = "What documents talk about emissions or compliance?"
    print(f"\n🔍 Vector search for: {query}\n")
    results = vector_search(query)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r}\n{'-'*80}")
