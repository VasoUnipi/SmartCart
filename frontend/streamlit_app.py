import streamlit as st
import requests

API_URL = "http://localhost:5000"  # Change if backend is on another host/port

st.title("🛒 SmartCart Web App")

# Search Products
st.header("🔍 Search Products")
name = st.text_input("Name")
category = st.text_input("Category")
price = st.number_input("Max Price", min_value=0.0, step=1.0)

if st.button("Search"):
    params = {}
    if name:
        params['name'] = name
    if category:
        params['category'] = category
    if price:
        params['price'] = price
    res = requests.get(f"{API_URL}/products", params=params)
    products = res.json()
    st.write(products)

# Add product to cart
st.header("🛒 Add to Cart")
user_id = st.text_input("User ID", value="user1")
product_id = st.text_input("Product ID")
quantity = st.number_input("Quantity", min_value=1, step=1)

if st.button("Add to Cart"):
    payload = {
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity
    }
    res = requests.post(f"{API_URL}/cart", json=payload)
    st.success(res.json().get("message"))

# View Cart
st.header("🧾 View Cart")
if st.button("View Cart"):
    res = requests.get(f"{API_URL}/cart/{user_id}")
    st.write(res.json())

# Checkout
st.header("✅ Checkout")
if st.button("Checkout"):
    res = requests.post(f"{API_URL}/cart/checkout/{user_id}")
    st.success(res.json().get("message"))

