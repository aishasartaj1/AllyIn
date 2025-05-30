from rag_tool import rag_answer_vector

query = "What is mentioned about emissions in the company documents?"
response = rag_answer_vector(query)
print("\n🧠 RAG Answer:\n", response)
