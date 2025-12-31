from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://vis-sol-offerflow.onrender.com", "http://vis-sol.prv.pl", "https://vis-sol.prv.pl"]}})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    client = data.get('client', 'Klient')
    val = data.get('val', 0)
    nr = data.get('nr', 'DOK/001')

    # Tworzenie pliku PDF w pamięci RAM
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Nagłówek VIS-SOL 2.0
    p.setFont("Helvetica-Bold", 18)
    p.drawString(72, 800, "VIS-SOL 2.0")
    p.setFont("Helvetica", 12)
    p.drawString(72, 780, "OFERTA HANDLOWA: " + nr)
    
    # Tabela z danymi
    p.line(70, 750, 525, 750)
    p.drawString(75, 725, f"Kontrahent:")
    p.drawString(250, 725, f"{client}")
    p.drawString(75, 700, f"Wartość netto:")
    p.drawString(250, 700, f"{val} PLN")
    p.line(70, 680, 525, 680)
    
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
