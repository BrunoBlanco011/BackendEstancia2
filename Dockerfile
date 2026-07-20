FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Recursos de NLTK horneados en la imagen (evita descargas en cada arranque)
RUN python -m nltk.downloader -d /usr/local/nltk_data punkt stopwords
ENV NLTK_DATA=/usr/local/nltk_data

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
