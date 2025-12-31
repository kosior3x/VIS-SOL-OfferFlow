FROM python:3.9-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie plików konfiguracji
COPY requirements.txt .

# Instalacja z wymuszeniem braku cache (żeby uniknąć błędów)
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie reszty kodu
COPY . .

# Wystawienie portu
EXPOSE 5000

# Start aplikacji
CMD ["python", "app.py"]
