from flask import Flask, request, jsonify
import google.generativeai as genai
import numpy as np
import faiss


genai.configure(api_key="g_api")  


documents = [
    "Apples are a healthy fruit.",
    "Cats are very cute and independent animals.",
    "Python is an easy-to-learn programming language.",
    "Dogs are loyal pets and love humans.",
    "Google Gemini is a generative AI model."
]

def get_embedding(text):
    response = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    return response['embedding']

embeddings = [get_embedding(doc) for doc in documents]
embedding_array = np.array(embeddings).astype('float32')

dimension = embedding_array.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embedding_array)


app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h2>Gemini Vector Store Search</h2>
        <form method="POST" action="/search">
            <input name="query" placeholder="Enter your query" style="width:300px">
            <input type="submit" value="Search">
        </form>
    '''

@app.route('/search', methods=['POST'])
def search():
    user_query = request.form.get("query")

   
    query_embedding = get_embedding(user_query)
    query_vector = np.array([query_embedding]).astype('float32')

    
    k = 3
    distances, indices = index.search(query_vector, k)
    results = [documents[i] for i in indices[0]]

    
    html_result = f"<h3>Top Results for: '{user_query}'</h3><ul>"
    for res in results:
        html_result += f"<li>{res}</li>"
    html_result += "</ul><a href='/'>Go Back</a>"

    return html_result

if __name__ == '__main__':
    app.run(debug=True)
