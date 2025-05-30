from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOpenAI
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from feedback.logger import log_query_event

# Updated table info with DuckDB-compatible interval syntax
custom_table_info = {
    "flags": """
    client_id: ID of the flagged client
    flag_type: type of issue (e.g., restatement, audit_issue)
    date: when the client was flagged

    Use this table for audit issues or clients flagged in specific time windows.
    For time filters, use:
        WHERE date >= CURRENT_DATE - INTERVAL '12 months'
    """,
    "customers": """
    customer_id: unique customer ID
    name: client name
    country: client's country
    JOIN customers.customer_id = flags.client_id
    """,
    "orders": """
    order_id: ID of the order
    customer_id: client placing the order
    amount: value of the order
    """
}

# Connect to DuckDB with schema + guidance
db = SQLDatabase.from_uri(
    "duckdb:///data/structured/data.duckdb",
    include_tables=["customers", "orders", "flags"],
    sample_rows_in_table_info=2,
    custom_table_info=custom_table_info,
)

# LLM setup
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Create the SQL Agent
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)

def query_sql(question: str):
    start = time.time()
    result = agent_executor.run(question)
    elapsed = time.time() - start
    log_query_event(question, tool_used="sql", response_time=elapsed)
    return result

if __name__ == "__main__":
    print("🔎 Example query: Top flagged clients in last year")
    print(query_sql("Which clients were flagged for restatements in the past 12 months?"))
