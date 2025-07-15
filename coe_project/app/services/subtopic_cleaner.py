import json
import os
import re

def extract_subtopic(question):
    """Naive keyword-based subtopic extractor. Replace with your logic."""
    if not isinstance(question, str):
        return "unknown"

    q_lower = question.lower()
    if "process" in q_lower:
        return "Process"

    elif "architecture" in q_lower:
        return "Architecture"
    elif "memory" in q_lower:
        return "Memory Management"
    else:
        return "General"

def clean_subtopics(
    questions_data,
    output_path="app/data/sample_pdfs/questions.json"
):
    cleaned_questions = []

    for item in questions_data:
        chunk_id = item.get("chunk_id", -1)
        context = item.get("context", "")
        raw_questions = item.get("questions", "")

        if not isinstance(raw_questions, str):
            continue  # Skip malformed entries

        for line in raw_questions.split("\n"):
            question = line.strip()
            if not question:
                continue
            subtopic = extract_subtopic(question)
            cleaned_questions.append({
                "chunk_id": chunk_id,
                "context": context,
                "question": question,
                "subtopic": subtopic
            })

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_questions, f, indent=2, ensure_ascii=False)

    print(f"✅ Cleaned subtopics written to: {output_path}")
    return cleaned_questions
