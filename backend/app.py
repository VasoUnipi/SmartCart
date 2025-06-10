#Αρχιτεκτονική backend για το SmartCart app
#Αυτό το αρχείο περιέχει τον κύριο κώδικα της εφαρμογής Flask που διαχειρίζεται τα αιτήματα και τις λειτουργίες του SmartCart app.
#Εισαγωγή των απαραίτητων βιβλιοθηκών και ρυθμίσεων για την εφαρμογή Flask
#Εισαγωγή του blueprint για το scraping
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId #Το ObjectId χρειάζεται για αλληλεπίδραση με MongoDB
from datetime import datetime
from pymongo import ASCENDING, DESCENDING
from scraping import scraping_bp
import os
import openai

app = Flask(__name__)
app.register_blueprint(scraping_bp)
#Καθορισμός της σύνδεσης με τη βάση δεδομένων MongoDB
# Χρησιμοποιείται το PyMongo για να συνδεθούμε με τη βάση δεδομένων MongoDB
app.config['MONGO_URI'] = 'mongodb://mongo:27017/smartcart'
mongo = PyMongo(app)

# Ρύθμιση του OpenAI API για χρήση με Groq
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"  # Groq-compatible

#------HOMEPAGE------
# Route: Home page
@app.route('/')
def home():
    return "🚀 Το SmartCart app τρέχει σωστά!"
#Δημιουργία endpoint για την προβολή όλων των προϊόντων
@app.route('/products', methods=['GET'])
#Ανάκτηση φίλτρων αναζήτησης από το URL
def get_products():
    name = request.args.get('name')
    category = request.args.get('category')
    max_price = request.args.get('price')
    order_by = request.args.get('order_by')  # <-- add this
#Δημιουργία ερωτήματος για αναζήτηση προϊόντων ανεξαρτήτως πεζών και κεφαλαίων
    query = {}
    if name:
        query['name'] = {'$regex': name, '$options': 'i'}
    if category:
        query['category'] = {'$regex': category, '$options': 'i'}
    if max_price:
        try:
            query['price'] = {'$lte': float(max_price)}
        except ValueError:
            pass

    # Map the order_by parameter to pymongo sorting
    sort = None
    if order_by == "price_asc":
        sort = [("price", ASCENDING)]
    elif order_by == "price_desc":
        sort = [("price", DESCENDING)]
    elif order_by == "name_asc":
        sort = [("name", ASCENDING)]
    elif order_by == "name_desc":
        sort = [("name", DESCENDING)]

    if sort:
    #Εκτέλεση αναζήτησης στη βάση δεδομένων MongoDB με ταξινόμηση
        products = list(mongo.db.products.find(query).sort(sort))
    else:
    #Εκτέλεση αναζήτησης στη βάση δεδομένων MongoDB
        products = list(mongo.db.products.find(query))

    for p in products:
        p['_id'] = str(p['_id'])
    return jsonify(products)
#Δημιουργία endpoint για την προσθήκη ενός συγκεκριμένου προϊόντος στη βάση δεδομένων
@app.route('/products', methods=['POST'])
def create_products():
    data = request.json
    if isinstance(data, list):  # multiple products
        result = mongo.db.products.insert_many(data)
        ids = [str(id) for id in result.inserted_ids]
        return jsonify({'message': f'{len(ids)} products created', 'ids': ids}), 201
    else:  # single product
        result = mongo.db.products.insert_one(data) #προσθήκη ενός προϊόντος στη βάση δεδομένων
        return jsonify({'message': 'Product created', 'id': str(result.inserted_id)}), 201 #επιστροφή μηνύματος επιτυχίας με το ID του προϊόντος

#Δημιουργία endpoint για την προσθήκη ενός συγκεκριμένου προϊόντος 
@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    mongo.db.carts.insert_one(data)
    return jsonify({"message": "Item added to cart"}), 201

@app.route('/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400
    cart_items = list(mongo.db.carts.find({"user_id": user_id}))
    for item in cart_items:
        item['_id'] = str(item['_id'])
    return jsonify(cart_items)


@app.route('/cart/<user_id>', methods=['GET'])
def view_cart(user_id):
    cart_items = list(mongo.db.carts.find({"user_id": user_id}))
    enriched_items = []
    for item in cart_items:
        product = mongo.db.products.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            enriched_items.append({
                "_id": str(item["_id"]),
                "product_id": str(item["product_id"]),
                "quantity": item["quantity"],
                "product_name": product["name"],
                "price": product["price"]
            })
    return jsonify(enriched_items)


@app.route('/cart/ai/<user_id>', methods=['POST'])
def ai_suggestions(user_id):
    # Your logic calling Groq/OpenAI or whatever AI service you use
    # to analyze cart content and return suggestions
    # Example stub:
    cart_items = list(mongo.db.carts.find({"user_id": user_id}))
    if not cart_items:
        return jsonify({"ai_suggestions": "Το καλάθι είναι άδειο."}), 400
    
    # Simulate AI result (replace with actual call to Groq/OpenAI)
    suggestions = "Προτάσεις από AI βασισμένες στα προϊόντα σας."
    
    return jsonify({"ai_suggestions": suggestions}), 200


@app.route('/cart/<item_id>', methods=['PUT'])
def update_quantity(item_id):
    quantity = request.json.get('quantity')
    mongo.db.carts.update_one({"_id": ObjectId(item_id)}, {"$set": {"quantity": quantity}})
    return jsonify({"message": "Quantity updated"})

@app.route('/cart/<item_id>', methods=['DELETE'])
def delete_cart_item(item_id):
    mongo.db.carts.delete_one({"_id": ObjectId(item_id)})
    return jsonify({"message": "Item removed from cart"})

@app.route('/cart/checkout/<user_id>', methods=['POST'])
def checkout(user_id):
    cart_items = list(mongo.db.carts.find({"user_id": user_id}))
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    mongo.db.purchases.insert_one({
        "user_id": user_id,
        "items": [
            {
                "product_id": item["product_id"],
                "quantity": item["quantity"]
            }
            for item in cart_items
        ],
        "timestamp": datetime.now()
    })

    mongo.db.carts.delete_many({"user_id": user_id})
    return jsonify({"message": "Purchase complete"}), 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
