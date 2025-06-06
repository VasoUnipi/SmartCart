from flask import Flask, send_file
from pymongo import MongoClient
from collections import Counter
import matplotlib.pyplot as plt
from bson import ObjectId
import io

app = Flask(__name__)

client = MongoClient("mongodb://host.docker.internal:27017/")  # ή αλλάζεις αν έχεις docker-compose
db = client["smartcart_db"]
carts = db["carts"]
products = db["products"]

@app.route("/api/analysis/top-products")
def top_products():
    purchases = carts.find({"checked_out": True})
    product_counter = Counter()

    for purchase in purchases:
        for item in purchase.get("items", []):
            product_counter[str(item["product_id"])] += item["quantity"]

    top_5 = product_counter.most_common(5)
    labels = []
    values = []

    for product_id, qty in top_5:
        product = products.find_one({"_id": ObjectId(product_id)})
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

@app.route("/api/analysis/purchases-per-day")
def purchases_per_day():
    pipeline = [
        {"$match": {"checked_out": True}},
        {"$group": {
            "_id": { "$dateToString": { "format": "%Y-%m-%d", "date": "$timestamp" }},
            "count": { "$sum": 1 }
        }},
        {"$sort": {"_id": 1}}
    ]
    result = list(carts.aggregate(pipeline))
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
