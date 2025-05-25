from pymongo import MongoClient
from collections import Counter
import matplotlib.pyplot as plt
from bson import ObjectId

# Σύνδεση με MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["smartcart_db"]
carts = db["carts"]
products = db["products"]

# 1. Συγκέντρωση όλων των προϊόντων που αγοράστηκαν
def get_top_products():
    purchases = carts.find({"checked_out": True})
    product_counter = Counter()

    for purchase in purchases:
        for item in purchase.get("items", []):
            product_counter[str(item["product_id"])] += item["quantity"]

    # Εμφάνιση Top 5 προϊόντων
    top_5 = product_counter.most_common(5)
    labels = []
    values = []

    for product_id, qty in top_5:
        product = products.find_one({"_id": ObjectId(product_id)})
        labels.append(product["name"])
        values.append(qty)

    plt.bar(labels, values)
    plt.title("Top 5 Δημοφιλέστερα Προϊόντα")
    plt.ylabel("Ποσότητες")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

# 2. Ανάλυση αγορών ανά ημέρα
def get_purchases_per_day():
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

    plt.plot(days, counts, marker='o')
    plt.title("Αριθμός Αγορών Ανά Ημέρα")
    plt.xlabel("Ημερομηνία")
    plt.ylabel("Αγορές")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Εκτέλεση
if __name__ == "__main__":
    get_top_products()
    get_purchases_per_day()
