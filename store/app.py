from flask import Flask, request, jsonify
import google.generativeai as genai
import numpy as np
import faiss
import PyPDF2
import pandas as pd
import os





genai.configure(api_key="g_api") 

app = Flask(__name__)



def load_documents():
    docs = []

    if os.path.exists("data.pdf"):
        # Read PDF
        with open("data.pdf", "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    docs.extend(text.split("\n"))

    elif os.path.exists("data.csv"):
        # Read CSV
        df = pd.read_csv("data.csv")
        for col in df.columns:
            docs.extend(df[col].dropna().astype(str).tolist())

    else:
        docs.append("No PDF or CSV found!")

    return [d.strip() for d in docs if d.strip()]



def get_embedding(text):
    response = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    return response['embedding']


documents = load_documents()
embeddings = [get_embedding(doc) for doc in documents]
embedding_array = np.array(embeddings).astype('float32')
dimension = embedding_array.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embedding_array)



@app.route('/')
def home():
    return '''
        <h2>Search from PDF/CSV</h2>
        <form method="POST" action="/search">
            <input name="query" placeholder="Enter your query" style="width:300px">
            <input type="submit" value="Search">
        </form>
    '''

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get("query")
    query_embedding = get_embedding(query)
    query_vector = np.array([query_embedding]).astype('float32')

    k = 3
    distances, indices = index.search(query_vector, k)
    results = [documents[i] for i in indices[0]]

    html_result = f"<h3>Top Matches for: '{query}'</h3><ul>"
    for r in results:
        html_result += f"<li>{r}</li>"
    html_result += "</ul><a href='/'>Go back</a>"

    return html_result

if __name__ == '__main__':
    app.run(debug=True)
