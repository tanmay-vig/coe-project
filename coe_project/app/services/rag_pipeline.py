# app/services/rag_pipeline.py

from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda

# === Load VectorStore ===
def load_vectorstore(path="app/data/faiss_index/"):
    embeddings = OllamaEmbeddings(model="llama3")
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

# === Build RAG Chain ===
def load_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", k=4)
    llm = ChatOllama(model="llama3", temperature=0)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# === Optional: LangGraph wrapper ===
def build_rag_graph(rag_chain):
    builder = StateGraph()

    def run_rag(state):
        query = state["query"]
        result = rag_chain.invoke(query)
        return {"response": result["result"]}

    builder.add_node("query", RunnableLambda(run_rag))
    builder.set_entry_point("query")
    builder.add_edge("query", "END")
    return builder.compile()
