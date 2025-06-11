# Βασική εικόνα
FROM python:3.11-slim

# Εργασιακός φάκελος
WORKDIR /app

# Αντιγραφή αρχείων
COPY . /app

# Εγκατάσταση dependencies
RUN pip install --no-cache-dir streamlit pymongo pandas matplotlib

# Εκκίνηση της Streamlit εφαρμογής
CMD ["streamlit", "run", "streamlit_analysis.py", "--server.address=0.0.0.0"]
