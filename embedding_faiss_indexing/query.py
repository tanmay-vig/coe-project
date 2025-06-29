from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="llama3.2")

def search_questions(query, topic=None, difficulty=None):
    db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    
    filters = {}
    if topic: filters["topic"] = topic
    if difficulty: filters["difficulty"] = difficulty
    
    results = db.similarity_search(query, filter=filters, k=10)
    
    for res in results:
        print(f"Question: {res.page_content}")
        print(f"Metadata: {res.metadata}\n")
#  search
search_questions("what are two types of register and their functions?",difficulty="hard")
print("\n---\n")
print("----------------------------")
search_questions(" memory managment" , difficulty="hard")