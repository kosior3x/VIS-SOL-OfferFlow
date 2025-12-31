from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(filename='form_submissions.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    form_data = request.form.to_dict()
    logging.info(f"Contact Form Submission: {form_data}")
    return jsonify({"status": "success", "message": "Form submitted successfully!"})

@app.route('/api/case', methods=['POST'])
def handle_case_form():
    form_data = request.form.to_dict()
    logging.info(f"Case Form Submission: {form_data}")
    return jsonify({"status": "success", "message": "Case submitted successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
