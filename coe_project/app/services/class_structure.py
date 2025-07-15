# app/services/class_structure.py

from app.utils.structure_parser import classify_structure

def parse_structure(text: str):
    """
    Extracts the class structure (Chapter, Topic, Subtopic, etc.) from raw OCR text.
    """
    return classify_structure(text)
