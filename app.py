import os
from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import requests

app = Flask(__name__)

# Pobieranie klucza z ustawień Render (Environment Variables)
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.form.get('map_data', 'Brak danych')
    client = request.form.get('client_name', 'Vis-Sol')
    
    # Tworzenie PDF
    pdf_path = "oferta_vis_sol.pdf"
    c = canvas.Canvas(pdf_path)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"OFERTA: {client}")
    c.setFont("Helvetica", 10)
    c.drawString(50, 780, f"Dane mapowania: {data[:100]}...")
    c.save()
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
