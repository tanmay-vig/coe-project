import json
import re

def extract_label(text):
    """
    Extract a clean topic or subtopic name from verbose LLM output.
    Prioritizes markdown bold (**...**), quoted ("..."), or patterns like 'The answer is: ...'
    """
    if not text:
        text = "General"
    text = text.strip()

    # Try to extract markdown bold **Physics**
    match = re.search(r"\*\*([^*]+)\*\*", text)
    if match:
        return match.group(1).strip()

    # Try quoted topic: "Physics" or 'Physics'
    match = re.search(r'"([^"]+)"', text)
    if match:
        return match.group(1).strip()
    match = re.search(r"'([^']+)'", text)
    if match:
        return match.group(1).strip()

    # Try patterns like: The answer is: Physics
    match = re.search(r"[Tt]he answer (is|would be)[\s:]*([A-Za-z /&\-()]+)", text)
    if match:
        return match.group(2).strip()

    # Try subtopic sentence pattern
    match = re.search(r"best subtopic.*?\s*[:\-]*\s*\**([A-Za-z0-9 \-/&()]+)\**", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Fallback: use if short enough
    return text if len(text.split()) <= 4 else "General"

def clean_subtopics(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for marks_key, questions in data.items():
        for q in questions:
            raw_topic = q.get("topic", "")
            raw_subtopic = q.get("subtopic", "")
            q["topic"] = extract_label(raw_topic)
            q["subtopic"] = extract_label(raw_subtopic)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Cleaned topics and subtopics saved to: {output_file}")

if __name__ == "__main__":
    clean_subtopics(
        input_file="C:\\Users\\hp\\projects\\Question_Generator\\Data_Preprocessing\\output_questions.json",
        output_file="output_questions.json"
    )
