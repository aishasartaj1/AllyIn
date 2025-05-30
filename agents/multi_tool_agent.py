from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
import sys
import os
import datetime
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variable
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load the model
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

# --- Define your tools ---
from src.retrievers.vector_retriever import vector_search
from src.retrievers.sql_retriever import query_sql
from src.retrievers.graph_retriever import run_cypher_query
from feedback.logger import log_query_event
from security.pii_filter import detect_pii
from security.compliance_tagger import flag_compliance_risks

tool_log = []

@tool
def vector_tool(query: str) -> dict:
    """Use this tool to search unstructured data like PDFs and emails."""
    timestamp = datetime.datetime.now()
    print(f"[{timestamp}] Used vector_tool for: {query}")
    tool_log.append((timestamp, "vector_tool", query))

    start = time.time()
    results = vector_search(query)
    elapsed = time.time() - start

    log_query_event(query, tool_used="vector", response_time=elapsed)

    joined_results = "\n".join(results)
    pii = detect_pii(joined_results)
    compliance = flag_compliance_risks(joined_results)

    return {
        "answer": f"Based on the unstructured data, here's what I found:<br>{joined_results.replace('\n', '<br>')}",
        "pii": pii,
        "compliance": compliance
    }

@tool
def sql_tool(query: str) -> dict:
    """Use this tool to query structured data like customers, orders, amounts."""
    timestamp = datetime.datetime.now()
    print(f"[{timestamp}] Used sql_tool for: {query}")
    tool_log.append((timestamp, "sql_tool", query))

    start = time.time()
    results = query_sql(query)
    elapsed = time.time() - start

    log_query_event(query, tool_used="sql", response_time=elapsed)

    if isinstance(results, list):
        joined = "\n".join(results)
    else:
        joined = str(results)

    pii = detect_pii(joined)
    compliance = flag_compliance_risks(joined)

    return {
        "answer": f"Here are the results from the structured data:<br>{joined.replace('\n', '<br>')}",
        "pii": pii,
        "compliance": compliance
    }

@tool
def graph_tool(query: str) -> dict:
    """Use this tool for questions that require graph queries."""
    timestamp = datetime.datetime.now()
    print(f"[{timestamp}] Used graph_tool for: {query}")
    tool_log.append((timestamp, "graph_tool", query))

    cypher_prompt = f"""
You are a helpful assistant that translates natural language questions into Cypher queries for Neo4j.

The Neo4j schema contains:
- (Facility)-[:EXCEEDS]->(Regulation)
- (Facility)-[:COMPLIES_WITH]->(Regulation)
- (Facility)-[:INSPECTED_BY]->(Agency)
- (Agency)-[:FLAGS]->(Facility)

Translate the following question into a Cypher query. Only return the Cypher code. Do not explain.

Question: {query}
"""
    cypher_query = llm.invoke(cypher_prompt).content
    print(f"[{timestamp}] Translated Cypher:\n{cypher_query}")

    try:
        start = time.time()
        results = run_cypher_query(cypher_query)
        elapsed = time.time() - start
        log_query_event(query, tool_used="graph", response_time=elapsed)

        return {
            "answer": f"From the knowledge graph, I found the following:<br>{str(results).replace('\n', '<br>')}",
            "pii": {},
            "compliance": []
        }

    except Exception as e:
        return {
            "answer": f"⚠️ Cypher execution failed: {str(e)}",
            "pii": {},
            "compliance": []
        }

# Initialize tools
tools = [vector_tool, sql_tool, graph_tool]

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# Manual test
if __name__ == "__main__":
    question = "What facilities exceed regulations?"
    print("\n🧠 Asking:", question)
    response = agent.run(question)
    print("\n📝 Response:\n", response)

    print("\n🧾 Tool Call Summary:")
    for t in tool_log:
        print(f"{t[0]} | {t[1]} | Query: {t[2]}")

    print("\n🔎 Testing PII detection with vector tool:")
    test_query = "Who is the compliance contact for Plant A?"
    response = vector_tool.invoke({"query": test_query})
    print("\n📝 Vector Tool Response:\n", response)

    print("\n🔍 Manual vector_tool test:")
    test_query = "Plant A compliance contact"
    response = vector_tool.invoke({"query": test_query})
    print("\n📝 Vector Tool Response:\n", response)
