from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "mixtral-8x7b-32768"

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

@app.route("/ai/recipe", methods=["POST"])
def recipe():
    data = request.json
    items = data.get("products", [])
    prompt = f"Δώσε μου μια συνταγή που περιλαμβάνει τα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": result})

@app.route("/ai/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    items = data.get("products", [])
    prompt = f"Αξιολόγησε διατροφικά τα παρακάτω προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": result})

@app.route("/ai/alternatives", methods=["POST"])
def alternatives():
    data = request.json
    items = data.get("products", [])
    prompt = f"Πρότεινέ μου πιο υγιεινές εναλλακτικές για τα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": result})

@app.route("/ai/mealplan", methods=["POST"])
def mealplan():
    data = request.json
    items = data.get("products", [])
    prompt = f"Δημιούργησε ένα εβδομαδιαίο διατροφικό πλάνο βασισμένο στα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": result})

@app.route("/ai/goal", methods=["POST"])
def goal():
    data = request.json
    goal = data.get("goal", "")
    prompt = f"Πρότεινέ μου μία λίστα αγορών για τον εξής διατροφικό στόχο: {goal}."
    result = groq_request(prompt)
    return jsonify({"response": result})

@app.route("/ai/eco", methods=["POST"])
def eco():
    data = request.json
    items = data.get("products", [])
    prompt = f"Αξιολόγησε περιβαλλοντικά τα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": result})

@app.route("/ai/combos", methods=["POST"])
def combos():
    data = request.json
    items = data.get("products", [])
    prompt = f"Πρότεινέ μου πώς να συνδυάσω τα εξής προϊόντα σε γεύματα ή πακέτα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
