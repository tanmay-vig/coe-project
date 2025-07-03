import json
import re
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from .subtopics import clean_subtopics

# Load model
llm = Ollama(model="llama3")

# Prompt Template
template = """
You are a question generation expert.

Given the context of a subject, generate well-structured academic questions of different marks: 
1 mark, 2 mark, 3 mark, and 5 mark questions.

Make sure questions are meaningful, clear, and directly based on the content.
Use Bloom’s taxonomy cognitive levels (remembering, understanding, applying, analyzing, evaluating, creating).

Include a variety of question types (MCQ, short, descriptive, numerical).
Avoid repetition or malformed questions.
Return the output in this JSON format:

{{
  "1_mark": [{{ "question": "...", "topic": "...", "subtopic": "...", "question_type": "...", "difficulty_level": "...", "time": "...", "cognitive_level": "...", "marks": 1, "image": null }}],
  "2_mark": [{{ ... }}],
  "3_mark": [{{ ... }}],
  "5_mark": [{{ ... }}]
}}

Context:
---------
{text}
---------
"""

prompt = PromptTemplate(template=template, input_variables=["text"])
parser = JsonOutputParser()

def extract_json_from_response(response: str):
    # Extract the first {...} block from the response
    try:
        json_str = re.search(r"{.*}", response, re.DOTALL).group(0)
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Invalid json output: {response.strip()}")

chain = (
    {"text": RunnablePassthrough()}
    | prompt
    | llm
    | RunnableLambda(extract_json_from_response)
)

# 🔹 Updated text chunking (smaller size, more overlap)
def chunk_text(text: str, chunk_size=800, chunk_overlap=200) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

# 🔹 Filter invalid / bad questions
def filter_questions(data):
    clean_data = {"1_mark": [], "2_mark": [], "3_mark": [], "5_mark": []}
    for section in clean_data:
        for q in data.get(section, []):
            question = q.get("question", "").strip()
            if (
                len(question) > 10 and
                not any(junk in question.lower() for junk in ["????", "mcq for the mcq", "''''", "true", "false", "importance of a factual mcq"]) and
                not re.match(r"^[^a-zA-Z0-9]*$", question) and
                ("?" in question or question.lower().startswith(("explain", "discuss", "justify", "design", "describe", "analyze", "compare", "evaluate", "derive", "calculate", "contrast", "apply", "remembering", "understanding", "applying", "analyzing", "evaluating", "creating", "design", "creating", "designing"))) and
                len(question.split()) > 4
            ):
                clean_data[section].append(q)
    return clean_data

# 🔹 Main generation
def generate_questions(text):
    chunks = chunk_text(text)
    all_questions = {"1_mark": [], "2_mark": [], "3_mark": [], "5_mark": []}

    print(f"🔍 Generating questions from {len(chunks)} chunks...")
    for idx, chunk in enumerate(chunks):
        print(f"➡️  Processing chunk {idx + 1}/{len(chunks)} (Length: {len(chunk)} chars)")
        try:
            result = chain.invoke(chunk)
            print(f"📦 Raw output for chunk {idx+1}:\n", json.dumps(result, indent=2))

            filtered = filter_questions(result)
            for mark in all_questions:
                all_questions[mark].extend(filtered.get(mark, []))
        except Exception as e:
            print(f"⚠️  Error in chunk {idx + 1}: {e}")

    with open("output_questions.json", "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print("✅ Saved structured questions to output_questions.json")

def run_question_generation(input_path="C:\\Users\\hp\\projects\\Question_Generator\\Data_Preprocessing\\extracted_text.txt", output_path="output_questions.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    generate_questions(text)
    clean_subtopics(
        input_file=output_path,
        output_file=output_path
    )
    print("✅ Question generation completed successfully!")


# 🔹 Entry point
if __name__ == "__main__":
    with open("C:\\Users\\hp\\projects\\Question_Generator\\Data_Preprocessing\\extracted_text.txt", "r", encoding="utf-8") as f:
        content = f.read()
    generate_questions(content)

    clean_subtopics(
        input_file="output_questions.json",
        output_file="output_questions.json"
    )

    print("✅ Question generation completed successfully!")