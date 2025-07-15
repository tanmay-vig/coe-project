from langchain_ollama import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Define the conversational LLM (change model if needed)
llm = ChatOllama(model="gemma:2b", temperature=0.2)

# Create a memory buffer to store chat history
memory = ConversationBufferMemory()

# Create a basic conversational chain
conversation_chain = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

def get_conversational_chain():
    return conversation_chain
