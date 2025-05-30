# AllyIn Compass

A smart enterprise assistant that can answer domain-specific questions using structured SQL data, unstructured documents (like emails and PDFs), and graph databases. Built with LangChain, Streamlit, Neo4j, and DuckDB.

---

## 🚀 Features

* **Multi-modal Querying:** Automatically routes user queries to the best tool (SQL, Vector, or Graph)
* **Compliance & PII Alerts:** Highlights sensitive data or risky terms
* **Dashboard:** Built-in observability for query logging and tool usage
* **Learning Tools:** Includes simulated fine-tuning using LoRA

---

## 📁 Folder Structure

```
AllyIn/
├── agents/                  # Agent logic for tool routing
├── data/                    # Structured CSV + Unstructured docs
├── dashboards/              # Streamlit metrics dashboard
├── feedback/                # Feedback logging
├── notebooks/               # RAG + LoRA experiments
├── security/                # PII + compliance tagging
├── src/retrievers/          # SQL, vector, and graph retrievers
├── ui/                      # Streamlit UI
├── demo_assets/             # Screenshots + demo video
└── README.md
```

---

## 📄 Setup Instructions

```bash
# Clone the repo
https://github.com/aishasartaj1/AllyIn.git

cd AllyIn

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your environment variables (see .env.template)
cp .env.template .env

# Start Streamlit UI
streamlit run ui/app.py
```

---

##  How to Run a Query

1. Launch the Streamlit app.

2. Enter a natural language query like:

  - Top flagged clients in the last year (sql Tool)
  - Which facilities exceed regulations? (Graph Tool)
  - Who is the compliance contact for Plant A? (Vector Tool with PII)
  - Summarize the AllyIn kickoff memo (Vector Tool)

The system selects the correct tool and returns an enriched response.

All queries are automatically routed to the right tool. See observability dashboard for logs.

---

## 🔧 Architecture Diagram

* UI ➔ `ui/app.py`
* Agent ➔ `agents/multi_tool_agent.py`
* Tools ➔ `src/retrievers/`
* Observability ➔ `dashboards/`
* Feedback ➔ `feedback/logger.py`
* PII/Compliance ➔ `security/`

![Architecture](demo_assets/architecture.png)

---

## 🧪 Tech Stack

* **LangChain**: agent logic and tool chaining
* **Streamlit**: frontend UI
* **Neo4j**: knowledge graph for compliance/inspection queries
* **DuckDB**: lightweight SQL engine
* **OpenAI API**: LLM backend

---

## 🤸️‍💻 Learning Outcomes

* **RAG (Retrieval-Augmented Generation):**

  * Found in: `notebooks/rag_baseline.ipynb`
  * Combines document retrieval + generation

* **LoRA (Low-Rank Adaptation):**

  * Found in: `notebooks/models/lora_adapter/`
  * Simulates fine-tuning LLMs with minimal compute

---

## 🎓 Credits

* LangChain
* Streamlit
* Neo4j
* OpenAI

---

## ✉️ License

MIT License - see `LICENSE` file

---

## 🌟 Final Note

This was an amazing learning experience! I explored RAG pipelines, simulated LoRA tuning, built end-to-end tool routing, and strengthened my understanding of observability in AI systems. I also learned I need to dig deeper into **model selection and scaling** — something I'm excited to continue learning.

Thanks for the opportunity!


