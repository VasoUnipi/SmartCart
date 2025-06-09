import streamlit as st
import requests
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()
AI_BASE = os.getenv("AI_BASE", "http://ai:5001")
API_BASE = "http://backend:5000"

st.set_page_config(page_title="SmartCart", page_icon="🛒", layout="wide")


# ------------------ SESSION STATE ------------------
if 'user_id' not in st.session_state:
    st.session_state.user_id = ''
if 'category_filter' not in st.session_state:
    st.session_state.category_filter = ""
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'results' not in st.session_state:
    st.session_state.results = []
if 'checkout_complete' not in st.session_state:
    st.session_state.checkout_complete = False
if st.session_state.checkout_complete:
    # 🎈 Εφέ μπαλονιών
    st.balloons()

    # 🔙 Κουμπί πάνω αριστερά
    col_left, col_space, col_main = st.columns([1, 1, 8])
    with col_left:
        if st.button("Επιστροφή στην αρχική"):
            st.session_state.checkout_complete = False
            st.session_state.show_results = False
            st.session_state.user_id = ''
            st.experimental_rerun()

    # 🧭 Κεντραρισμένο περιεχόμενο
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align: center;'>
            <h2>Η αγορά ολοκληρώθηκε επιτυχώς!</h2>
            <img src='https://cdn-icons-png.flaticon.com/512/845/845646.png' width='120'>
            <p style='font-size: 20px;'>Ευχαριστούμε για την προτίμησή σας! 🛍️</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()


    if st.button("Επιστροφή στην αρχική σελίδα"):
        st.session_state.checkout_complete = False
        st.session_state.show_results = False
        st.experimental_rerun()
    st.stop()  # Σταματά το υπόλοιπο της σελίδας

image_path = os.path.join(os.path.dirname(__file__), "logos", "2.png")
img = Image.open(image_path) # width x height σε pixels
st.markdown("<br><br>", unsafe_allow_html=True)


#st.title("🛒 SmartCart")

# ------------------ BACKEND ΣΥΝΑΡΤΗΣΕΙΣ ------------------
def get_categories():
    try:
        r = requests.get(f"{API_BASE}/products")
        if r.status_code == 200:
            products = r.json()
            categories = sorted(list(set([p['category'] for p in products if 'category' in p])))
            return ["Όλες"] + categories
    except:
        return ["Όλες"]

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

def get_cart(user_id):
    try:
        r = requests.get(f"{API_BASE}/cart/{user_id}")
        if r.status_code != 200:
            return []
        items = r.json()

        # Φέρε όλα τα προϊόντα μία φορά
        r_products = requests.get(f"{API_BASE}/products")
        products = r_products.json() if r_products.status_code == 200 else []

        # Κάνε map id -> product
        product_map = {p["_id"]: p for p in products}

        # Εμπλούτισε το καλάθι με όνομα/εικόνα κλπ
        for item in items:
            prod = product_map.get(item["product_id"])
            if prod:
                item["name"] = prod.get("name")
                item["image_url"] = prod.get("image_url")
                item["price"] = prod.get("price", 1)  # Χρήσιμο για υπολογισμό συνόλου
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
st.sidebar.subheader("🧑 Είσοδος Χρήστη")
user_input = st.sidebar.text_input("Παρακαλώ εισάγετε όνομα χρήστη:", value=st.session_state.get('user_id', ''))
if user_input:
    st.session_state.user_id = user_input
# ------------------ ΥΠΟΧΡΕΩΤΙΚΟ USER ID ------------------
if not st.session_state.user_id:
    st.warning("⚠️ Παρακαλώ εισάγετε το User ID σας από το μενού στα αριστερά για να συνεχίσετε.")
    st.stop()
# ------------------ ΚΟΡΔΕΛΑ ------------------
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
    }
    .product-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        background-color: #f9f9f9;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
with col1:
    st.markdown("<h3 style='color:#2c3e50;'>🛒 SmartCart</h3>", unsafe_allow_html=True)
with col2:
    st.session_state.search_term = st.text_input("Αναζήτηση προϊόντος", value=st.session_state.search_term)
with col3:
    st.session_state.category_filter = st.selectbox("Κατηγορία", get_categories())
with col4:
    if st.button("🔍 Αναζήτηση"):
        results = search_products(
            name=st.session_state.search_term,
            category=st.session_state.category_filter
        )
        st.session_state.results = results
        st.session_state.show_results = True

# ------------------ ΑΡΧΙΚΗ ΣΕΛΙΔΑ ------------------
if not st.session_state.show_results:
    st.markdown("### Καλωσήρθατε στο **SmartCart** 🛍️")
    st.markdown("Αναζητήστε προϊόντα, προσθέστε τα στο καλάθι και αξιοποιήστε την τεχνητή νοημοσύνη για συμβουλές και συνταγές.")

# ------------------ ΑΠΟΤΕΛΕΣΜΑΤΑ ------------------
if st.session_state.show_results:
    products = st.session_state.results
    if products:
        st.markdown("### 📦 Αποτελέσματα")
        cols = st.columns(3)
        for i, product in enumerate(products):
            with cols[i % 3]:
                st.image(product['image_url'] if product.get('image_url') else "https://via.placeholder.com/200", width=200)
                st.markdown(f"**{product['name']}** | {product['category']} | {product['price']}€")
                st.markdown(product['description'])
                colx, coly = st.columns([3, 1])
                qty = colx.number_input("Ποσότητα", min_value=1, max_value=10, key=f"qty_{product['_id']}")
                if coly.button("🛒", key=f"add_{product['_id']}"):
                    added = add_to_cart(st.session_state.user_id, {"product_id": product['_id'], "quantity": qty})
                    if added:
                        st.success("Προστέθηκε στο καλάθι")
                    else:
                        st.error("Αποτυχία προσθήκης")
    else:
        st.info("Δεν βρέθηκαν προϊόντα.")

# ------------------ ΚΑΛΑΘΙ ------------------
#st.markdown("---")
#st.subheader("🧺 Το Καλάθι Μου")
#st.markdown(f"**User ID:** `{st.session_state.user_id}`")
#cart_items = get_cart(st.session_state.user_id)
#total = 0

#for item in cart_items:
 #   st.markdown(f"**{item['product_id']}** - Ποσότητα: {item['quantity']}")
  #  col1, col2, col3 = st.columns(3)
   # new_qty = col1.number_input("Αλλαγή ποσότητας", min_value=1, max_value=10, value=item['quantity'], key=f"uq_{item['_id']}")
    #if col2.button("Ενημέρωση", key=f"uqbtn_{item['_id']}"):
     #   if update_quantity(item['_id'], new_qty):
      #      st.success("Ενημερώθηκε")
       # else:
        #    st.error("Σφάλμα ενημέρωσης")
    #if col3.button("❌ Αφαίρεση", key=f"rm_{item['_id']}"):
     #   if delete_cart_item(item['_id']):
      #      st.success("Διαγράφηκε")
       # else:
        #    st.error("Αποτυχία διαγραφής")
    #total += item['quantity'] * 1

#st.info(f"Σύνολο προϊόντων: {total}")
#if st.button("✅ Ολοκλήρωση Αγοράς"):
 #   if checkout(st.session_state.user_id):
  #      st.success("Η αγορά ολοκληρώθηκε!")
   #     st.session_state.results = []
    #    st.session_state.show_results = False
    #else:
     #   st.error("Το καλάθι είναι άδειο ή απέτυχε η πληρωμή.")
# ------------------ SIDEBAR ΚΑΛΑΘΙ ------------------
if st.session_state.user_id:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧺 Το Καλάθι Μου")
    cart_items = get_cart(st.session_state.user_id)
    total = 0

    for item in cart_items:
        st.sidebar.markdown("----")
        product_name = item.get('name', item.get('product_id', 'Άγνωστο'))
        image_url = item.get('image_url', "https://via.placeholder.com/100")
        st.sidebar.image(image_url, width=100)
        st.sidebar.markdown(f"**{product_name}**")
        st.sidebar.markdown(f"Ποσότητα: {item['quantity']}")
        total += item['quantity'] * 1  # Αν θες πραγματική τιμή, φέρε και price

    st.sidebar.markdown(f"**Σύνολο προϊόντων:** `{total}`")

    if st.sidebar.button("✅ Ολοκλήρωση Αγοράς"):
        if checkout(st.session_state.user_id):
            st.session_state.checkout_complete = True
            st.experimental_rerun()
        else:
            st.sidebar.error("Το καλάθι είναι άδειο ή απέτυχε η πληρωμή.")
# ------------------ ΟΘΟΝΗ ΟΛΟΚΛΗΡΩΣΗΣ ------------------
if st.session_state.get("checkout_complete"):
    st.markdown("## Η αγορά ολοκληρώθηκε επιτυχώς!")
    st.markdown("Μπορείτε να επιστρέψετε στην αρχική σελίδα.")
    if st.button("Επιστροφή"):
        st.session_state.checkout_complete = False
        st.experimental_rerun()
        st.session_state.useri_id = ''
    st.stop()
# ------------------ AI ΒΟΗΘΟΣ ------------------
with st.sidebar.expander("🤖 AI Βοηθός", expanded=False):
    ai_option = st.selectbox("Λειτουργία", [
        "Πρόταση συνταγής",
        "Αξιολόγηση διατροφής",
        "Υγιεινές εναλλακτικές",
        "Εβδομαδιαίο πλάνο",
        "Λίστα για στόχο",
        "Περιβαλλοντική ανάλυση",
        "Συνδυαστικά προϊόντα"], key="ai_option")

    ai_input = st.text_input("Προϊόντα (με κόμμα)", key="ai_input")
    extra_input = ""
    if ai_option == "Λίστα για στόχο":
        extra_input = st.text_input("Στόχος (π.χ. vegan, διαβήτης)", key="ai_goal")

    if st.button("▶ AI Εκτέλεση"):
        endpoint_map = {
            "Πρόταση συνταγής": "/ai/recipe",
            "Αξιολόγηση διατροφής": "/ai/evaluate",
            "Υγιεινές εναλλακτικές": "/ai/alternatives",
            "Εβδομαδιαίο πλάνο": "/ai/mealplan",
            "Λίστα για στόχο": "/ai/goal",
            "Περιβαλλοντική ανάλυση": "/ai/eco",
            "Συνδυαστικά προϊόντα": "/ai/combos"
        }
        route = endpoint_map.get(ai_option)
        data = {"products": [x.strip() for x in ai_input.split(",")]} if ai_option != "Λίστα για στόχο" else {"goal": extra_input}
        r = requests.post(f"{AI_BASE}{route}", json=data)

        r = requests.post(f"{AI_BASE}{route}", json=data)
        if r.status_code == 200:
            st.success(r.json()["response"])
        else:
            st.error("Αποτυχία απόκρισης από AI.")

# ------------------ SCRAPING ------------------
with st.expander("🌐 Τιμή από άλλες πηγές (scraping)", expanded=False):
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
                        st.subheader(f"🔍 Αποτέλεσμα για «{result['name']}»")
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if result["image_url"]:
                                st.image(result["image_url"], width=100)
                            else:
                                st.text("Χωρίς εικόνα")
                        with col2:
                            st.markdown(f"**{result['name']}**")
                            st.markdown(f"💶 Τιμή: `{result['price']}`")
                            st.markdown(f"[🔗 Προβολή στο κατάστημα]({result['product_url']})")
                    else:
                        st.info("Δεν βρέθηκε προϊόν.")
                else:
                    st.warning("⚠️ Σφάλμα κατά το scraping.")
            except Exception as e:
                st.error(f"❌ Σφάλμα: {e}")
        else:
            st.warning("Παρακαλώ εισάγετε ένα προϊόν.")
