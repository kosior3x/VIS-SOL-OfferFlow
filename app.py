from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    client = data.get('client', 'Klient')
    val = data.get('val', 0)
    nr = data.get('nr', 'DOK/001')

    # Tworzenie pliku PDF w pamięci RAM
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Nagłówek VIS-SOL
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "OFERTA HANDLOWA: " + nr)
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, "Podmiot: VIS-SOL (vis-sol.prv.pl)")
    
    # Dane klienta i wycena
    p.line(100, 770, 500, 770)
    p.drawString(100, 740, f"Kontrahent: {client}")
    p.drawString(100, 720, f"Kwota netto: {val} PLN")
    
    # Klauzula BASS i Tajemnica
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(100, 150, "Dokument wygenerowany automatycznie przez system Alex BASS.")
    p.drawString(100, 135, "TAJEMNICA HANDLOWA VIS-SOL - DOSTĘP ZASTRZEŻONY.")

    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Oferta_{client}.pdf", mimetype='application/pdf')

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    data = request.json
    print("Received form submission:")
    print(json.dumps(data, indent=2))
    return jsonify({"success": True, "message": "Form submitted successfully!"})

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
