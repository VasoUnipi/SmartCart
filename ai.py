from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import unicodedata
import re

# Φόρτωση μεταβλητών περιβάλλοντος
load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set.")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"

# Ελάχιστο σύνολο λέξεων που θεωρούμε "έγκυρες" στα Ελληνικά
greek_dictionary = set([
    'φακές', 'σκόρδο', 'ελαιόλαδο', 'σερβίρουμε', 'πιπέρι', 'σέλινο',
    'μπολ', 'βράζουμε', 'νερό', 'ψιλοκομμένο', 'κουταλάκι', 'τηγάνι',
    'αλάτι', 'ντομάτα', 'φέτα', 'ζυμαρικά', 'λαχανικά', 'σάλτσα',
    'πατάτες', 'κρεμμύδι', 'ρύζι', 'τυρί'
])

def is_fake_word(word):
    word = word.lower()
    greek_chars = re.findall(r"[Α-Ωα-ω]", word)
    return len(greek_chars) > 0 and len(word) > 3 and word not in greek_dictionary

def clean_text(text):
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        greek = len(re.findall(r"[Α-Ωα-ω]", line))
        latin = len(re.findall(r"[A-Za-zА-Яа-я]", line))

        if greek < 3 or latin > greek:
            continue

        if any(re.search(pat, line, re.IGNORECASE) for pat in [
            r"\b(necessary|zout|pokud|sous|izmetoume|Sκόρδο|alla|из|einen|αναιμίας|ρεκόρ)\b"
        ]):
            continue

        words_in_line = line.split()
        if sum(is_fake_word(w) for w in words_in_line) > 2:
            continue

        cleaned.append(line)

    return '\n'.join(cleaned)

def query_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Απάντα μόνο στα Ελληνικά, χωρίς καμία λέξη από άλλη γλώσσα."},
            {"role": "user", "content": prompt}
        ]
    }
    res = requests.post(GROQ_API_URL, headers=headers, json=data)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]

def build_prompt(prefix, items):
    return f"{prefix}: {', '.join(items)}.\nΑπάντησε μόνο στα Ελληνικά."

# ENDPOINTS
@app.route("/ai/recipe", methods=["POST"])
def recipe():
    items = request.json.get("products", [])
    prompt = f"""
Δώσε μου μία συνταγή με τα εξής προϊόντα: {', '.join(items)}.
ΜΟΝΟ στα Ελληνικά. Καμία άλλη γλώσσα. Όχι μεταφράσεις ή τίτλους.
Πρώτα Υλικά (σε bullets), μετά Οδηγίες (με 1., 2., 3.)
"""
    response = query_groq(prompt)
    return jsonify({"response": clean_text(response)})

@app.route("/ai/evaluate", methods=["POST"])
def evaluate():
    items = request.json.get("products", [])
    prompt = build_prompt("Αξιολόγησε διατροφικά τα προϊόντα", items)
    return jsonify({"response": clean_text(query_groq(prompt))})

@app.route("/ai/alternatives", methods=["POST"])
def alternatives():
    items = request.json.get("products", [])
    prompt = build_prompt("Πρότεινέ μου πιο υγιεινές εναλλακτικές για", items)
    return jsonify({"response": clean_text(query_groq(prompt))})

@app.route("/ai/mealplan", methods=["POST"])
def mealplan():
    items = request.json.get("products", [])
    prompt = build_prompt("Δώσε ένα εβδομαδιαίο διατροφικό πλάνο βασισμένο στα", items)
    return jsonify({"response": clean_text(query_groq(prompt))})

@app.route("/ai/goal", methods=["POST"])
def goal():
    goal = request.json.get("goal", "")
    prompt = f"Δώσε μου μία λίστα αγορών για τον διατροφικό στόχο: {goal}.\nΜΟΝΟ στα Ελληνικά."
    return jsonify({"response": clean_text(query_groq(prompt))})

@app.route("/ai/eco", methods=["POST"])
def eco():
    items = request.json.get("products", [])
    prompt = build_prompt("Αξιολόγησε περιβαλλοντικά τα εξής προϊόντα", items)
    return jsonify({"response": clean_text(query_groq(prompt))})

@app.route("/ai/combos", methods=["POST"])
def combos():
    items = request.json.get("products", [])
    prompt = build_prompt("Πώς να συνδυάσω τα εξής προϊόντα σε γεύματα", items)
    return jsonify({"response": clean_text(query_groq(prompt))})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
