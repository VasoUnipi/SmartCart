# 🛒 SmartCart – Έξυπνο Καλάθι Αγορών για το UnipiShop

## Περιγραφή
Το SmartCart είναι ένα Πληροφοριακό Σύστημα γραμμένο σε Python με Flask, το οποίο επιτρέπει στον χρήστη να δημιουργήσει και να διαχειριστεί καλάθια αγορών, να αναζητήσει προϊόντα από βάση δεδομένων, να λάβει στατιστικά αγορών, να κάνει scraping από άλλα e-shops και να πάρει συνταγές ή διατροφικές αξιολογήσεις με χρήση AI.

Αναπτύχθηκε στο πλαίσιο του ΠΜΣ "Πληροφοριακά Συστήματα και Υπηρεσίες" – Μάθημα: Η Γλώσσα Προγραμματισμού Python.

## Τεχνολογίες
- Python 3.10+
- Flask (REST API)
- MongoDB (NoSQL Database)
- Streamlit (UI)
- matplotlib /pandas (Ανάλυση Δεδομένων)
- BeautifulSoup (Web Scraping)
- Groq API με LLaMA 3 (AI)
- Docker / Docker Compose

## Οδηγίες Εγκατάστασης

1. Κλωνοποίηση του αποθετηρίου
  
   git clone https://github.com/yourusername/smartcart.git
   cd smartcart

### Μέσω Docker (Προτεινόμενο)

1. **Βεβαιωθείτε ότι έχετε εγκατεστημένο το Docker και Docker Compose**
2. **Απλώς εκτελέστε:**

   docker-compose up --build

   ή πατήστε **"Run all services"** στο περιβάλλον σας αν υποστηρίζει GUI.
3. **Όλα τα services (Flask API, MongoDB, Streamlit) θα ξεκινήσουν αυτόματα.**

>**Σημαντικό:** Πριν την εκτέλεση, φροντίστε να έχετε δημιουργήσει το αρχείο `.env` στη ρίζα του project και να έχετε τοποθετήσει το API Key για το Groq AI στο παρακάτω format:

GROQ_API_KEY=your_api_key_here

## Δομή Έργου

SMARTCART/
├── backend/
│   ├── app.py
│   ├── products_seed.py
│   ├── scraping.py
│   ├── requirements.txt
│   ├── Dockerfile
├── frontend/
│   ├── streamlit_app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── logos/
│   │   ├── SmartCart.png
│   │   └── 2.png
├── ai.py
├── ai.Dockerfile
├── docker-compose.yml
├── streamlit_analysis.py
├── streamlit_analysis.Dockerfile
├── .env              # API key για Groq (δεν περιλαμβάνεται)
├── README.md


## REST API Endpoints

### Προϊόντα
- `GET /products` – Λίστα προϊόντων
- `POST/products/<id>` – Πρόσθεση προϊόντως

### Καλάθι
- `POST /cart` – Δημιουργία νέου καλαθιού
- `GET/cart/<user_id>` – Προβολή καλαθιού ενός χρήστη
- `PUT /cart/<item_id>` – Προσθήκη προϊόντος
- `DELETE /cart/<item_id>` – Αφαίρεση προϊόντος
- `POST /cart/checkout/{user_id}` – Ολοκλήρωση αγοράς

### Web Scraping
- `GET/api/mymarket-scrape?product_name=<name>` – Εναλλακτικές τιμές/περιγραφές από e-shops

### AI Προτάσεις
- `POST /ai/recipe` – Συνταγή βάσει περιεχομένου καλαθιού
[.......]

## 🧪 Δοκιμές με Postman

Μπορείτε να βρείτε όλες τις κλήσεις του API στο αρχείο `SmartCart.postman_collection.json`, έτοιμες για import στο Postman.

Οδηγίες: https://learning.postman.com/docs/getting-started/importing-and-exporting/

## 📌 Σημειώσεις
- Τα API keys για την Groq API πρέπει να αποθηκευτούν στο αρχείο `.env`

