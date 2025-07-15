# app/services/question_gen.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import os

from langchain_ollama import ChatOllama
ollama_llm = ChatOllama(model="gemma:2b")  # ✅ Using original gemma:2b model

def split_text_into_chunks(text, chunk_size=500, chunk_overlap=50):
    """Split long text into smaller chunks for better LLM input."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.create_documents([text])

def generate_questions_from_chunks(chunks):
    """Use Ollama to generate questions for each chunk."""
    questions = []
    for i, chunk in enumerate(chunks):
        prompt = f"Generate exam-style questions based on the following academic content:\n\n{chunk.page_content}"
        try:
            output = ollama_llm.invoke(prompt)  # This returns an AIMessage
            questions.append({
                "chunk_id": i,
                "context": chunk.page_content,
                "questions": output.content.strip()  # ✅ Fix is here
            })
        except Exception as e:
            questions.append({
                "chunk_id": i,
                "context": chunk.page_content,
                "error": str(e)
            })
    return questions


def save_questions_to_json(questions, out_path="app/data/sample_pdfs/questions.json"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

def process_text_to_questions(text):
    chunks = split_text_into_chunks(text)
    print(f"📚 Number of Chunks: {len(chunks)}")

    questions = generate_questions_from_chunks(chunks)
    print(f"✅ Total Questions Extracted: {len(questions)}")
    if questions:
        print("🧪 Sample Question:", questions[0])

    save_questions_to_json(questions)
    return questions
