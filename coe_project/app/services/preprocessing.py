# app/services/preprocessing.py

import re

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing unwanted characters and extra whitespace.
    You can expand this with more cleaning logic if needed.
    """
    if not text:
        return ""

    # Remove multiple spaces, newlines, and special chars
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,;!?]', '', text)
    return text.strip()

