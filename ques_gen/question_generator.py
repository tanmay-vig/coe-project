import json
import random
from transformers import pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

# Load question generator model
question_gen = pipeline("text2text-generation", model="iarfmoose/t5-base-question-generator")

# Load subtopic predictor model
llm = Ollama(model="llama3")
output_parser = StrOutputParser()

# Prompt template for subtopic prediction
subtopic_prompt = PromptTemplate.from_template("""
Given the subject: {topic}
And the question: "{question}"

What is the best subtopic this question belongs to?
Respond with a short academic subtopic label like "Neural Networks", "Backpropagation", etc.
""")
subtopic_chain = subtopic_prompt | llm | output_parser

# Metadata presets for each marks category
MARKS_META = {
    1: {"question_type": "mcq", "difficulty_level": "easy", "time": "1 min", "cognitive_level": "remembering"},
    2: {"question_type": "short", "difficulty_level": "medium", "time": "2-3 min", "cognitive_level": "understanding"},
    3: {"question_type": "descriptive", "difficulty_level": "medium", "time": "4-5 min", "cognitive_level": "applying"},
    5: {"question_type": "long", "difficulty_level": "hard", "time": "6-10 min", "cognitive_level": "evaluating"}
}

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

# Basic validation to filter poor questions
def is_valid_question(q):
    q = q.lower().strip()
    return len(q) > 10 and not any(bad in q for bad in ["true", "false", "not_entailment", "entailment"])

# Rule-based topic detection (based on keywords)
def detect_topic(text, topic_keywords):
    for topic, keywords in topic_keywords.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                return topic
    return "General"

# Save questions to PDF
def save_questions_to_pdf(data, pdf_path="output/questions.pdf"):
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    elements = []

    for marks_group in data.values():
        for q in marks_group:
            elements.append(Paragraph(f"<b>Question:</b> {q['question']}", styles["Normal"]))
            elements.append(Paragraph(f"Topic: {q['topic']} | Subtopic: {q['subtopic']}", styles["Normal"]))
            elements.append(Paragraph(f"Marks: {q['marks']} | Type: {q['question_type']} | Difficulty: {q['difficulty_level']} | Time: {q['time']} | Cognitive: {q['cognitive_level']}", styles["Normal"]))
            elements.append(Spacer(1, 12))

    doc.build(elements)
    print(f"📄 Questions saved as PDF at {pdf_path}")

# Main generation function
def generate_questions(text, topic_keywords, selected_topic, questions_per_category=5):
    chunks = splitter.split_text(text)
    seen_questions = set()
    used_chunks = set()
    marks_buckets = {1: [], 2: [], 3: [], 5: []}

    for marks in [1, 2, 3, 5]:
        while len(marks_buckets[marks]) < questions_per_category and len(used_chunks) < len(chunks):
            chunk = random.choice(chunks)
            if chunk in used_chunks:
                continue
            used_chunks.add(chunk)

            prompt = f"""Generate a {MARKS_META[marks]["difficulty_level"]} level {MARKS_META[marks]["question_type"]} question from the following content for {marks} marks:  {chunk}"""
            result = question_gen(prompt, max_length=200, do_sample=False)
            question = result[0]['generated_text'].strip()

            if not is_valid_question(question) or question in seen_questions:
                continue
            seen_questions.add(question)

            topic = selected_topic or detect_topic(chunk, topic_keywords)
            subtopic = subtopic_chain.invoke({"topic": topic, "question": question}).strip()

            question_json = {
                "question": question,
                "topic": topic,
                "subtopic": subtopic,
                "question_type": MARKS_META[marks]["question_type"],
                "difficulty_level": MARKS_META[marks]["difficulty_level"],
                "time": MARKS_META[marks]["time"],
                "cognitive_level": MARKS_META[marks]["cognitive_level"],
                "marks": marks,
                "image": None
            }

            marks_buckets[marks].append(question_json)

    return marks_buckets

# Save questions to JSON
def save_questions(output, filename="output/output_questions.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved structured questions to {filename}")

# Entry point
if __name__ == "__main__":
    # Ask user for topic
    user_topic = input("📚 Enter the topic you want to generate questions on (or leave blank to auto-detect): ").strip()

    # Read refined text
    with open("output/refined_output.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # Read keyword mapping
    with open("ques_gen/keyword.json", "r", encoding="utf-8") as kf:
        topic_keywords = json.load(kf)

    print("🚀 Generating questions with subtopics...")
    final_questions = generate_questions(text, topic_keywords, selected_topic=user_topic)
    save_questions(final_questions)
    save_questions_to_pdf(final_questions)
    print("✅ Question generation completed successfully!")
