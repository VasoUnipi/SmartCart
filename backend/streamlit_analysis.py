import streamlit as st
from pymongo import MongoClient
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from bson import ObjectId

# Σύνδεση με MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["smartcart"]
purchases = db["purchases"]
products = db["products"]

# Συνάρτηση για την ανάκτηση ονόματος προϊόντος από το ID
def get_product_name(pid):
    try:
        obj_id = ObjectId(pid)
        product = products.find_one({"_id": obj_id})
    except:
        product = products.find_one({"id": pid})
    return product["name"] if product else "Άγνωστο προϊόν"

# Top 5 δημοφιλέστερα προϊόντα
def plot_top_products():
    counter = Counter()
    for purchase in purchases.find():
        for item in purchase.get("items", []):
            counter[str(item["product_id"])] += item.get("quantity", 1)
    top = counter.most_common(5)
    names = [get_product_name(pid) for pid, _ in top]
    quantities = [q for _, q in top]
    # Εμφάνιση γραφήματος και πίνακα
    st.subheader("Top 5 Δημοφιλέστερα Προϊόντα")
    st.bar_chart(pd.DataFrame({"Προϊόν": names, "Ποσότητα": quantities}).set_index("Προϊόν"))
    st.dataframe(pd.DataFrame({"Προϊόν": names, "Ποσότητα": quantities}))

# Αγορές ανά ημέρα
def plot_purchases_per_day():
    pipeline = [
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    data = list(purchases.aggregate(pipeline))
    df = pd.DataFrame(data)
    if df.empty:
        st.info("Δεν υπάρχουν καταγεγραμμένες ημερομηνίες.")
        return
    df.columns = ["Ημερομηνία", "Αγορές"]
    st.subheader("Αριθμός Αγορών Ανά Ημέρα")
    st.line_chart(df.set_index("Ημερομηνία"))
    st.dataframe(df)

# Αυτόματο καλάθι
# Συνάρτηση για αυτόματη δημιουργία καλαθιού με τα 5 πιο δημοφιλή προϊόντα
def auto_cart():
    counter = Counter()
    for purchase in purchases.find():
        seen = set()
        for item in purchase.get("items", []):
            pid = str(item["product_id"])
            if pid not in seen:
                counter[pid] += 1
                seen.add(pid)
    top = counter.most_common(5)
    names = [get_product_name(pid) for pid, _ in top]
    df = pd.DataFrame({"Προϊόν": names, "Προτεινόμενη Ποσότητα": [1] * len(names)})

    st.subheader("Αυτόματη Δημιουργία Καλαθιού")
    st.table(df)

# Streamlit UI
# Ρύθμιση της σελίδας
st.title("SmartCart | Υποσύστημα Ανάλυσης Δεδομένων")
# Ρυθμίσεις εμφάνισης
plot_top_products()
st.markdown("---")
plot_purchases_per_day()
st.markdown("---")
auto_cart()
