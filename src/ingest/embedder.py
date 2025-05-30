import json
import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
import numpy as np

# Load parsed JSONL
with open("data/unstructured/parsed.jsonl", "r", encoding="utf-8") as f:
    docs = [json.loads(line)["text"] for line in f]

# Chunk documents by paragraphs (basic split)
chunks = []
for doc in docs:
    parts = doc.split("\n\n")
    chunks.extend([p.strip() for p in parts if len(p.strip()) > 0])

print(f"📄 Total text chunks to embed: {len(chunks)}")

# Load sentence-transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks, convert_to_numpy=True)

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Create collection
collection_name = "docs"
vector_size = embeddings.shape[1]
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
)

# Prepare points for upload
points = [
    models.PointStruct(
        id=str(uuid.uuid4()),
        vector=vec.tolist(),
        payload={"text": chunk}
    )
    for vec, chunk in zip(embeddings, chunks)
]

# Upload to Qdrant
client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"✅ Successfully uploaded {len(points)} embedded chunks to Qdrant.")
