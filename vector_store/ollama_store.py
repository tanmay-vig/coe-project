import json
import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

def load_questions(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    for marks_group in data.values():
        for q in marks_group:
            metadata = {
                "topic": q.get("topic"),
                "subtopic": q.get("subtopic"),
                "marks": q.get("marks"),
                "type": q.get("question_type"),
                "difficulty": q.get("difficulty_level"),
                "time": q.get("time"),
                "cognitive": q.get("cognitive_level")
            }
            docs.append(Document(page_content=q["question"], metadata=metadata))
    return docs

if __name__ == "__main__":
    json_path = os.path.join("output", "questions.json")
    save_path = os.path.join("Vector_Store", "faiss_index_ollama")

    print("📦 Loading questions and creating vector embeddings...")

    docs = load_questions(json_path)
    embeddings = OllamaEmbeddings(model="llama3")  # You can change model here
    vectorstore = FAISS.from_documents(docs, embeddings)

    vectorstore.save_local(save_path)

    print(f"✅ Vector store saved to: {save_path}")
