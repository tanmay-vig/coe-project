from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOllama
from app.services.search_engine import load_vectorstore

def get_conversational_chain():
    # Load vector DB
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", k=5)

    # Use Ollama (gemma2:b) as local chat model
    llm = ChatOllama(model="gemma:2b", temperature=0)

    # Build conversational chain
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
