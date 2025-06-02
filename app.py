from flask import Flask, send_from_directory, render_template_string, request, jsonify, session
from flask_cors import CORS
import os
import hmac
import hashlib
import requests
import json
from datetime import datetime
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

# Configure CORS to allow requests from your Render domain
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://chikori-web-app.onrender.com",
            "http://localhost:8080"  # For local development
        ]
    }
})

# Ensure session cookie is secure in production
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))

# TBC API Configuration
TBC_API_KEY = os.getenv('TBC_API_KEY', 'YOUR_API_KEY_HERE')
TBC_MERCHANT_ID = os.getenv('TBC_MERCHANT_ID', 'YOUR_MERCHANT_ID_HERE')
TBC_API_BASE_URL = 'https://api.tbcbank.ge/v1/online-installments'

class TBCInstallmentAPI:
    def __init__(self, api_key, merchant_id, base_url):
        self.api_key = api_key
        self.merchant_id = merchant_id
        self.base_url = base_url

    def _generate_signature(self, payload):
        return hmac.new(
            self.api_key.encode('utf-8'),
            json.dumps(payload).encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def initiate_installment(self, product_data):
        endpoint = f"{self.base_url}/initiate"
        
        payload = {
            "priceTotal": product_data['price'],
            "productId": product_data['id'],
            "quantity": 1,
            "campaignId": product_data.get('campaignId', 'default'),
            "pricePerMonth": product_data.get('pricePerMonth'),
            "invoiceId": f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "installmentType": product_data.get('installmentType', 'standard'),
            "preAuth": True
        }

        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key,
            'merchant-id': self.merchant_id,
            'signature': self._generate_signature(payload)
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def check_status(self, session_id):
        endpoint = f"{self.base_url}/status/{session_id}"
        
        headers = {
            'apikey': self.api_key,
            'merchant-id': self.merchant_id
        }

        try:
            response = requests.get(endpoint, headers=headers)
            return response.json()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# Initialize TBC API client
tbc_client = TBCInstallmentAPI(TBC_API_KEY, TBC_MERCHANT_ID, TBC_API_BASE_URL)

@app.route('/')
def home():
    with open('index.html', 'r') as f:
        html = f.read()
    return render_template_string(html)

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)

@app.route('/api/tbc/initiate', methods=['POST'])
def initiate_tbc_installment():
    try:
        product_data = request.json
        result = tbc_client.initiate_installment(product_data)
        
        if result.get('status') == 'success':
            # Store session information
            session['tbc_session_id'] = result.get('sessionId')
            session['invoice_id'] = product_data.get('invoiceId')
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/tbc/status/<session_id>', methods=['GET'])
def check_tbc_status(session_id):
    try:
        result = tbc_client.check_status(session_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/tbc-callback', methods=['POST'])
def tbc_callback():
    try:
        # Verify callback signature
        signature = request.headers.get('signature')
        payload = request.get_data()
        
        expected_signature = hmac.new(
            TBC_API_KEY.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature or '', expected_signature):
            return jsonify({'status': 'error', 'message': 'Invalid signature'}), 400
        
        data = request.json
        
        # Handle different status updates
        if data['status'] == 'success':
            # Process successful installment
            print(f"Successful installment for session {data.get('sessionId')}")
            # Implement your order fulfillment logic here
            pass
        elif data['status'] == 'failed':
            # Handle failed installment
            print(f"Failed installment for session {data.get('sessionId')}")
            pass
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Ensure all required environment variables are set
    required_env_vars = ['TBC_API_KEY', 'TBC_MERCHANT_ID', 'FLASK_SECRET_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Using default/placeholder values for development.")
    
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
