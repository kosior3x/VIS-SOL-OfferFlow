from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import io

app = Flask(__name__, static_folder='', static_url_path='')
CORS(app, origins=["https://vis-sol.prv.pl", "https://vis-sol-offerflow.onrender.com"])

@app.route('/health', methods=['GET'])
def health():
    return jsonify(status="ok"), 200

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    tool_id = data.get('tool_id')

    if tool_id == 'generator-ofert':
        return generate_offer_pdf(data)
    elif tool_id == 'kalkulator-bdo':
        return jsonify(message="Kalkulator BDO - w budowie"), 200
    elif tool_id == 'monitoring':
        return jsonify(message="Monitoring - w budowie"), 200
    else:
        return jsonify(error="Invalid tool_id"), 400

def generate_offer_pdf(data):
    client = data.get('client', 'Klient')
    val = data.get('val', 0)
    nr = data.get('nr', 'DOK/001')

    # Tworzenie pliku PDF w pamięci RAM
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Nagłówek VIS-SOL 2.0
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, 800, "OFERTA HANDLOWA: VIS-SOL 2.0")
    p.setFont("Helvetica", 10)
    p.drawString(100, 780, f"Numer dokumentu: {nr}")

    # Tabela z danymi
    table_data = [
        ['Kontrahent', client],
        ['Kwota netto', f'{val} PLN']
    ]
    
    table = Table(table_data, colWidths=[150, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    table.wrapOn(p, 400, 200)
    table.drawOn(p, 100, 680)
    
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
