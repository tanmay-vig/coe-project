from langchain_community.llms import Ollama
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

llm = Ollama(model="llama3.2")

def generate_questions(chunk):
    prompt = f"""
Generate diverse questions from this text chunk. Include:
1. 1 MCQ with 4 options
2. 1 Short answer question
3. 1 Long answer question
4. 1 Numerical problem (if applicable)

For EACH question provide:
- question text (for MCQ, just the stem)
- topic (1-3 words)
- type (mcq/short/long/numerical)
- difficulty (easy/medium/hard)
- cognitive level (remembering/understanding/applying/evaluating)
- For MCQ ONLY: "options" array with exactly 4 choices

Output ONLY as valid JSON array:
[
  {{
    "question": "...",
    "topic": "...",
    "type": "...",
    "difficulty": "...",
    "cognitive_level": "...",
    "options": ["A", "B", "C", "D"]  // ONLY for MCQ
  }}
]

Text Chunk:
{chunk}
"""
    
    response = llm.invoke(prompt)
    try:
        return json.loads(response.strip())
    except:
        return []
    
# chunking
with open("cleaned_content.txt") as f:
    text = f.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", "!"]
)
chunks = splitter.split_text(text)

# question generation
questions = []
for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i+1}/{len(chunks)}")
    question = generate_questions(chunk)
    questions.extend(question)
for question in questions:
    print(question)
with open("questions.json", "w") as f:
    json.dump(questions, f, indent=2)