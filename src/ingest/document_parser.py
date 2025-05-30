import os
import json
import fitz
from email import message_from_file

def parse_pdf(path):
    with fitz.open(path) as doc:
        return "".join([page.get_text() for page in doc])

def parse_eml(path):
    with open(path, "r", encoding="utf-8") as f:
        msg = message_from_file(f)
        subject = msg.get("Subject", "")
        body = msg.get_payload()
        return f"Subject: {subject}\n\nBody: {body}"

output = []
folder = "data/unstructured"

for file in os.listdir(folder):
    path = os.path.join(folder, file)
    if file.endswith(".pdf"):
        text = parse_pdf(path)
        output.append({"text": text})
    elif file.endswith(".eml"):
        text = parse_eml(path)
        output.append({"text": text})

with open("data/unstructured/parsed.jsonl", "w", encoding="utf-8") as out:
    for doc in output:
        json.dump(doc, out)
        out.write("\n")

print("Parsed data saved to parsed.jsonl")
