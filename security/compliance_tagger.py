def flag_compliance_risks(text):
    """Flags risky compliance-related terms in the given text."""

    risk_terms = [
        "restatement",
        "earnings risk",
        "lawsuit",
        "regulatory breach",
        "whistleblower",
        "non-compliance",
        "audit failure",
        "penalty",
        "violation"
    ]

    found_terms = [term for term in risk_terms if term.lower() in text.lower()]

    return found_terms

if __name__ == "__main__":
    sample_text = """
        The company faces an earnings risk due to audit failure and a potential whistleblower report.
    """
    result = flag_compliance_risks(sample_text)
    print("⚠️ Risk terms detected:", result)

