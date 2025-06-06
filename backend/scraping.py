from flask import Blueprint, jsonify
import requests
from urllib.parse import quote_plus, quote

scraping_bp = Blueprint('scraping', __name__)

def greek_to_greeklish(text):
    mapping = {
        'α': 'a', 'ά': 'a',
        'β': 'v',
        'γ': 'g',
        'δ': 'd',
        'ε': 'e', 'έ': 'e',
        'ζ': 'z',
        'η': 'i', 'ή': 'i',
        'θ': 'th',
        'ι': 'i', 'ί': 'i', 'ϊ': 'i', 'ΐ': 'i',
        'κ': 'k',
        'λ': 'l',
        'μ': 'm',
        'ν': 'n',
        'ξ': 'x',
        'ο': 'o', 'ό': 'o',
        'π': 'p',
        'ρ': 'r',
        'σ': 's', 'ς': 's',
        'τ': 't',
        'υ': 'y', 'ύ': 'y', 'ϋ': 'y', 'ΰ': 'y',
        'φ': 'f',
        'χ': 'x',
        'ψ': 'ps',
        'ω': 'o', 'ώ': 'o',
    }
    return ''.join(mapping.get(c.lower(), c) for c in text)

# ✅ Δηλώνουμε σωστά το route
@scraping_bp.route("/scraping/search/<term>", methods=["GET"])
def scrape_ab(term):
    try:
        # Μετατροπή σε greeklish για χρήση στο URL
        greeklish_term = greek_to_greeklish(term)
        query = quote(greeklish_term)

        url = "https://www.ab.gr/api/v1/"
        params = {
            "operationName": "GetProductSearch",
            "variables": f'{{"lang":"gr","searchQuery":"{query}","pageNumber":0,"pageSize":20,"filterFlag":true,"fields":"PRODUCT_TILE","plainChildCategories":true,"useSpellingSuggestion":true}}',
            "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"d1422cd4a4d0404f06cc547ad892b50102e8849a9fbc064e030faf3c31a3ae3c"}}'
        }

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        products = data.get("data", {}).get("productSearch", {}).get("products", [])
        results = []

        for product in products[:10]:
            title = product.get("name", "")
            url_path = product.get("url", "")
            link = f"https://www.ab.gr{url_path}"

            # Απόκτηση τιμής
            price_info = product.get("price", {})
            price = price_info.get("price") or price_info.get("value") or "N/A"

            # Απόκτηση εικόνας
            image_url = ""
            images = product.get("images", [])
            for img in images:
                if img.get("format") == "respListGrid" and img.get("imageType") == "PRIMARY":
                    image_url = "https://www.ab.gr" + img.get("url", "")
                    break
            if not image_url and images:
                image_url = "https://www.ab.gr" + images[0].get("url", "")

            results.append({
                "title": title,
                "price": f"{price}€" if price != "N/A" else "Μη διαθέσιμη",
                "link": link,
                "image": image_url
            })

        if not results:
            return jsonify({"message": "Δεν βρέθηκαν προϊόντα."})

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
