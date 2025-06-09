import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
from flask import Blueprint, request, jsonify

scraping_bp = Blueprint('scraping', __name__)

@scraping_bp.route('/api/mymarket-scrape', methods=['GET'])
def mymarket_scrape():
    product_name = request.args.get('product_name')
    if not product_name:
        return jsonify({"error": "Missing product_name parameter"}), 400

    result = scrape_mymarket_product(product_name)  # η συνάρτηση scraping σου
    return jsonify(result)


def slugify(text):
        # Πρώτα κάνουμε μερικές αντικαταστάσεις για να ταιριάζει το site
    replacements = {
        'Στεργίου': 'stergiou',
        'Κρουασάν' : 'krouasan',
        'Βουτύρου' : 'voutyrou',
        'Παπαδοπούλου': 'papadopoulou',
        'Μπύρα': 'mpyra',
        'Κουτί': 'kouti',
        '1,5lt': '15lt',
        'Ουίσκι': 'ouiski',
        'Αλουμινόφυλλο': 'alouminofyllo',
        'Φράουλα': 'fraoula',
        'Iceberg': 'iceberg',
        'Πλευρώτους': 'plevrotous',
        'Μαρουλένια': 'maroulenia',
        'Που': 'pou',
        'Κοτόπουλου': 'kotopoulou',
        'Κοτόπουλο': 'kotopoulo',
        'Ρύζι': 'ryzi',
        'η': 'i',
        'ή': 'ι',
        'Ή': 'Ι',
        'ς': 'σ', 
        'φ': 'f',
        'Φ': 'f',
        'υ': 'y',
        'χ': 'ch',
        'Χ': 'ch',
        'Αυγά': 'avga',
        'αυγά': 'avga',
        'b': 'v',
        'Β': 'v',
        'β': 'v' 
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    # Μετατροπή σε λατινικούς χαρακτήρες, πεζά, παύλες αντί για κενά, χωρίς ειδικούς χαρακτήρες
    text = unidecode(text)
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text

def scrape_mymarket_product(product_name):
    slug = slugify(product_name)
    product_url = f"https://www.mymarket.gr/{slug}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    res = requests.get(product_url, headers=headers)
    if res.status_code != 200:
        return {"error": "Product page not found", "url": product_url}

    soup = BeautifulSoup(res.text, "html.parser")

    # Όνομα προϊόντος - από meta property og:title ή h1
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        name = og_title["content"].split("|")[0].strip()
    else:
        h1 = soup.find("h1", class_="text-2xl")
        name = h1.text.strip() if h1 else product_name

    # Τιμή προϊόντος - ψάχνουμε το span με την κλάση που βγάζει την τελική τιμή
    price_span = soup.find("span", class_="product-full--final-price")
    price = price_span.text.strip() if price_span else "N/A"

    # URL εικόνας - από tag <link rel="preload" href="...">
    link_img = soup.find("link", rel="preload", attrs={"as": "image"})
    image_url = link_img["href"] if link_img else None

    return {
        "name": name,
        "price": price,
        "image_url": image_url,
        "product_url": product_url
    }
    # Για γρήγορο test
if __name__ == "__main__":
    product_name = "Οικογένεια Στεργίου Κρουασάν Βουτύρου 260gr"
    result = scrape_mymarket_product(product_name)
    print(result) 
