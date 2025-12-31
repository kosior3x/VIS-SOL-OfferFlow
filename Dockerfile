# Wybieramy lekki obraz Pythona
FROM python:3.9-slim

# Ustawiamy katalog roboczy wewnątrz kontenera
WORKDIR /app

# Kopiujemy listę bibliotek i instalujemy je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę plików (app.py)
COPY . .

# Informujemy, na jakim porcie działa nasza aplikacja
EXPOSE 5000

# Komenda uruchamiająca silnik
CMD ["python", "app.py"]
