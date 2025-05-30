import streamlit as st
import sys
import os
from datetime import date

# Make tools importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from feedback.logger import save_feedback
from agents.multi_tool_agent import agent
from dashboards.metrics import show_dashboard
from security.pii_filter import detect_pii
from security.compliance_tagger import flag_compliance_risks

# --- Initialize session ---
if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""
if "answer" not in st.session_state:
    st.session_state["answer"] = ""

# --- Page Setup ---
st.set_page_config(page_title="AllyIn Compass", layout="centered")
st.title("🧭 AllyIn Compass")
st.markdown("Ask your enterprise assistant questions across documents, graphs, and structured data.")

# --- Domain Selection ---
domain = st.selectbox("🌐 Select a domain", ["General", "Finance", "Biotech", "Energy"])
placeholder = f"e.g. What's the latest compliance update in {domain.lower()}?"
user_query = st.text_input("🔍 Ask a question:", value=st.session_state["user_query"])

# --- Optional Reset Button for Testing ---
if st.button("🔄 Reset Session"):
    st.session_state["user_query"] = ""
    st.session_state["answer"] = ""
    st.rerun()

# --- Answer Area ---
if user_query:
    st.session_state["user_query"] = user_query
    print(f"🤖 Agent received question: {user_query}")

    with st.spinner("Thinking..."):
        answer_obj = agent.run(user_query)
        print(answer_obj)
        print("🔍 Type of answer_obj:", type(answer_obj))
        st.session_state["answer"] = answer_obj

    st.markdown("### 🧠 Answer")

    if isinstance(answer_obj, dict):
        formatted_answer = answer_obj.get("answer", "")
        if answer_obj.get("pii"):
            formatted_answer += f"<br><br>⚠️ <b>Warning</b>: Detected PII - {answer_obj['pii']}"
        if answer_obj.get("compliance"):
            formatted_answer += f"<br>⚠️ <b>Risk Alert</b>: Compliance terms found - {answer_obj['compliance']}"
    else:
        formatted_answer = answer_obj.replace("\n", "<br>")
        # Detect PII and compliance from final LLM output
        pii = detect_pii(answer_obj)
        compliance = flag_compliance_risks(answer_obj)
        if pii:
            formatted_answer += f"<br><br>⚠️ <b>Warning</b>: Detected PII - {pii}"
        if compliance:
            formatted_answer += f"<br>⚠️ <b>Risk Alert</b>: Compliance terms found - {compliance}"

    st.markdown(formatted_answer, unsafe_allow_html=True)

    st.markdown("### 🙋 Was this helpful?")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("👍 Yes"):
            save_feedback(user_query, answer_obj, rating=1)
            st.success("Thanks for your feedback!")
            st.rerun()
    with col2:
        if st.button("👎 No"):
            save_feedback(user_query, answer_obj, rating=0)
            st.info("Feedback noted.")
            st.rerun()

# ✅ Show previous answer (if no new query entered)
elif st.session_state["answer"]:
    st.markdown("### 🧠 Last Answer")
    prev = st.session_state["answer"]
    if isinstance(prev, dict):
        formatted_answer = prev.get("answer", "")
        if prev.get("pii"):
            formatted_answer += f"<br><br>⚠️ <b>Warning</b>: Detected PII - {prev['pii']}"
        if prev.get("compliance"):
            formatted_answer += f"<br>⚠️ <b>Risk Alert</b>: Compliance terms found - {prev['compliance']}"
    else:
        formatted_answer = prev.replace("\n", "<br>")
        pii = detect_pii(prev)
        compliance = flag_compliance_risks(prev)
        if pii:
            formatted_answer += f"<br><br>⚠️ <b>Warning</b>: Detected PII - {pii}"
        if compliance:
            formatted_answer += f"<br>⚠️ <b>Risk Alert</b>: Compliance terms found - {compliance}"
    st.markdown(formatted_answer, unsafe_allow_html=True)

# --- Sidebar (Always show observability) ---
with st.sidebar:
    st.markdown("## 🧭 AllyIn Compass")
    st.header("📊 Observability")
    show_dashboard()
