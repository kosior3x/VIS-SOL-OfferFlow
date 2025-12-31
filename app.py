
import os
import replicate
from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
import io

# Sprawdzenie klucza API Replicate
if "REPLICATE_API_KEY" not in os.environ:
    raise ValueError("BŁĄD KRYTYCZNY: Klucz API Replicate nie został znaleziony w zmiennych środowiskowych.")

app = Flask(__name__)
CORS(app)

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    client = data.get('client', 'Klient')
    val = data.get('val', 0)
    nr = data.get('nr', 'DOK/001')

    # Generate dynamic content using Replicate AI
    prompt = f"Generate a short, professional and encouraging closing paragraph for a business offer document. The offer is for a client named '{client}' and the total value is {val} PLN. The paragraph should be optimistic and express eagerness to collaborate. Do not include a greeting or a signature, just the paragraph itself. Keep it to 2-3 sentences. Write in Polish."

    try:
        output = replicate.run(
            "meta/llama-2-7b-chat:8e6975e5ed6174911a61d9e2e40b0b204808d3da03552afcb96321580ce109e2",
            input={"prompt": prompt, "max_new_tokens": 128} # limit output length
        )
        ai_message = "".join(output)
    except Exception as e:
        print(f"Replicate API call failed: {e}")
        ai_message = f"Z niecierpliwością oczekujemy na możliwość współpracy z Państwem przy tym projekcie. Jesteśmy przekonani, że nasze rozwiązania przyniosą Państwa firmie, {client}, wymierne korzyści."

    # Tworzenie pliku PDF w pamięci RAM
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Nagłówek VIS-SOL
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "OFERTA HANDLOWA: " + nr)
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, "Podmiot: VIS-SOL (vis-sol.prv.pl)")
    
    p.line(100, 770, 500, 770)

    # Dane klienta i wycena
    p.drawString(100, 740, f"Kontrahent: {client}")
    p.drawString(100, 720, f"Kwota netto: {val} PLN")
    
    # Dynamicznie generowana treść
    p.setFont("Helvetica", 11)
    y_position = 680
    lines = simpleSplit(ai_message, 'Helvetica', 11, 400) # 400 = page_width - margins
    for line in lines:
        p.drawString(100, y_position, line)
        y_position -= 15 # Move down for next line

    # Klauzula BASS i Tajemnica
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(100, 150, "Dokument wygenerowany automatycznie przez system Alex BASS.")
    p.drawString(100, 135, "TAJEMNICA HANDLOWA VIS-SOL - DOSTĘP ZASTRZEŻONY.")

    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Oferta_{client}.pdf", mimetype='application/pdf')

@app.route('/preview')
def preview():
    return send_from_directory('.', 'test.html')

@app.route('/generate-test-pdf')
def generate_test_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "TESTOWY DOKUMENT PDF")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, "Wygenerowano z Vis-Flow")

    p.line(100, 770, 500, 770)
    p.drawString(100, 740, "To jest testowy dokument PDF.")

    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Testowy.pdf", mimetype='application/pdf')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
