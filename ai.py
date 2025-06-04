from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import unicodedata

# Φόρτωσε τοπικά τις μεταβλητές περιβάλλοντος
load_dotenv()

app = Flask(__name__)

# Πάρε το API key από το περιβάλλον χωρίς default τιμή
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"


def clean_response(text):
    def is_valid_word(word):
        for char in word:
            if not (
                'Α' <= char <= 'Ω' or 'α' <= char <= 'ω' or
                'A' <= char <= 'Z' or 'a' <= char <= 'z' or
                char.isdigit() or
                char in " \n\r\t.,;:!?()[]{}'\"-%*/+=–—" or
                unicodedata.category(char).startswith('Z')
            ):
                return False
        return True
    cleaned_words = [word for word in text.split() if is_valid_word(word)]
    return ' '.join(cleaned_words)

def groq_request(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def format_prompt(main_prompt):
    return main_prompt.strip() + "\n\nΑπάντησε μόνο στα Ελληνικά χωρίς λέξεις από άλλες γλώσσες."

@app.route("/ai/recipe", methods=["POST"])
def recipe():
    data = request.json
    items = data.get("products", [])
    prompt = f"Δώσε μου μια συνταγή που περιλαμβάνει τα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": clean_response(result)})

@app.route("/ai/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    items = data.get("products", [])
    prompt = f"Αξιολόγησε διατροφικά τα παρακάτω προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": clean_response(result)})

@app.route("/ai/alternatives", methods=["POST"])
def alternatives():
    data = request.json
    items = data.get("products", [])
    prompt = f"Πρότεινέ μου πιο υγιεινές εναλλακτικές για τα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": clean_response(result)})

@app.route("/ai/mealplan", methods=["POST"])
def mealplan():
    data = request.json
    items = data.get("products", [])
    prompt = f"Δημιούργησε ένα εβδομαδιαίο διατροφικό πλάνο βασισμένο στα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": clean_response(result)})

@app.route("/ai/goal", methods=["POST"])
def goal():
    data = request.json
    goal = data.get("goal", "")
    prompt = f"Πρότεινέ μου μία λίστα αγορών για τον εξής διατροφικό στόχο: {goal}."
    result = groq_request(prompt)
    return jsonify({"response": clean_response(result)})

@app.route("/ai/eco", methods=["POST"])
def eco():
    data = request.json
    items = data.get("products", [])
    prompt = f"Αξιολόγησε περιβαλλοντικά τα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": clean_response(result)})

@app.route("/ai/combos", methods=["POST"])
def combos():
    data = request.json
    items = data.get("products", [])
    prompt = f"Πρότεινέ μου πώς να συνδυάσω τα εξής προϊόντα σε γεύματα ή πακέτα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": clean_response(result)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
