FROM python:3.11-slim

WORKDIR /app

COPY ai.py ./

RUN pip install --no-cache-dir flask requests

EXPOSE 5001

CMD ["python", "ai.py"]
