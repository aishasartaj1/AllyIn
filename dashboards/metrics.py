import streamlit as st
import pandas as pd
import json

def load_metrics():
    with open("logs/metrics_log.jsonl") as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines]

def show_dashboard():
    st.subheader("📈 AllyIn Usage Dashboard")

    data = load_metrics()
    if not data:
        st.info("No usage data yet.")
        return

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    # Queries per Day
    st.markdown("#### 📅 Queries Per Day")
    st.bar_chart(df.groupby("date").size())

    st.markdown("---")

    # Tool Usage
    st.markdown("#### 🧰 Tool Usage Frequency")
    st.bar_chart(df["tool"].value_counts())

    st.markdown("---")

    # Response Time
    st.markdown("#### ⏱️ Average Response Time")
    avg_time = df["response_time"].mean()
    st.metric("Avg Response (s)", f"{avg_time:.2f}")
