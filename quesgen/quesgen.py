from flask import Flask
import google.generativeai as genai
import pickle
import os
import traceback




genai.configure(api_key="AIzaSyDITxfnFKTWI6aIt3jwmdaGfa-_xDO9BEI")

app = Flask(__name__)



@app.route('/')
def home():
    return '''
    <h2>Gemini Question Generator</h2>
    <p><a href="/generate-questions">📚 Generate Questions from Your Saved Embeddings</a></p>
    '''

@app.route('/generate-questions')
def generate_questions():
    if not os.path.exists("stored.pkl"):
        return "<h3> 'stored_embeddings.pkl' not found. Please save your embeddings first.</h3>"


    with open("stored.pkl", "rb") as f:
        data = pickle.load(f)
        documents = data.get("docs", [])

    if not documents:
        return "<h3>⚠️ No documents found inside the embeddings file.</h3>"

  
    combined_text = "\n".join(documents)[:3000]

    prompt = f"""
    Generate 5 quiz-style or educational questions based on this content:

    {combined_text}
    """

    try:
        model = genai.GenerativeModel(model_name="models/gemini-pro")

        response = model.generate_content(prompt)
        questions = response.text.split("\n")
    except Exception as e:
       return f"<h3> Gemini API Error:</h3><pre>{traceback.format_exc()}</pre>"


    html = "<h2>📘 Questions Generated from Your Data</h2><ul>"
    for q in questions:
        if q.strip():
            html += f"<li>{q.strip()}</li>"
    html += "</ul><a href='/'>⬅ Back to Home</a>"

    return html

if __name__ == '__main__':
    app.run(debug=True)
