from flask import Flask, jsonify, request
from flask_cors import CORS # Pozwala stronie rozmawiać z serwerem

app = Flask(__name__)
CORS(app) # Ważne: bez tego przeglądarka zablokuje połączenie

@app.route('/api/process', methods=['POST'])
def process_offer():
    data = request.json
    client = data.get('client', 'Nieznany')
    base_val = data.get('val', 0)
    
    # Logika BASS w Pythonie - tu możesz doliczać skomplikowane koszty
    final_val = base_val * 0.9 if data.get('partner') else base_val
    
    return jsonify({
        "status": "processed",
        "client": client,
        "final_val": round(final_val, 2),
        "msg": f"Alex AI: Oferta dla {client} zoptymalizowana pomyślnie."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
