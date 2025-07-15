# app/services/search_engine.py

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from app.utils.filter_utils import smart_filter

# === Load FAISS VectorStore ===
def load_vectorstore(path="app/data/faiss_index/"):
    embeddings = OllamaEmbeddings(model="gemma:2b")
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

# === Smart Search with Filtering ===
def search_questions(query, top_k=10, filters=None):
    """
    Perform semantic search on embedded questions and apply optional metadata filtering.

    Args:
        query (str): Search query
        top_k (int): Number of top similar results to retrieve
        filters (dict): Optional filters like marks, difficulty_level, cognitive_level

    Returns:
        List of matched question documents with metadata
    """
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", k=top_k)
    similar_docs = retriever.get_relevant_documents(query)

    if filters:
        return smart_filter(similar_docs, filters)
    return [{"question": doc.page_content, "meta": doc.metadata} for doc in similar_docs]


# === Filtering Logic ===
def smart_filter(docs, filters):
    """Filter questions based on marks, difficulty level, and cognitive level (if provided)."""
    target_marks = filters.get("marks")
    target_difficulty = filters.get("difficulty_level", "").lower()
    target_cognitive = filters.get("cognitive_level", "").lower()

    exact = [
        doc for doc in docs
        if doc.metadata.get("marks") == target_marks
        and doc.metadata.get("difficulty_level", "").lower() == target_difficulty
        and doc.metadata.get("cognitive_level", "").lower() == target_cognitive
    ]
    if exact:
        return exact

    fallback = [
        doc for doc in docs
        if doc.metadata.get("difficulty_level", "").lower() == target_difficulty
    ]
    if fallback:
        return fallback

    return docs[:3]  # Default: top 3 results as fallback
