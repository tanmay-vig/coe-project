def search_questions(query=None, marks=None, difficulty=None, cognitive_level=None):
    from langchain_community.vectorstores import FAISS
    from langchain_ollama import OllamaEmbeddings

    if not any([query, marks, difficulty, cognitive_level]):
        print("❌ Please provide at least one of: query, marks, difficulty, or cognitive_level.")
        return

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = FAISS.load_local("faiss_index_ollama", embeddings, allow_dangerous_deserialization=True)

    # Use vector search if query is provided, else get all docs (limited)
    if query:
        docs = db.similarity_search(query, k=20)
    else:
        docs = db.similarity_search("general", k=50)  # fallback search with dummy keyword

    def match(doc):
        if marks is not None and doc.metadata.get("marks") != int(marks):
            return False
        if difficulty and doc.metadata.get("difficulty_level", "").lower() != difficulty.lower():
            return False
        if cognitive_level and doc.metadata.get("cognitive_level", "").lower() != cognitive_level.lower():
            return False
        return True

    filtered = [d for d in docs if match(d)]

    if not filtered:
        print("⚠️ No exact match found. Showing top similar questions.")
        filtered = docs[:5]

    print(f"\n🎯 Showing {len(filtered)} question(s):\n")
    for doc in filtered:
        metadata = doc.metadata
        print(f"❓ Question: {doc.page_content}")
        print(f"🏷️  Topic: {metadata.get('topic', 'unknown')}")
        print(f"🔹 Subtopic: {metadata.get('subtopic', 'unknown')}")
        print(f"🎯 Marks: {metadata.get('marks', '?')}")
        print(f"📈 Difficulty: {metadata.get('difficulty_level', 'unknown')}")
        print(f"🧠 Cognitive Level: {metadata.get('cognitive_level', 'unknown')}")
        print("-" * 60)

# Example usage
if __name__ == "__main__":
    print("🔍 Welcome to Question Search")
    q = input("Enter query (optional): ").strip()
    m = input("Enter marks (optional): ").strip()
    d = input("Enter difficulty level (optional): ").strip()
    c = input("Enter cognitive level (optional): ").strip()

    search_questions(
        query=q if q else None,
        marks=int(m) if m.isdigit() else None,
        difficulty=d if d else None,
        cognitive_level=c if c else None
    )
