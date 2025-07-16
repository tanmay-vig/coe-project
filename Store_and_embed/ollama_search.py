import json

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
        difficulty_value = (
            doc.metadata.get("difficulty_level") 
            or doc.metadata.get("difficulty") 
            or ""
        ).lower()
        if difficulty and difficulty_value != difficulty.lower():
            return False
        if cognitive_level and doc.metadata.get("cognitive_level", "").lower() != cognitive_level.lower():
            return False
        return True

    filtered = [d for d in docs if match(d)]

    if not filtered:
        print("⚠️ No exact match found. Showing top similar questions.")
        filtered = docs[:5]

    print(f"\n🎯 Showing {len(filtered)} question(s):\n")

    results = []

    for doc in filtered:
        metadata = doc.metadata
        # DEBUGGING
        # print("DEBUG metadata:", metadata)
        difficulty_value = (
            doc.metadata.get("difficulty_level") 
            or doc.metadata.get("difficulty") 
            or ""
        )
        question_info = {
            "question": doc.page_content,
            "topic": metadata.get("topic", "unknown"),
            "subtopic": metadata.get("subtopic", "unknown"),
            "marks": metadata.get("marks", "?"),
            "difficulty_level": difficulty_value.capitalize(),
            "cognitive_level": metadata.get("cognitive_level", "unknown")
        }
        results.append(question_info)

        # Print to console
        print(f"❓ Question: {question_info['question']}")
        print(f"🏷️  Topic: {question_info['topic']}")
        print(f"🔹 Subtopic: {question_info['subtopic']}")
        print(f"🎯 Marks: {question_info['marks']}")
        print(f"📈 Difficulty: {question_info['difficulty_level']}")
        print(f"🧠 Cognitive Level: {question_info['cognitive_level']}")
        print("-" * 60)

    # Combine search parameters and results
    output = {
        "search_parameters": {
            "query": query,
            "marks": marks,
            "difficulty": difficulty,
            "cognitive_level": cognitive_level
        },
        "results": results
    }

    # Save to JSON file
    with open("search_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Results saved to 'search_results.json'.")

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
