from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate

llm = ChatOllama(model="gemma:2b", temperature=0.2)

def classify_structure(text: str):
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
Analyze the following academic content and extract its hierarchical structure.
Label each line as Chapter, Topic, Subtopic, Example, or Definition. Use this format:

Chapter: ...
Topic: ...
Subtopic: ...
Definition: ...
Example: ...

Text:
{text}

Output:
"""
    )

    full_prompt = prompt.format(text=text)
    response = llm.invoke(full_prompt)
    return response
