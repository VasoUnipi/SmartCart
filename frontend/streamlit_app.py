import streamlit as st
import requests
from PIL import Image
import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)
API_BASE = "http://backend:5000"

st.set_page_config(page_title="SmartCart", page_icon="🛒", layout="wide")

# ------------------ SESSION STATE ------------------
for key, default in {
    'user_id': '',
    'category_filter': "",
    'search_term': "",
    'show_results': False,
    'results': [],
    'checkout_complete': False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if st.session_state.checkout_complete:
    st.balloons()
    if st.button("Επιστροφή στην αρχική"):
        st.session_state.checkout_complete = False
        st.session_state.show_results = False
        st.session_state.user_id = ''
        st.experimental_rerun()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center;'>
            <h2>Η αγορά ολοκληρώθηκε επιτυχώς!</h2>
            <p style='font-size: 20px;'>Ευχαριστούμε για την προτίμησή σας!</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()


# ------------------ BACKEND CALLS ------------------
def get_categories():
    try:
        r = requests.get(f"{API_BASE}/products")
        if r.status_code == 200:
            products = r.json()
            categories = sorted(set([p['category'] for p in products if 'category' in p]))
            return ["Όλες"] + categories
    except:
        return ["Όλες"]

def search_products(name=None, category=None, price=None, order_by=None):
    params = {}
    if name:
        params['name'] = name
    if category and category != "Όλες":
        params['category'] = category
    if price:
        params['price'] = price
    if order_by:
        params['order_by'] = order_by
    try:
        r = requests.get(f"{API_BASE}/products", params=params)
        return r.json() if r.status_code == 200 else []
    except:
        return []

def get_cart(user_id):
    try:
        r = requests.get(f"{API_BASE}/cart/{user_id}")
        if r.status_code != 200:
            return []
        items = r.json()
        products = requests.get(f"{API_BASE}/products").json()
        product_map = {p["_id"]: p for p in products}
        for item in items:
            prod = product_map.get(item["product_id"])
            if prod:
                item.update({
                    "name": prod.get("name"),
                    "image_url": prod.get("image_url"),
                    "price": prod.get("price", 1)
                })
        return items
    except:
        return []

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

# ------------------ USER ID ------------------
st.sidebar.subheader("Είσοδος Χρήστη")
user_input = st.sidebar.text_input("Παρακαλώ εισάγετε όνομα χρήστη:", value=st.session_state.get('user_id', ''))
if user_input:
    st.session_state.user_id = user_input
if not st.session_state.user_id:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('image.png');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.warning("Παρακαλώ εισάγετε το Όνομα Χρήστη σας για να συνεχίσετε.")
    st.stop()
    
# ------------------ SEARCH BAR ------------------
col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 2, 2, 2, 1])
with col1:
    image_path_top = os.path.join(os.path.dirname(__file__), "SmartCart.png")
    img_top = Image.open(image_path_top)
    st.image(img_top, width=100)
with col2:
    st.session_state.search_term = st.text_input("Αναζήτηση προϊόντος", value=st.session_state.search_term)
with col3:
    st.session_state.category_filter = st.selectbox("Κατηγορία", get_categories())
with col4:
    max_price = st.number_input("Μέγιστη τιμή (€)", min_value=0.0, value=0.0, step=0.5)
with col5:
    order_by = st.selectbox("Ταξινόμηση κατά", ["-", "Τιμή ↑", "Τιμή ↓", "Όνομα A-Ω", "Όνομα Ω-A"])
with col6:
    if st.button("🔍 Αναζήτηση"):
        order_param = None
        if order_by == "Τιμή αύξουσα":
            order_param = "price_asc"
        elif order_by == "Τιμή φθίνουσα":
            order_param = "price_desc"
        elif order_by == "Όνομα A-Ω":
            order_param = "name_asc"
        elif order_by == "Όνομα Ω-A":
            order_param = "name_desc"

        results = search_products(
            name=st.session_state.search_term,
            category=st.session_state.category_filter,
            price=max_price if max_price > 0 else None,
            order_by=order_param
        )
        st.session_state.results = results
        st.session_state.show_results = True
# ------------------ RESULTS ------------------
if not st.session_state.show_results:
    st.markdown("### Καλωσήρθατε στο **SmartCart** ")
    st.markdown("Αναζητήστε προϊόντα, προσθέστε τα στο καλάθι και λάβετε AI προτάσεις και συνταγές.")

if st.session_state.show_results:
    products = st.session_state.results
    if products:
        st.markdown("### Αποτελέσματα Αναζήτησης")
        cols = st.columns(3)
        for i, product in enumerate(products):
            with cols[i % 3]:
                st.image(product.get('image_url', "https://via.placeholder.com/200"), width=200)
                st.markdown(f"**{product['name']}** | {product['category']} | {product['price']}€")
                st.markdown(product['description'])
                colx, coly = st.columns([3, 1])
                qty = colx.number_input("Ποσότητα", min_value=1, max_value=10, key=f"qty_{product['_id']}")
                if coly.button("🛒", key=f"add_{product['_id']}"):
                    added = add_to_cart(st.session_state.user_id, {"product_id": product['_id'], "quantity": qty})
                    st.success("Προστέθηκε στο καλάθι" if added else "Αποτυχία προσθήκης")
    else:
        st.info("Δεν βρέθηκαν προϊόντα.")

# ------------------ CART SIDEBAR ------------------
st.sidebar.markdown("---")
st.sidebar.subheader(" Το Καλάθι Μου")
cart_items = get_cart(st.session_state.user_id)
total_products, total_price = 0, 0.0

for item in cart_items:
    st.sidebar.markdown("----")
    name = item.get('name', item['product_id'])
    image_url = item.get('image_url', "https://via.placeholder.com/100")
    quantity = item['quantity']
    price = item.get('price', 1.0)
    item_total = quantity * price

    st.sidebar.image(image_url, width=100)
    st.sidebar.markdown(f"**{name}**")
    new_qty = st.sidebar.number_input("Ποσότητα", min_value=1, max_value=100, value=quantity, key=f"cart_qty_{item['_id']}")
    if new_qty != quantity:
        if update_quantity(item["_id"], new_qty):
            st.experimental_rerun()
    if st.sidebar.button("Αφαίρεση", key=f"remove_{item['_id']}"):
        if delete_cart_item(item["_id"]):
            st.experimental_rerun()

    st.sidebar.markdown(f"Τιμή: `{price:.2f}€`")
    st.sidebar.markdown(f"Υποσύνολο: `{item_total:.2f}€`")

    total_products += quantity
    total_price += item_total

# ------------------ AI SUGGESTIONS ------------------
if cart_items:
    with st.sidebar:
        st.markdown("### Επιλέξτε τι θέλετε να ρωτήσετε τον SmartieBot:")

        ai_choice = st.radio(
            "Θέμα ερώτησης",
            [
                "Ανάλυση διατροφικής αξίας",
                "Κατάλληλα για vegans ή vegetarians",
                "Παρόμοια / συμπληρωματικά προϊόντα",
                "Ιδέες για συνταγές"
            ],
            index=0
        )

        if st.button("Ρώτησε τον SmartieBot!"):
            st.info("Ο SmartieBot επεξεργάζεται το καλάθι σας...")

            # Prepare cart summary
            products_str = "\n".join([
                f"- {item['name']} ({item['quantity']}x): {item.get('description', '')}"
                for item in cart_items
            ])

            # Build prompt based on choice
            prompt_map = {
                "Ανάλυση διατροφικής αξίας": "Ανάλυση της διατροφικής αξίας των παρακάτω προϊόντων.",
                "Κατάλληλα για vegans ή vegetarians": "Ποια από τα παρακάτω προϊόντα είναι κατάλληλα για vegans ή vegetarians;",
                "Παρόμοια / συμπληρωματικά προϊόντα": "Πρότεινε παρόμοια ή συμπληρωματικά προϊόντα για όσα έχω στο καλάθι.",
                "Ιδέες για συνταγές": "Πρότεινε ιδέες για συνταγές που μπορώ να φτιάξω με τα παρακάτω προϊόντα."
            }

            prompt = f"""
Έχω τα εξής προϊόντα στο καλάθι μου:

{products_str}

{prompt_map[ai_choice]}

Απάντησε στα ελληνικά, με σαφήνεια και χωριστές ενότητες αν χρειάζεται.
"""

            try:
                chat_completion = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[
                        {"role": "system", "content": "Είσαι διατροφολόγος"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                response = chat_completion.choices[0].message.content
                st.markdown("### Απάντηση από τον SmartieBot:")
                st.markdown(response)

            except Exception as e:
                st.error(f"Σφάλμα απόκρισης από AI: {e}")           

# ------------------ CHECKOUT ------------------
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Σύνολο προϊόντων:** `{total_products}`")
st.sidebar.markdown(f"**Συνολικό κόστος:** `{total_price:.2f}€`")
if st.sidebar.button("Ολοκλήρωση Αγοράς"):
    if checkout(st.session_state.user_id):
        st.session_state.checkout_complete = True
        st.experimental_rerun()
    else:
        st.sidebar.error("Το καλάθι είναι άδειο ή απέτυχε η πληρωμή.")

# ------------------ SCRAPING ------------------
with st.expander("Τιμή από άλλες πηγές (scraping)", expanded=False):
    scrap_term = st.text_input("Προϊόν για τιμή από τρίτο site", key="scraping")

    if st.button("🔎 Έλεγχος τιμής από άλλο κατάστημα"):
        if scrap_term.strip():
            try:
                # Κλήση στο backend endpoint σου
                r = requests.get(f"{API_BASE}/api/mymarket-scrape", params={"product_name": scrap_term})
                if r.status_code == 200:
                    result = r.json()

                    # Έλεγχος αν επιστράφηκε τιμή
                    if "name" in result:
                        st.subheader(f"Αποτέλεσμα για «{result['name']}»")
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if result["image_url"]:
                                st.image(result["image_url"], width=100)
                            else:
                                st.text("Χωρίς εικόνα")
                        with col2:
                            st.markdown(f"**{result['name']}**")
                            st.markdown(f"Τιμή: `{result['price']}`")
                            st.markdown(f"[Προβολή στο κατάστημα]({result['product_url']})")
                    else:
                        st.info("Δεν βρέθηκε προϊόν.")
                else:
                    st.warning("Σφάλμα κατά το scraping.")
            except Exception as e:
                st.error(f"Σφάλμα: {e}")
        else:
            st.warning("Παρακαλώ εισάγετε ένα προϊόν.")
