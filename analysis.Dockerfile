FROM python:3.11-slim

WORKDIR /app

COPY analysis.py purchases.json ./

RUN pip install --no-cache-dir flask pandas

EXPOSE 5002

CMD ["python", "analysis.py"]
