FROM python:3.11-slim

WORKDIR /app

COPY streamlit_analysis.py ./
RUN pip install --no-cache-dir streamlit pymongo matplotlib pandas

CMD ["streamlit", "run", "streamlit_analysis.py", "--server.port=8502", "--server.address=0.0.0.0"]
