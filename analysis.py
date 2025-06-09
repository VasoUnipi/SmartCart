
from flask import Flask, send_file, request, jsonify
from pymongo import MongoClient
from collections import Counter
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Σύνδεση με MongoDB
client = MongoClient("mongodb://host.docker.internal:27017/")
db = client["smartcart_db"]
purchases_col = db["purchases"]
products_col = db["products"]

# Top 5 δημοφιλέστερα προϊόντα
@app.route("/api/analysis/top-products")
def top_products():
    purchases = purchases_col.find()
    product_counter = Counter()

    for purchase in purchases:
        for item in purchase.get("items", []):
            product_counter[str(item["product_id"])] += item.get("quantity", 1)

    top_5 = product_counter.most_common(5)
    labels = []
    values = []

    for product_id, qty in top_5:
        product = products_col.find_one({"id": product_id})
        if product:
            labels.append(product["name"])
            values.append(qty)

    plt.figure()
    plt.bar(labels, values)
    plt.title("Top 5 Δημοφιλέστερα Προϊόντα")
    plt.ylabel("Ποσότητες")
    plt.xticks(rotation=30)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

# Αριθμός αγορών ανά ημέρα
@app.route("/api/analysis/purchases-per-day")
def purchases_per_day():
    pipeline = [
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    result = list(purchases_col.aggregate(pipeline))
    days = [r['_id'] for r in result]
    counts = [r['count'] for r in result]

    plt.figure()
    plt.plot(days, counts, marker='o')
    plt.title("Αριθμός Αγορών Ανά Ημέρα")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Αγορές")
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

# Συνήθως αγοράζονται μαζί
@app.route("/api/analysis/frequently-bought-together")
def frequently_bought_together():
    target_id = request.args.get("product_id")
    if not target_id:
        return jsonify({"error": "Missing product_id"}), 400

    co_occurrence = Counter()
    purchases = purchases_col.find()

    for purchase in purchases:
        items = [str(item["product_id"]) for item in purchase.get("items", [])]
        if target_id in items:
            for pid in items:
                if pid != target_id:
                    co_occurrence[pid] += 1

    top_related = co_occurrence.most_common(3)
    related_products = []
    for pid, count in top_related:
        prod = products_col.find_one({"id": pid})
        if prod:
            related_products.append({
                "product_id": pid,
                "name": prod["name"],
                "times_bought_together": count
            })

    return jsonify(related_products)

# Αυτόματη δημιουργία καλαθιού βάσει επαναλαμβανόμενων αγορών
@app.route("/api/analysis/auto-cart")
def auto_cart():
    product_counter = Counter()
    purchases = purchases_col.find()

    for purchase in purchases:
        seen = set()
        for item in purchase.get("items", []):
            pid = str(item["product_id"])
            if pid not in seen:
                product_counter[pid] += 1
                seen.add(pid)

    recommended = product_counter.most_common(5)
    cart_suggestion = []
    for pid, freq in recommended:
        prod = products_col.find_one({"id": pid})
        if prod:
            cart_suggestion.append({
                "product_id": pid,
                "name": prod["name"],
                "recommended_quantity": 1
            })

    return jsonify(cart_suggestion)

# Εκκίνηση του Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
