import json
import re
import os

def extract_subtopic(text):
    # Try extracting from markdown bold (e.g., **Neural Networks**)
    match = re.search(r"\*\*([^\*]+)\*\*", text)
    if match:
        return match.group(1).strip()
    
    # Try extracting from quotes (e.g., "Backpropagation")
    match = re.search(r'"([^"]+)"', text)
    if match:
        return match.group(1).strip()
    
    # Try extracting from common phrasing patterns
    match = re.search(r"subtopic (is|would be|for this question would be)[:\s]*([A-Za-z \-/()]+)", text, re.IGNORECASE)
    if match:
        return match.group(2).strip()

    # Default fallback: if short text, treat it as the subtopic
    return text.strip() if len(text.split()) <= 4 else "General"

def clean_subtopics(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for marks_key, questions in data.items():
        for q in questions:
            original = q.get("subtopic", "")
            q["subtopic"] = extract_subtopic(original)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Cleaned subtopics saved to: {output_file}")

if __name__ == "__main__":
    clean_subtopics(
        input_file="output/output_questions.json",
        output_file="output/questions.json"
    )
