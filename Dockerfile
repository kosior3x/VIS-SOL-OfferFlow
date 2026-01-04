# Startujemy z lekkiego Pythona
FROM python:3.9-slim

# Katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy plik z listą bibliotek
COPY requirements.txt .

# Instalujemy Flask
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy całą zawartość Vis-Sol do kontenera
COPY . .

# Port, na którym działa program
EXPOSE 5000

# Start Alexa i Twojego programu
CMD ["python", "app.py"]
