# products_seed.py
import requests

API = "http://localhost:5000/products"

products = [
{
  "id": "680fc403a5eca3c64edaa26f",
  "name": "Γάλα Πλήρες 1lt",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 1.29,
  "description": "Φρέσκο πλήρες γάλα 1 λίτρου από ελληνικές φάρμες.",
  "image_url": "https://images.unsplash.com/photo-1576186726188-c9d70843790f?q=80&w=1965&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa270",
  "name": "Γιαούρτι Στραγγιστό 2% 200g",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 0.99,
  "description": "Ελαφρύ στραγγιστό γιαούρτι με 2% λιπαρά.",
  "image_url": "https://plus.unsplash.com/premium_photo-1713719213311-044ae870a7ec?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa271",
  "name": "Τυρί Φέτα 400g",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 5.5,
  "description": "Παραδοσιακή ελληνική φέτα Π.Ο.Π.",
  "image_url": "https://cdn.pixabay.com/photo/2015/02/10/02/42/cheese-630511_960_720.jpg"
},
{
  "id": "680fc403a5eca3c64edaa272",
  "name": "Αυγά Large 6 τεμ",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 2.7,
  "description": "Αυγά μεγάλου μεγέθους από ελευθέρας βοσκής.",
  "image_url": "https://images.unsplash.com/photo-1498654077810-12c21d4d6dc3?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa273",
  "name": "Βούτυρο Αγνό 250g",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 3.2,
  "description": "Αγνό φρέσκο βούτυρο για ψήσιμο και άλειμμα.",
  "image_url": "https://plus.unsplash.com/premium_photo-1699651798312-dd6d2734b4fb?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa274",
  "name": "Κεφίρ 330ml",
  "category": "Γαλακτοκομικά & Αυγά",
  "price": 1.8,
  "description": "Ρόφημα κεφίρ με προβιοτικά.",
  "image_url": "https://images.unsplash.com/photo-1525070389266-b9afb0eed846?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa275",
  "name": "Μήλα Starking",
  "category": "Φρούτα & Λαχανικά",
  "price": 2.5,
  "description": "Γλυκά και τραγανά μήλα Starking.",
  "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa276",
  "name": "Μπανάνες",
  "category": "Φρούτα & Λαχανικά",
  "price": 1.4,
  "description": "Φρέσκες μπανάνες υψηλής ποιότητας.",
  "image_url": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa277",
  "name": "Ντομάτες",
  "category": "Φρούτα & Λαχανικά",
  "price": 1.8,
  "description": "Φρέσκες ντομάτες ελληνικής παραγωγής.",
  "image_url": "https://images.unsplash.com/photo-1582284540020-8acbe03f4924?q=80&w=1935&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa278",
  "name": "Πατάτες",
  "category": "Φρούτα & Λαχανικά",
  "price": 1.2,
  "description": "Πατάτες κατάλληλες για βράσιμο ή τηγάνισμα.",
  "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa279",
  "name": "Καρότα",
  "category": "Φρούτα & Λαχανικά",
  "price": 1,
  "description": "Φρέσκα καρότα για σαλάτες και φαγητά.",
  "image_url": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa27a",
  "name": "Πορτοκάλια",
  "category": "Φρούτα & Λαχανικά",
  "price": 1.6,
  "description": "Ζουμερά πορτοκάλια για χυμό ή φαγητό.",
  "image_url": "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?q=80&w=1935&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa27b",
  "name": "Αγγούρια",
  "category": "Φρούτα & Λαχανικά",
  "price": 1.5,
  "description": "Δροσερά αγγούρια για σαλάτες.",
  "image_url": "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa27c",
  "name": "Φράουλες",
  "category": "Φρούτα & Λαχανικά",
  "price": 3,
  "description": "Γλυκές φρέσκες φράουλες.",
  "image_url": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa27d",
  "name": "Κατεψυγμένες Πατάτες 1kg",
  "category": "Κατεψυγμένα Προϊόντα",
  "price": 2.8,
  "description": "Κατεψυγμένες πατάτες έτοιμες για τηγάνισμα.",
  "image_url": "https://images.unsplash.com/photo-1723763246578-99e614b2a91b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzB8fGZyaWVkJTIwcG90YXRvc3xlbnwwfHwwfHx8MA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa27e",
  "name": "Πίτσα Κατεψυγμένη 350g",
  "category": "Κατεψυγμένα Προϊόντα",
  "price": 3.7,
  "description": "Πίτσα με τυριά και αλλαντικά έτοιμη στο φούρνο.",
  "image_url": "https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?q=80&w=1776&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa27f",
  "name": "Μπιφτέκια Κατεψυγμένα 500g",
  "category": "Κατεψυγμένα Προϊόντα",
  "price": 5.2,
  "description": "Κατεψυγμένα μπιφτέκια μοσχαρίσια.",
  "image_url": "https://images.unsplash.com/photo-1659345737306-7022e0687e0d?q=80&w=1931&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "680fc403a5eca3c64edaa280",
  "name": "Κατεψυγμένα Φασολάκια",
  "category": "Κατεψυγμένα Προϊόντα",
  "price": 2.5,
  "description": "Κατεψυγμένα φασολάκια έτοιμα για μαγείρεμα.",
  "image_url": "https://images.unsplash.com/photo-1567375698348-5d9d5ae99de0?q=80&w=1935&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
},
{
  "id": "6810f4933d0187a89f45b2dd",
  "name": "Ζυμαρικά Σπαγγέτι 500g",
  "category": "Τρόφιμα Παντοπωλείου",
  "price": 1,
  "description": "Κλασικά ιταλικά ζυμαρικά σπαγγέτι.",
  "image_url": "https://plus.unsplash.com/premium_photo-1675627339038-703eef80e11f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHNwYWdoZXR0aXxlbnwwfHwwfHx8MA%3D%3D"
},
{
  "id": "6810f4933d0187a89f45b2de",
  "name": "Ρύζι Καρολίνα 500g",
  "category": "Τρόφιμα Παντοπωλείου",
  "price": 1.3,
  "description": "Ρύζι για γεμιστά και άλλα ελληνικά φαγητά.",
  "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cmljZXxlbnwwfHwwfHx8MA%3D%3D"
},
{
  "id": "6810f4933d0187a89f45b2df",
  "name": "Όσπρια Φακές Ψιλές 500g",
  "category": "Τρόφιμα Παντοπωλείου",
  "price": 1.5,
  "description": "Φακές ψιλές ελληνικής παραγωγής.",
  "image_url": "https://images.unsplash.com/photo-1638378545909-d78bd9b4271c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGxlbnRpbHN8ZW58MHx8MHx8fDA%3D"
},
{
  "id": "6810f4933d0187a89f45b2e0",
  "name": "Κονσέρβα Τόνου σε Νερό 160g",
  "category": "Τρόφιμα Παντοπωλείου",
  "price": 1.9,
  "description": "Κονσέρβα τόνου υψηλής ποιότητας.",
  "image_url": "https://plus.unsplash.com/premium_photo-1695304030270-ec988d7b267e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8dHVuYSUyMGNhbnxlbnwwfHwwfHx8MA%3D%3D"
},
{
  "id": "6810f4933d0187a89f45b2e1",
  "name": "Τοματοπολτός 500g",
  "category": "Τρόφιμα Παντοπωλείου",
  "price": 1.1,
  "description": "Πυκνός τοματοπολτός για σάλτσες και μαγειρική.",
  "image_url": "https://images.unsplash.com/photo-1472476443507-c7a5948772fc?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dG9tYXRvJTIwcGFzdGV8ZW58MHx8MHx8fDA%3D"
},
{
  "id": "6810f4933d0187a89f45b2e2",
  "name": "Ψωμί Ολικής Άλεσης 500g",
  "category": "Αρτοποιήματα",
  "price": 1.9,
  "description": "Ψωμί ολικής άλεσης με φυσικό προζύμι.",
  "image_url": "https://images.unsplash.com/photo-1635439954773-ed98b09dccb2?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8d2hvbGVtZWFsJTIwYnJlYWR8ZW58MHx8MHx8fDA%3D"
},
{
  "id": "6810f4933d0187a89f45b2e3",
  "name": "Κρουασάν Βουτύρου 60g",
  "category": "Αρτοποιήματα",
  "price": 0.8,
  "description": "Φρεσκοψημένο κρουασάν βουτύρου.",
  "image_url": "https://plus.unsplash.com/premium_photo-1661743823829-326b78143b30?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y3JvaXNzYW50fGVufDB8fDB8fHww"
},
{
  "id": "6810f4933d0187a89f45b2e4",
  "name": "Μπαγκέτα Σταρένια",
  "category": "Αρτοποιήματα",
  "price": 1.2,
  "description": "Τραγανή μπαγκέτα σταρένια.",
  "image_url": "https://images.unsplash.com/photo-1691862469586-9c7c183b27b7?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8d2hlYXQlMjBiYWd1ZXR0ZXN8ZW58MHx8MHx8fDA%3D"
},
{
  "id": "6810f4933d0187a89f45b2e5",
  "name": "Φρυγανιές Ολικής Άλεσης",
  "category": "Αρτοποιήματα",
  "price": 1.7,
  "description": "Φρυγανιές τραγανές με αλεύρι ολικής.",
  "image_url": "https://plus.unsplash.com/premium_photo-1725469970279-dec43c20ee61?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8d2hvbGVtZWFsJTIwdG9hc3R8ZW58MHx8MHx8fDA%3D"
},
{
  "id": "6810f4933d0187a89f45b2e6",
  "name": "Μπισκότα Digestive 250g",
  "category": "Αρτοποιήματα",
  "price": 2.1,
  "description": "Μπισκότα με αλεύρι ολικής και φυτικές ίνες.",
  "image_url": "https://plus.unsplash.com/premium_photo-1667899298617-afedd0d2f3d9?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZGlnZXN0aXZlJTIwY29va2llc3xlbnwwfHwwfHx8MA%3D%3D"
},
{
  "id": "6810f5a53d0187a89f45b2e8",
  "name": "Μπριζόλα Μοσχαρίσια",
  "category": "Κρέας & Ψάρι",
  "price": 9.9,
  "description": "Φρέσκια μπριζόλα από ελληνικό μοσχάρι.",
  "image_url": "https://images.unsplash.com/photo-1628543108325-1c27cd7246b3?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8YmVlZiUyMHN0ZWFrfGVufDB8fDB8fHww"
},
{
  "id": "6810f5a53d0187a89f45b2e9",
  "name": "Φιλέτο Κοτόπουλο 1kg",
  "category": "Κρέας & Ψάρι",
  "price": 6.5,
  "description": "Φιλέτο κοτόπουλου χωρίς πέτσα και κόκαλο.",
  "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Y2hpY2tlbiUyMGZpbGxldHxlbnwwfHwwfHx8MA%3D%3D"
},
{
  "id": "6810f5a53d0187a89f45b2ea",
  "name": "Σολομός Φιλέτο 250g",
  "category": "Κρέας & Ψάρι",
  "price": 5.9,
  "description": "Φιλέτο σολομού ιδανικό για ψήσιμο.",
  "image_url": "https://images.unsplash.com/photo-1499125562588-29fb8a56b5d5?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c2FsbW9uJTIwZmlsbGV0fGVufDB8fDB8fHww"
},
{
  "id": "6810f5a53d0187a89f45b2eb",
  "name": "Γαρίδες Κατεψυγμένες 500g",
  "category": "Κρέας & Ψάρι",
  "price": 7.8,
  "description": "Κατεψυγμένες γαρίδες καθαρισμένες.",
  "image_url": "https://plus.unsplash.com/premium_photo-1707927340705-ad673cf26177?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZnJvemVuJTIwc2hyaW1wfGVufDB8fDB8fHww"
},
{
  "id": "6810f5a53d0187a89f45b2ec",
  "name": "Αναψυκτικό Κόλα 330ml",
  "category": "Ποτά & Αναψυκτικά",
  "price": 0.85,
  "description": "Αναψυκτικό τύπου κόλα με ανθρακικό.",
  "image_url": "https://plus.unsplash.com/premium_photo-1676979223508-1509a7dc4571?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y29jYSUyMGNvbGElMjBiZXZlcmFnZXxlbnwwfHwwfHx8MA%3D%3D"
},
{
  "id": "6810f5a53d0187a89f45b2ed",
  "name": "Νερό Μεταλλικό 1.5lt",
  "category": "Ποτά & Αναψυκτικά",
  "price": 0.4,
  "description": "Φυσικό μεταλλικό νερό.",
  "image_url": "https://images.unsplash.com/photo-1595994195534-d5219f02f99f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bWluZXJhbCUyMHdhdGVyfGVufDB8fDB8fHww"
},
{
  "id": "6810f5a53d0187a89f45b2ee",
  "name": "Χυμός Πορτοκάλι 1lt",
  "category": "Ποτά & Αναψυκτικά",
  "price": 1.9,
  "description": "100% φυσικός χυμός πορτοκάλι.",
  "image_url": "https://images.unsplash.com/photo-1577680716097-9a565ddc2007?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8b3JhbmdlJTIwanVpY2V8ZW58MHx8MHx8fDA%3D"
},
{
  "id": "6810f5a53d0187a89f45b2ef",
  "name": "Μπύρα Lager 500ml",
  "category": "Ποτά & Αναψυκτικά",
  "price": 1.2,
  "description": "Δροσιστική μπύρα lager ελληνικής παραγωγής.",
  "image_url": "https://images.unsplash.com/photo-1644085159285-5fd924740cb3?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8bGFnZXIlMjBiZWVyfGVufDB8fDB8fHww"
},
{
  "id": "6810f5a53d0187a89f45b2f0",
  "name": "Κρασί Λευκό 750ml",
  "category": "Ποτά & Αναψυκτικά",
  "price": 4.5,
  "description": "Ξηρό λευκό κρασί από ελληνικούς αμπελώνες.",
  "image_url": "https://plus.unsplash.com/premium_photo-1676590905367-12ff693f0afe?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8d2hpdGUlMjB3aW5lfGVufDB8fDB8fHww"
}]


for product in products:
    res = requests.post(API, json=product)
    print(f"{product['name']} -> {res.status_code}")


print("✅ Seeded products successfully!")
