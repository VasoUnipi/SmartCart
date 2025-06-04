FROM python:3.11-slim

WORKDIR /app

COPY ai.py ./

RUN pip install --no-cache-dir flask requests python-dotenv

EXPOSE 5001

ENV PYTHONUNBUFFERED=1

CMD ["python", "ai.py"]
