from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
from security.pii_filter import detect_pii
from security.compliance_tagger import flag_compliance_risks
from feedback.logger import log_query_event
import os
import time

# Load .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load models and clients
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host="localhost", port=6333)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

def rag_answer_vector(user_query: str, top_k: int = 3) -> str:
    # Step 1: Embed the query
    query_vector = embedding_model.encode(user_query).tolist()

    # Step 2: Retrieve top-k chunks
    hits = client.search(collection_name="docs", query_vector=query_vector, limit=top_k)
    context_chunks = [hit.payload["text"] for hit in hits]
    context = "\n---\n".join(context_chunks)

    # Step 3: Build prompt
    prompt = f"""Use the following context to answer the question.
If the answer is not present in the context, say "I don't know".

Context:
{context}

Question: {user_query}
Answer:"""

    # Step 4: Generate answer (timed)
    start_time = time.time()
    response = llm.invoke(prompt).content
    elapsed_time = time.time() - start_time

    # Step 5: Apply security filters
    pii = detect_pii(response)
    risks = flag_compliance_risks(response)

    if pii or risks:
        response += "\n\n⚠️ **Security Warning**:\n"
        if pii:
            response += f"- Detected PII: {list(pii.keys())}\n"
        if risks:
            response += f"- Compliance Risk Terms: {risks}\n"

    # Step 6: Log the query event
    log_query_event(user_query, tool_used="vector", response_time=elapsed_time)

    return response

