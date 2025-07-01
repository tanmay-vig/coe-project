import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.documents import Document

# Search configuration
INDEX_PATH = os.path.join("Vector_Store", "faiss_index_ollama")
EMBEDDING_MODEL = "llama3"  # Replace with smaller model if needed

def load_vectorstore(index_path):
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

def print_results(results):
    if not results:
        print("❌ No matching questions found.")
        return
    print(f"\n🔍 Top {len(results)} Matching Questions:\n")
    for i, r in enumerate(results, 1):
        meta = r.metadata
        print(f"{i}. {r.page_content}")
        print(f"   🧠 Topic: {meta.get('topic')} | Subtopic: {meta.get('subtopic')} | Marks: {meta.get('marks')} | Type: {meta.get('type')}")
        print(f"   💡 Difficulty: {meta.get('difficulty')} | Time: {meta.get('time')} | Cognitive: {meta.get('cognitive')}\n")

if __name__ == "__main__":
    print("🔄 Loading vector store...")
    db = load_vectorstore(INDEX_PATH)

    while True:
        user_query = input("💬 Enter your question or concept to search (or type 'exit'): ").strip()
        if user_query.lower() == "exit":
            break

        print("🔎 Searching...\n")
        results = db.similarity_search(user_query, k=5)
        print_results(results)
