# rag_pipeline/rag_chain.py

from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama
from app.services.search_engine import load_vectorstore

def load_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", k=4)
    llm = ChatOllama(model="gemma:2b", temperature=0)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
