from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from scraping import scraping_bp

app = Flask(__name__)
app.register_blueprint(scraping_bp)

app.config['MONGO_URI'] = 'mongodb://mongo:27017/smartcart'
mongo = PyMongo(app)

#------HOMEPAGE------
# Route: Home page
@app.route('/')
def home():
    return "🚀 Το SmartCart app τρέχει σωστά!"

@app.route('/products', methods=['GET'])
def get_products():
    name = request.args.get('name')
    category = request.args.get('category')
    max_price = request.args.get('price')

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

    products = list(mongo.db.products.find(query))
    for p in products:
        p['_id'] = str(p['_id'])
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_products():
    data = request.json
    if isinstance(data, list):  # multiple products
        result = mongo.db.products.insert_many(data)
        ids = [str(id) for id in result.inserted_ids]
        return jsonify({'message': f'{len(ids)} products created', 'ids': ids}), 201
    else:  # single product
        result = mongo.db.products.insert_one(data)
        return jsonify({'message': 'Product created', 'id': str(result.inserted_id)}), 201


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
        "items": cart_items,
        "timestamp": datetime.now()
    })

    mongo.db.carts.delete_many({"user_id": user_id})
    return jsonify({"message": "Purchase complete"}), 200

@app.route('/purchases/<user_id>', methods=['GET'])
def get_purchases(user_id):
    history = list(mongo.db.purchases.find({"user_id": user_id}))
    for h in history:
        h['_id'] = str(h['_id'])
        h['timestamp'] = h['timestamp'].isoformat()
        for item in h['items']:
            item['_id'] = str(item['_id'])
            item['product_id'] = str(item['product_id']) if 'product_id' in item else ''
    return jsonify(history), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
