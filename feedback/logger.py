import time
import json
from datetime import datetime

def save_feedback(query: str, answer: str, rating: int):
    log = {
        "query": query,
        "answer": answer,
        "rating": rating  # 1 = 👍, 0 = 👎
    }
    with open("feedback_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log) + "\n")


def log_query_event(query: str, tool_used: str, response_time: float):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "tool": tool_used,
        "response_time": round(response_time, 3)
    }
    with open("logs/metrics_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
