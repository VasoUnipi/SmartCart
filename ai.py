from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import unicodedata
import re
import nltk
from nltk.corpus import words
import re
nltk.download('words')


def is_fake_word(word):
    greek_chars = re.findall(r"[Α-Ωα-ω]", word)
    if not greek_chars:
        return False
    return len(word) > 3 and word.lower() not in greek_dictionary

# Αντικατάστησε αυτό με δικό σου ελληνικό λεξικό (λίστα λέξεων)
greek_dictionary = set([
    'φακές', 'σκόρδο', 'ελαιόλαδο', 'σερβίρουμε', 'πιπέρι', 'σέλινο',
    'μπολ', 'βράζουμε', 'χρόνος', 'νερό', 'κουταλάκι', 'ψιλοκομμένο', 'φύλλο'
])

def aggressive_clean_response(text):
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        greek_count = len(re.findall(r"[Α-Ωα-ω]", line))
        foreign_count = len(re.findall(r"[A-Za-zА-Яа-я]", line))

        # Αν έχει λίγα ελληνικά γράμματα ή πολλά ξένα → skip
        if greek_count < 3 or foreign_count > greek_count:
            continue

        # Skip αν έχει λέξεις που δείχνουν "χαλασμένη έξοδο"
        if re.search(r"(einen|zout|izmetoume|necessary|pokud|sous|из|alledas|Sκόρδο|alla|шоко)", line, re.IGNORECASE):
            continue

        # Skip αν έχει πολλές "απίθανες" λέξεις
        words_in_line = line.split()
        fake_words = sum(is_fake_word(w) for w in words_in_line)
        if fake_words > 2:
            continue

        cleaned.append(line)

    return '\n'.join(cleaned)


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
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Αν περιέχει περισσότερα ξένα γράμματα από ελληνικά, πετά το
        greek_count = len(re.findall(r"[Α-Ωα-ω]", line))
        foreign_count = len(re.findall(r"[A-Za-zА-Яа-я]", line))
        if foreign_count > greek_count:
            continue

        # Αν περιέχει "εικονικά" συστατικά (π.χ. Sκόρδοallas, izmetoume), πετά το
        if re.search(r"(alledas|einen|из|necessary|izmetoume|pokud|zout|sous)", line, re.IGNORECASE):
            continue

        cleaned.append(line)

    return '\n'.join(cleaned)



def groq_request(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
    "model": GROQ_MODEL,
    "messages": [
        {
            "role": "system",
            "content": "Μίλα μόνο ελληνικά. Μην χρησιμοποιήσεις λέξεις από άλλες γλώσσες. Απόφυγε εφευρεμένες λέξεις ή λέξεις που δεν είναι μέρος της ελληνικής."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
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
    prompt = f"""
    Δώσε μου μία απλή συνταγή με τα εξής προϊόντα: {', '.join(items)}.

    Πολύ σημαντικό:
    Χρησιμοποίησε **αποκλειστικά** την ελληνική γλώσσα.
    **Απαγόρευονται** λέξεις στα αγγλικά, γερμανικά ή άλλες γλώσσες.
    Μην εφευρίσκεις λέξεις ή χρησιμοποιείς ανορθόγραφες λέξεις.
    Χρησιμοποίησε μόνο καθημερινά, πραγματικά ελληνικά υλικά.

    Δώσε πρώτα τα Υλικά (σε κουκκίδες), μετά τις Οδηγίες (αριθμημένες).

    Παράδειγμα μορφοποίησης:

    Υλικά:
    - 2 αυγά
    - 100γρ φέτα
    - 1 ντομάτα

    Οδηγίες:
    1. Χτυπάμε τα αυγά σε ένα μπολ.
    2. Προσθέτουμε την φέτα και την ντομάτα ψιλοκομμένη.
    3. Ψήνουμε σε αντικολλητικό τηγάνι για 5 λεπτά.

    ΜΗΝ προσθέσεις κανένα επιπλέον σχόλιο, τίτλο ή εξήγηση.
    ΠΡΟΣΟΧΗ: Μην προσθέσεις τίτλο, εισαγωγή, σχόλια ή μετάφραση. Μόνο τη συνταγή.
    """

    result = groq_request(prompt)
    return jsonify({"response": aggressive_clean_response(result)})


@app.route("/ai/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    items = data.get("products", [])
    prompt = f"Αξιολόγησε διατροφικά τα παρακάτω προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": aggressive_clean_response(result)})


@app.route("/ai/alternatives", methods=["POST"])
def alternatives():
    data = request.json
    items = data.get("products", [])
    prompt = f"Πρότεινέ μου πιο υγιεινές εναλλακτικές για τα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": aggressive_clean_response(result)})


@app.route("/ai/mealplan", methods=["POST"])
def mealplan():
    data = request.json
    items = data.get("products", [])
    prompt = f"Δημιούργησε ένα εβδομαδιαίο διατροφικό πλάνο βασισμένο στα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": aggressive_clean_response(result)})


@app.route("/ai/goal", methods=["POST"])
def goal():
    data = request.json
    goal = data.get("goal", "")
    prompt = f"Πρότεινέ μου μία λίστα αγορών για τον εξής διατροφικό στόχο: {goal}."
    result = groq_request(prompt)
    return jsonify({"response": aggressive_clean_response(result)})


@app.route("/ai/eco", methods=["POST"])
def eco():
    data = request.json
    items = data.get("products", [])
    prompt = f"Αξιολόγησε περιβαλλοντικά τα εξής προϊόντα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": aggressive_clean_response(result)})


@app.route("/ai/combos", methods=["POST"])
def combos():
    data = request.json
    items = data.get("products", [])
    prompt = f"Πρότεινέ μου πώς να συνδυάσω τα εξής προϊόντα σε γεύματα ή πακέτα: {', '.join(items)}."
    result = groq_request(prompt)
    return jsonify({"response": aggressive_clean_response(result)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
