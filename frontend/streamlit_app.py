import streamlit as st
import requests

API_BASE = "http://backend:5000"

st.set_page_config(page_title="SmartCart", page_icon="🛒")
# ----------- ΕΝΑΡΞΗ ΤΟΥ SESSION STATE -------------
if 'user_id' not in st.session_state:
    st.session_state.user_id = ''
st.title("🛒 SmartCart")

# ----------- ΣΥΝΑΡΤΗΣΕΙΣ BACKEND -------------
def search_products(name=None, category=None, price=None):
    params = {}
    if name:
        params['name'] = name
    if category and category != "Όλες":
        params['category'] = category
    if price:
        params['price'] = price
    try:
        r = requests.get(f"{API_BASE}/products", params=params)
        return r.json() if r.status_code == 200 else []
    except:
        return []

def get_categories():
    try:
        r = requests.get(f"{API_BASE}/products")
        if r.status_code == 200:
            products = r.json()
            categories = sorted(list(set([p['category'] for p in products if 'category' in p])))
            return ["Όλες"] + categories
    except:
        return ["Όλες"]

def get_cart(user_id):
    r = requests.get(f"{API_BASE}/cart/{user_id}")
    return r.json() if r.status_code == 200 else []

def add_to_cart(user_id, product):
    product['user_id'] = user_id
    r = requests.post(f"{API_BASE}/cart", json=product)
    return r.status_code == 201

def delete_cart_item(item_id):
    r = requests.delete(f"{API_BASE}/cart/{item_id}")
    return r.status_code == 200

def update_quantity(item_id, qty):
    r = requests.put(f"{API_BASE}/cart/{item_id}", json={"quantity": qty})
    return r.status_code == 200

def checkout(user_id):
    r = requests.post(f"{API_BASE}/cart/checkout/{user_id}")
    return r.status_code == 200

# ----------- USER ID INPUT -------------
st.sidebar.subheader("🧑 Είσοδος Χρήστη")
user_input = st.sidebar.text_input("Δώσε το User ID σου:", value=st.session_state.get('user_id', ''))

if user_input:
    st.session_state.user_id = user_input

# ----------- ΦΟΡΜΑ ΑΝΑΖΗΤΗΣΗΣ -------------
# ----------- ΦΟΡΜΑ ΑΝΑΖΗΤΗΣΗΣ -------------
st.subheader("🔍 Αναζήτηση Προϊόντων")
name = st.text_input("Όνομα προϊόντος")
category_list = get_categories()
category = st.selectbox("Κατηγορία", category_list)
price = st.number_input("Μέγιστη τιμή", min_value=0.0, value=0.0, step=0.5)
sort_option = st.selectbox("Ταξινόμηση κατά", ["Χωρίς ταξινόμηση", "Τιμή (Αύξουσα)", "Τιμή (Φθίνουσα)", "Όνομα (Α-Ω)", "Όνομα (Ω-Α)"])

if st.button("Αναζήτηση"):
    results = search_products(name, category, price if price > 0 else None)
    if sort_option == "Τιμή (Αύξουσα)":
        results.sort(key=lambda x: x.get('price', 0))
    elif sort_option == "Τιμή (Φθίνουσα)":
        results.sort(key=lambda x: x.get('price', 0), reverse=True)
    elif sort_option == "Όνομα (Α-Ω)":
        results.sort(key=lambda x: x.get('name', '').lower())
    elif sort_option == "Όνομα (Ω-Α)":
        results.sort(key=lambda x: x.get('name', '').lower(), reverse=True)
    st.session_state['results'] = results

# ----------- ΑΠΟΤΕΛΕΣΜΑΤΑ ΑΝΑΖΗΤΗΣΗΣ -------------
if 'results' in st.session_state:
    st.subheader("📦 Αποτελέσματα")
    for product in st.session_state.results:
        st.markdown(f"**{product['name']}** | {product['category']} | {product['price']}€")
        st.image(product['image_url'] if product.get('image_url') else "https://via.placeholder.com/200", width=200)
        st.markdown(product['description'])
        col1, col2 = st.columns([3, 1])
        qty = col1.number_input("Ποσότητα", min_value=1, max_value=10, key=f"qty_{product['_id']}")
        if col2.button("Προσθήκη", key=f"add_{product['_id']}"):
            added = add_to_cart(st.session_state.user_id, {"product_id": product['_id'], "quantity": qty})
            if added:
                st.success("Προστέθηκε στο καλάθι")
            else:
                st.error("Αποτυχία προσθήκης")

# ----------- ΚΑΛΑΘΙ -------------
st.subheader("🧺 Το Καλάθι Μου")
st.markdown(f"**User ID:** `{st.session_state.user_id}`")
cart_items = get_cart(st.session_state.user_id)

total = 0
for item in cart_items:
    st.markdown(f"**{item['product_id']}** - Ποσότητα: {item['quantity']}")
    col1, col2, col3 = st.columns(3)
    new_qty = col1.number_input("Αλλαγή ποσότητας", min_value=1, max_value=10, value=item['quantity'], key=f"uq_{item['_id']}")
    if col2.button("Ενημέρωση", key=f"uqbtn_{item['_id']}"):
        if update_quantity(item['_id'], new_qty):
            st.success("Ενημερώθηκε")
        else:
            st.error("Σφάλμα ενημέρωσης")
    if col3.button("❌ Αφαίρεση", key=f"rm_{item['_id']}"):
        if delete_cart_item(item['_id']):
            st.success("Διαγράφηκε")
        else:
            st.error("Αποτυχία διαγραφής")
    total += item['quantity'] * 1

st.info(f"Σύνολο προϊόντων: {total}")
if st.button("✅ Ολοκλήρωση Αγοράς"):
    if checkout(st.session_state.user_id):
        st.success("Η αγορά ολοκληρώθηκε!")
        st.session_state.results = []
    else:
        st.error("Το καλάθι είναι άδειο ή απέτυχε η πληρωμή.")
