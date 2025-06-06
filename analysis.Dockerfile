FROM python:3.11-slim

WORKDIR /app

COPY analysis.py .

RUN pip install --no-cache-dir flask pymongo matplotlib

EXPOSE 5002

CMD ["python", "analysis.py"]
