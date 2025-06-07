
import requests

API = "http://localhost:5000/products"

products = [
    
{
  "id": "680fc403a5eca3c64edaa26f",
  "name": "Ροδόπη Γάλα Κατσικίσιο Πλήρες 1lt",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 1.29,
  "description": "Γάλα με μεγάλη βιολογική αξία, για υγιεινή διατροφή! Πλούσιο σε ασβέστιο και φώσφορο, πολύτιμα για τα παιδιά! Το κατσικίσιο γάλα διαφέρει από το αγελαδινό, έχει ξεχωριστή γεύση, έχει λιγότερη λακτόζη για αυτό είναι ιδιαίτερα εύπεπτο.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/14_04_22/9c54cc42-15dd-4a47-819a-01c5e0743467_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa270",
  "name": "Όλυμπος Γιαούρτι Στραγγιστό 2% Λιπαρά 3x200gr",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 2.99,
  "description": "Ελαφρύ στραγγιστό γιαούρτι με 2% λιπαρά.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/05_10_23/9f5556d1-0422-4fd9-9c76-e015935a205c_EH.jpg"
},
{
  "id": "680fc403a5eca3c64edaa271",
  "name": "Δωδωνη Φετα Σε Αλμη 400gr",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 5.5,
  "description": "Η αυθεντική φέτα ΔΩΔΩΝΗ σε πρακτική πλαστική συσκευασία που διατηρεί το τυρί μέσα στη φυσική του άλμη, χαρίζοντας του φρεσκάδα και μεγαλύτερο χρόνο συντήρησης.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/21_07_21/796a0034-d880-4a3f-a5b2-4766e625b85f_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa272",
  "name": "Χρυσά Αυγά Φρέσκα 10άδα",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 2.7,
  "description": "ΧΡΥΣΑ ΑΥΓΑ Φρέσκα 10άδα 45γρ+ (διαφόρων μεγεθών)",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/11_07_23/7422d4d1-7eb5-4456-839f-bde60d24c8a4_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa273",
  "name": "Lurpak Βούτυρο Ανάλατο Αλουμινόφυλλο 250gr",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 4.2,
  "description": "Αγνό φρέσκο βούτυρο για ψήσιμο και άλειμμα.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/11_04_24/afc5cf49-7efb-4fd1-8f30-9d81c098a8a2_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa274",
  "name": "Μεβγάλ Κεφίρ Φράουλα 330ml",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 0.8,
  "description": "Ρόφημα κεφίρ με προβιοτικά.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/29_11_24/abf96edb-a426-4fe5-a99d-6035b0e04fc6_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa275",
  "name": "Μπάρμπα Στάθης Σαλάτα Τραγανή Λάχανο & Καρότο300gr",
  "category": "Φρούτα & Λαχανικά",
  "price": 1.5,
  "description": "Φρέσκη σαλάτα από λάχανο και καρότο, έτοιμη προς κατανάλωση.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/31_05_23/c18b736e-7b4b-407b-b0f4-bc4cd5dc91b6_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa276",
  "name": "Φρεσκούλης Σαλάτα Ιταλική Iceberg, Μαρούλι, Ραντίτσιο 200gr",
  "category": "Φρούτα & Λαχανικά",
  "price": 1.4,
  "description": "Φρέσκη σαλάτα με iceberg, μαρούλι και ραντίτσιο.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/07_04_21/c89e46f4-a0cc-45c5-9f55-c8737a67c767_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa277",
  "name": "Αγρόκηπος Παντζάρια Πέλλας Σακούλα 500gr",
  "category": "Φρούτα & Λαχανικά",
  "price": 1.8,
  "description": "Φρέσκα παντζάρια Πέλλας σε σακούλα 500gr.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/02_08_21/3dd9c66b-c2c2-4592-ae0c-32de7193e101_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa278",
  "name": "Μανιτάρια Πλευρώτους Ελληνικά 500gr",
  "category": "Φρούτα & Λαχανικά",
  "price": 2.2,
  "description": "Φρέσκα μανιτάρια πλευρώτους ελληνικής παραγωγής.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/18_04_24/0a432332-59aa-4b02-bae4-339bc45c6833_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa279",
  "name": "Μανιτάρια Φρέσκα Εισαγωγής 500gr",
  "category": "Φρούτα & Λαχανικά",
  "price": 1,
  "description": "Φρέσκα μανιτάρια εισαγωγής 500gr.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/15_07_21/5482bddf-3801-4040-98ac-eb27e43f23ce_EO.jpg"
},
{
  "id": "680fc403a5eca3c64edaa27a",
  "name": "Μπάρμπα Στάθης Σαλάτα Μαρουλένια 200gr",
  "category": "Φρούτα & Λαχανικά",
  "price": 1.6,
  "description": "Φρέσκια σαλάτα μαρουλένια με μαρούλι, ρόκα και σπανάκι.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/31_05_23/3c593401-d3e0-41c0-be0b-56f0e1cb6199_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa27b",
  "name": "Μπάρμπα Στάθης Σαλάτα Ιταλική 140gr",
  "category": "Φρούτα & Λαχανικά",
  "price": 1.5,
  "description": "Φρέσκια σαλάτα ιταλική με μαρούλι και πράσινη και κόκκινη ρόκα.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/31_05_23/06897f0a-17e1-40b8-bf08-563cd310258a_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa27c",
  "name": "Τοματίνια Που Αγαπάς Εγχώρια 250gr",
  "category": "Φρούτα & Λαχανικά",
  "price": 2.2,
  "description": "Φρέσκα τοματίνια ελληνικής παραγωγής, ιδανικά για σαλάτες.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/12_12_24/96b03f69-7e15-43d0-af6a-6ca4762b9bda_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa27d",
  "name": "Μπάρμπα Στάθης Πατάτες Country Κατεψυγμένες 750gr",
  "category": "Κατεψυγμένα Προϊόντα",
  "price": 2.8,
  "description": "Κατεψυγμένες πατάτες έτοιμες για τηγάνισμα.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/23_04_24/5468de45-1ab0-4e7e-af6b-61655cb3a1ea_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa27e",
  "name": "Χρυσή Ζύμη Πίτσα Χωριάτικη Κατεψυγμένη 420gr",
  "category": "Κατεψυγμένα Προϊόντα",
  "price": 3.7,
  "description": "Πίτσα τυρί φέτα Π.Ο.Π, καπνιστό τυρί Μετσόβου, ελιές, πιπεριά και ρίγανη έτοιμη στο φούρνο.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/11_05_23/e65edade-64fe-4c09-af23-83a7bd1b4a26_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa27f",
  "name": "Meatka Μπιφτέκι Κοτόπουλου Ελληνικό Νωπό 600gr",
  "category": "Κατεψυγμένα Προϊόντα",
  "price": 5.2,
  "description": "Κατεψυγμένα μπιφτέκια κοτόπουλου.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/21_06_21/4ce67ca1-8533-43cd-a87d-fcbfc2a53987_E1.jpg"
},
{
  "id": "680fc403a5eca3c64edaa280",
  "name": "Μπάρμπα Στάθης Φασολάκια Πλατιά Κατεψυγμένα 420gr",
  "category": "Κατεψυγμένα Προϊόντα",
  "price": 3.3,
  "description": "Κατεψυγμένα φασολάκια έτοιμα για μαγείρεμα.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/02_05_25/9e3266cf-fec1-45d2-8fab-68085cac9bde_EH.jpg"
},
{
  "id": "6810f4933d0187a89f45b2dd",
  "name": "Barilla Ζυμαρικά Spaghetti No5 500gr",
  "category": "Τρόφιμα Παντοπωλείου",
  "price": 1,
  "description": "Κλασικά ιταλικά ζυμαρικά σπαγγέτι.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/13_09_23/d088c6c6-3c97-4184-8348-f6de0ffcdc12_EH.jpg"
},
{
  "id": "6810f4933d0187a89f45b2de",
  "name": "3αλφα Ρύζι Καρολίνα 500gr",
  "category": "Τρόφιμα Παντοπωλείου",
  "price": 1.3,
  "description": "Ρύζι για γεμιστά και άλλα ελληνικά φαγητά.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/26_10_22/02caa853-f3e0-4f71-9707-4df857adcdb5_E1.jpg"
},
{
  "id": "6810f4933d0187a89f45b2df",
  "name": "3αλφα Φακές Ψιλές 500gr",
  "category": "Τρόφιμα Παντοπωλείου",
  "price": 1.5,
  "description": "Φακές ψιλές ελληνικής παραγωγής.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/14_03_22/b39b9b20-cf5a-46b6-8da5-56612ee82409_E1.jpg"
},
{
  "id": "6810f4933d0187a89f45b2e0",
  "name": "Rio Mare Τόνος Σε Νερό 160gr",
  "category": "Τρόφιμα Παντοπωλείου",
  "price": 1.9,
  "description": "Κονσέρβα τόνου υψηλής ποιότητας.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/24_11_23/aa850bbd-efd3-46c8-8a3e-aa307e6e57ca_E1.jpg"
},
{
  "id": "6810f4933d0187a89f45b2e1",
  "name": "Kyknos Τοματοπολτός 410gr",
  "category": "Τρόφιμα Παντοπωλείου",
  "price": 2.5,
  "description": "Πυκνός τοματοπολτός για σάλτσες και μαγειρική.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/02_04_24/d32b6511-cee3-4086-b8d9-1f811f2f2891_E1.jpg"
},
{
  "id": "6810f4933d0187a89f45b2e2",
  "name": "Κρις Κρις Φέτες Ζωής Ψωμί Τοστ Ολικής Άλεσης 500gr",
  "category": "Αρτοποιήματα",
  "price": 1.9,
  "description": "Ψωμί ολικής άλεσης με φυσικό προζύμι.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/10_11_23/e4310775-eb28-470f-a551-e07e0e334703_E1.jpg"
},
{
  "id": "6810f4933d0187a89f45b2e3",
  "name": "Οικογένεια Στεργίου Κρουασάν Βουτύρου 260gr",
  "category": "Αρτοποιήματα",
  "price": 2.5,
  "description": "Φρεσκοψημένο κρουασάν βουτύρου.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/18_04_23/b2b8ca0e-143f-4c62-bbfd-bae2925a4527_E1.jpg"
},
{
  "id": "6810f4933d0187a89f45b2e4",
  "name": "Καραμολέγκος Φόρμα Τοστ Σταρένιο 680gr",
  "category": "Αρτοποιήματα",
  "price": 1.2,
  "description": "Ψωμί τοστ σταρένιο με φυσικό προζύμι.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/11_07_23/c1726901-c35c-479e-8a5a-b1082600d2d6_E1.jpg"
},
{
  "id": "6810f4933d0187a89f45b2e5",
  "name": "Βοσινάκης Χωριάτικες Φρυγανιές Ολικής Άλεσης 240gr",
  "category": "Αρτοποιήματα",
  "price": 2.0,
  "description": "Φρυγανιές τραγανές με αλεύρι ολικής.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/15_11_23/9513e167-4162-44fc-b22c-f8c1ae215d6a_E1.jpg"
},
{
  "id": "6810f4933d0187a89f45b2e6",
  "name": "Παπαδοπούλου Μπισκότα Digestive 250gr",
  "category": "Αρτοποιήματα",
  "price": 2.1,
  "description": "Μπισκότα με αλεύρι ολικής και φυτικές ίνες.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/17_12_20/61ce8e11-1ea7-41b4-9e7e-5dbb9cf34e66_E1.jpg"
},
{
  "id": "6810f5a53d0187a89f45b2e8",
  "name": "Αντωνάκη Μπριζόλα Καπνιστή Μέλι 210gr",
  "category": "Κρέας & Ψάρι",
  "price": 3.5,
  "description": "Καπνιστή μπριζόλα με μέλι, ιδανική για σάντουιτς.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/10_02_21/4b2e4b67-0ec8-4f78-8697-8ed46b521e97_E1.jpg"
},
{
  "id": "6810f5a53d0187a89f45b2e9",
  "name": "Mimikos Στήθος Φιλέτο Κοτόπουλο Ελληνικό Νωπό 650gr",
  "category": "Κρέας & Ψάρι",
  "price": 10.5,
  "description": "Φιλέτο κοτόπουλου χωρίς πέτσα και κόκαλο.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/04_05_23/8ea8de7d-44a1-4d90-8f56-fd221bc90650_E1.jpg"
},
{
  "id": "6810f5a53d0187a89f45b2ea",
  "name": "Pescanova Φιλέτο Σολομός Ατλαντικού Κατεψυγμένος 250gr",
  "category": "Κρέας & Ψάρι",
  "price": 10.9,
  "description": "Φιλέτο σολομού ιδανικό για ψήσιμο.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/10_01_25/e6495393-730a-423a-9b5d-7ce93b26f94a_EH.jpg"
},
{
  "id": "6810f5a53d0187a89f45b2eb",
  "name": "Captain Iglo Φιλέτο Ψαριού Κατεψυγμένο 240gr",
  "category": "Κρέας & Ψάρι",
  "price": 5.8,
  "description": "Tο προϊόν προέρχεται από αλιεία που έχει πάρει ανεξάρτητη πιστοποίηση ότι πληροί το πρότυπο του MSC για καλή διαχείριση και αειφορία.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/21_06_24/e4ef27a1-9965-44cb-afdf-f3500351298f_E1.jpg"
},
{
  "id": "6810f5a53d0187a89f45b2ec",
  "name": "Coca Cola 8x330ml",
  "category": "Ποτά & Αναψυκτικά",
  "price": 5.85,
  "description": "Κλασικό αναψυκτικό Coca Cola σε συσκευασία 8x330ml.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/02_06_25/3b1a9468-0519-4b9c-913a-010a5e75e0dd_EH.jpg"
},
{
  "id": "6810f5a53d0187a89f45b2ed",
  "name": "Ζαγόρι Φυσικό Μεταλλικό Νερό 1,5lt 6τεμ",
  "category": "Ποτά & Αναψυκτικά",
  "price": 1.6,
  "description": "Φυσικό μεταλλικό νερό.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/12_05_25/42a35cc4-f496-48c1-a0b4-648896766d8d_E1.jpg"
},
{
  "id": "6810f5a53d0187a89f45b2ee",
  "name": "Όλυμπος Φυσικός Χυμός Πορτοκάλι 1lt",
  "category": "Ποτά & Αναψυκτικά",
  "price": 2.9,
  "description": "100% φυσικός χυμός πορτοκάλι.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/13_06_24/b3b22e81-75a5-4ff9-bb49-eafa92002a14_EH.jpg"
},
{
  "id": "6810f5a53d0187a89f45b2ef",
  "name": "Heineken Μπύρα Lager Κουτί 500ml",
  "category": "Ποτά & Αναψυκτικά",
  "price": 1.6,
  "description": "Ανοιχτόχρωμη ξανθιά Lager. Ιδανική για κάθε περίσταση.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/15_04_25/4cdacf0d-a6a1-46d8-9060-11c8d25f4997_EH.jpg"
},
{
  "id": "6810f5a53d0187a89f45b2f0",
  "name": "White Horse Ουίσκι 700ml",
  "category": "Ποτά & Αναψυκτικά",
  "price": 17.00,
  "description": "Ένα από τα πιο δημοφιλή blended ουίσκι στον κόσμο, με γεύση που συνδυάζει malt και grain.",
  "image_url": "https://cdn.mymarket.gr/images/styles/large/16_07_21/16ff216c-42af-4f83-9e04-569b9d0eba4a_E1.jpg"
}
]

for product in products:
    res = requests.post(API, json=product)
    print(f"{product['name']} -> {res.status_code}")


print("✅ Seeded products successfully!")
