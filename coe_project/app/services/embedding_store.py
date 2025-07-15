import os
import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema import Document
from langchain_ollama import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="gemma:2b")



# === Load questions from questions.json ===
def load_questions(file_path="app/data/questions.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    # Check format: Flat list or marks-grouped
    if isinstance(data, list):
        for item in data:
            docs.append(
                Document(
                    page_content=item.get("questions", ""),
                    metadata={
                        "topic": item.get("topic", "unknown"),
                        "subtopic": item.get("subtopic", "unknown"),
                        "marks": item.get("marks", 0),
                        "type": item.get("question_type", "unknown"),
                        "difficulty_level": item.get("difficulty_level", "unknown"),
                        "cognitive_level": item.get("cognitive_level", "unknown"),
                        "time": item.get("time", "unknown"),
                        "chunk_id": item.get("chunk_id", -1)
                    }
                )
            )
    else:
        # old grouped format (e.g., { "2": [ {...}, {...} ] })
        for mark_group, questions in data.items():
            for q in questions:
                docs.append(
                    Document(
                        page_content=q.get("question", ""),
                        metadata={
                            "topic": q.get("topic", "unknown"),
                            "subtopic": q.get("subtopic", "unknown"),
                            "marks": q.get("marks", 0),
                            "type": q.get("question_type", "unknown"),
                            "difficulty_level": q.get("difficulty_level", "unknown"),
                            "cognitive_level": q.get("cognitive_level", "unknown"),
                            "time": q.get("time", "unknown")
                        }
                    )
                )
    return docs


# === Store documents into FAISS vectorstore ===
def store_in_faiss(docs, index_path="app/data/faiss_index"):  # ✅ Renamed function
    if os.path.exists(os.path.join(index_path, "index.faiss")):
        print(f"🔄 FAISS index already exists at {index_path}. Skipping rebuild.")
        return

    print("⚙️ Creating FAISS index using Ollama embeddings...")
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(index_path)
    print(f"✅ Stored FAISS index at: {index_path}")


# === Optional standalone run ===
if __name__ == "__main__":
    questions = load_questions("app/data/questions.json")
    store_in_faiss(questions)  # ✅ Matches renamed function
