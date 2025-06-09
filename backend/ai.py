import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("GROQ_API_KEY")

# MongoDB setup
client = MongoClient("mongodb://mongo:27017/")
db = client.smartcart

@app.route("/ai/analyze/<user_id>", methods=["GET"])
def analyze_cart(user_id):
    cart_items = list(db.carts.find({"user_id": user_id}))
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    product_names = [item['name'] for item in cart_items if 'name' in item]

    prompt = f"""
    Analyze the following products:
    {', '.join(product_names)}

    1. Are they vegan or vegetarian?
    2. Provide dietary information (e.g., calories, sugar, fat, etc.).
    3. Suggest 3 similar healthier alternatives.
    4. Suggest 2 recipes using the items in the cart.
    """

    try:
        response = openai.ChatCompletion.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful nutrition assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response["choices"][0]["message"]["content"]
        return jsonify({"analysis": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
