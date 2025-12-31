import os
from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import requests
import json

app = Flask(__name__)

# Klucze i konfiguracja
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
MODEL_VERSION = "meta/llama-2-70b-chat" # Potężny mózg do optymalizacji map

def optimize_mapping_logic(raw_data):
    """Mechanizm rozwoju: AI analizuje dane i optymalizuje mapę."""
    if not REPLICATE_API_TOKEN:
        return f"Błąd: Brak tokena. Dane surowe: {raw_data}"
    
    prompt = f"""
    Jesteś Alex, analityk Vis-Sol. Zoptymalizuj poniższą mapę procesów. 
    Wskaż błędy w logice i zaproponuj lepsze zestrojenie, aby efekt był maksymalny.
    Dane do analizy: {raw_data}
    """
    
    headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}", "Content-Type": "application/json"}
    url = "https://api.replicate.com/v1/predictions"
    
    payload = {
        "version": "02e386b35a93012921509a250325d97a54497e594833240e872c0c7a339908d1",
        "input": {"prompt": prompt}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        prediction = response.json()
        # Tutaj następuje 'nauka' - w realnym systemie można by tu dodać zapis do bazy danych
        return " ".join(prediction.get("output", ["Analiza w toku..."]))
    except:
        return f"Optymalizacja lokalna (offline): {raw_data[:200]}..."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    client = request.form.get('client_name', 'Klient Vis-Sol')
    raw_map = request.form.get('map_data', '')

    # 1. URUCHOMIENIE MECHANIZMU ROZWOJU (AI)
    optimized_result = optimize_mapping_logic(raw_map)

    # 2. GENEROWANIE PROFESJONALNEJ OFERTY PDF
    pdf_path = "oferta_vis_sol.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Nagłówek Vis-Sol
    c.setFont("Helvetica-Bold", 20)
    c.setStrokeColorRGB(0.1, 0.4, 0.8)
    c.drawString(50, height - 50, "VIS-SOL | Raport Optymalizacji")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, "WWW: vis-sol.prv.pl | System: OfferFlow v2.0")
    c.line(50, height - 75, width - 50, height - 75)

    # Treść: Klient
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 110, f"Podmiot: {client}")

    # Treść: Zoptymalizowana Mapa
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 150, "Analiza i zestrojenie mapy (by Alex):")
    
    text_object = c.beginText(50, height - 170)
    text_object.setFont("Helvetica", 10)
    
    # Dzielenie tekstu na linie, żeby nie wyszedł poza PDF
    lines = optimized_result.replace('\n', ' ').split(' ')
    current_line = ""
    for word in lines:
        if len(current_line + word) < 90:
            current_line += word + " "
        else:
            text_object.textLine(current_line)
            current_line = word + " "
    text_object.textLine(current_line)
    
    c.drawText(text_object)

    # Stopka
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 30, "Dokument wygenerowany automatycznie przez mechanizm rozwoju Vis-Sol.")
    
    c.save()
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
