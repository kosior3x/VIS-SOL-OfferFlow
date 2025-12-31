from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "VIS-SOL Reaktor: System operacyjny Alex jest aktywny."

@app.route('/api/status', methods=['GET'])
def status():
    # Tutaj Alex będzie zwracać parametry stabilności systemu
    return jsonify({
        "status": "online",
        "engine": "Python 3.9",
        "version": "2.5-BASS",
        "stability": "98%"
    })

if __name__ == '__main__':
    app.run(debug=True)
