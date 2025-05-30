import re

def detect_pii(text):
    """Detects emails, phone numbers, and SSNs in the input text."""

    patterns = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "phone": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    }

    findings = {}

    for label, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            findings[label] = matches

    return findings

if __name__ == "__main__":
    sample_text = """
        Contact John at john.doe@example.com or (123) 456-7890.
        His SSN is 123-45-6789.
    """
    result = detect_pii(sample_text)
    print("Detected PII:", result)
