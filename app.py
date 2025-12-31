from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
