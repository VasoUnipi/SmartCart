from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/smartcart_db"
mongo = PyMongo(app)

#------HOMEPAGE------
# Route: Home page
@app.route('/')
def home():
    return "🚀 Το SmartCart app τρέχει σωστά!"

# ---------- ΑΡΧΙΚΟΠΟΙΗΣΗ ΠΡΟΪΟΝΤΩΝ ----------
@app.route('/init/products', methods=['POST'])
#def init_products():
    #products = [
        #{"name": "Γάλα", "category": "Τρόφιμα", "description": "Γάλα 1lt", "image_url": "", "price": 1.5},
        #{"name": "Ψωμί", "category": "Τρόφιμα", "description": "Ψωμί ολικής", "image_url": "", "price": 0.9},
        #{"name": "Οδοντόκρεμα", "category": "Υγιεινή", "description": "Οδοντόκρεμα 75ml", "image_url": "", "price": 2.3},
        #{"name": "Αφρόλουτρο", "category": "Υγιεινή", "description": "500ml", "image_url": "", "price": 3.8}
    #]
    #mongo.db.products.delete_many({})
    #mongo.db.products.insert_many(products)   
    #return jsonify({"message": "Τα προϊόντα αρχικοποιήθηκαν"}), 201

# ---------- ΛΙΣΤΑ / ΑΝΑΖΗΤΗΣΗ ΠΡΟΪΟΝΤΩΝ ----------
@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    name = request.args.get('name')
    query = {}
    if category:
        query['category'] = category
    if name:
        query['name'] = {'$regex': name, '$options': 'i'}
    products = list(mongo.db.products.find(query))
    for p in products:
        p['_id'] = str(p['_id'])
    return jsonify(products), 200

# ---------- ΔΗΜΙΟΥΡΓΙΑ ΚΑΛΑΘΙΟΥ ----------
@app.route('/cart', methods=['POST'])
def create_cart():
    cart = {"items": [], "checked_out": False, "timestamp": None}
    cart_id = mongo.db.carts.insert_one(cart).inserted_id
    return jsonify({"cart_id": str(cart_id)}), 201

# ---------- ΠΡΟΣΘΗΚΗ ΠΡΟΪΟΝΤΟΣ ΣΤΟ ΚΑΛΑΘΙ ----------
@app.route('/cart/<cart_id>/add', methods=['POST'])
def add_to_cart(cart_id):
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    if not ObjectId.is_valid(cart_id) or not ObjectId.is_valid(product_id):
        return jsonify({"error": "Μη έγκυρα IDs"}), 400

    cart = mongo.db.carts.find_one({"_id": ObjectId(cart_id)})
    if not cart or cart.get("checked_out"):
        return jsonify({"error": "Το καλάθι δεν υπάρχει ή έχει ήδη ολοκληρωθεί"}), 400

    # Προσθήκη προϊόντος
    mongo.db.carts.update_one(
        {"_id": ObjectId(cart_id)},
        {"$push": {"items": {"product_id": ObjectId(product_id), "quantity": quantity}}}
    )
    return jsonify({"message": "✅ Το προϊόν προστέθηκε στο καλάθι!"}), 200

# ---------- ΟΛΟΚΛΗΡΩΣΗ ΑΓΟΡΑΣ ----------
@app.route('/cart/<cart_id>/checkout', methods=['POST'])
def checkout(cart_id):
    if not ObjectId.is_valid(cart_id):
        return jsonify({"error": "Μη έγκυρο ID"}), 400

    cart = mongo.db.carts.find_one({"_id": ObjectId(cart_id)})
    if not cart or cart.get("checked_out"):
        return jsonify({"error": "Το καλάθι δεν υπάρχει ή έχει ήδη ολοκληρωθεί"}), 400

    mongo.db.carts.update_one(
        {"_id": ObjectId(cart_id)},
        {"$set": {"checked_out": True, "timestamp": datetime.now()}}
    )
    return jsonify({"message": "🛒 Η αγορά ολοκληρώθηκε!"}), 200

# ---------- ΙΣΤΟΡΙΚΟ ΑΓΟΡΩΝ ----------
@app.route('/purchases', methods=['GET'])
def purchase_history():
    carts = list(mongo.db.carts.find({"checked_out": True}))
    for c in carts:
        c['_id'] = str(c['_id'])
        for item in c['items']:
            item['product_id'] = str(item['product_id'])
        c['timestamp'] = c['timestamp'].isoformat() if c['timestamp'] else None
    return jsonify(carts), 200

# ---------- ΕΝΑΡΞΗ SERVER ----------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
