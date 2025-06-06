from flask import Flask, send_from_directory, render_template_string, request, jsonify, session, redirect, url_for
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

# Debug: Print loaded environment variables
print("=== Loaded Environment Variables ===")
print(f"TBC_API_KEY: {os.getenv('TBC_API_KEY')}")
print(f"TBC_MERCHANT_ID: {os.getenv('TBC_MERCHANT_ID')}")
print(f"TBC_CAMPAIGN_ID: {os.getenv('TBC_CAMPAIGN_ID')}")
print(f"Has TBC_SECRET: {'Yes' if os.getenv('TBC_SECRET') else 'No'}")
print("================================")

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
TBC_API_KEY = os.getenv('TBC_API_KEY')
TBC_SECRET = os.getenv('TBC_SECRET')
TBC_MERCHANT_ID = os.getenv('TBC_MERCHANT_ID')
TBC_CAMPAIGN_ID = os.getenv('TBC_CAMPAIGN_ID', '204')
TBC_API_BASE_URL = 'https://test-api.tbcbank.ge'  # Use 'https://api.tbcbank.ge' for production
TBC_TOKEN_CACHE = {}

if not TBC_API_KEY or not TBC_MERCHANT_ID or not TBC_SECRET:
    print("WARNING: Missing TBC credentials!")
    print("Please ensure your .env file exists and contains the correct credentials.")

class TBCInstallmentAPI:
    def __init__(self, api_key, merchant_id, base_url):
        self.api_key = api_key
        self.secret = os.getenv('TBC_SECRET')
        self.merchant_id = merchant_id
        self.base_url = base_url
        self.access_token = None

    def _get_access_token(self):
        """Get OAuth access token from TBC Bank"""
        try:
            # Check if we have a cached token that's still valid
            if self.access_token and TBC_TOKEN_CACHE.get('expires_at', 0) > datetime.now().timestamp():
                return self.access_token

            # Prepare the token request
            token_url = f"{self.base_url}/oauth/token"
            auth = (self.api_key, self.secret)
            data = {
                'grant_type': 'client_credentials',
                'scope': 'online_installments'
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.post(token_url, auth=auth, data=data, headers=headers)
            
            if response.ok:
                token_data = response.json()
                self.access_token = token_data['access_token']
                # Cache the token with expiration
                TBC_TOKEN_CACHE['token'] = self.access_token
                TBC_TOKEN_CACHE['expires_at'] = datetime.now().timestamp() + (token_data['expires_in'] / 1000)
                return self.access_token
            else:
                print(f"Failed to get access token: {response.text}")
                return None

        except Exception as e:
            print(f"Error getting access token: {str(e)}")
            return None

    def _generate_signature(self, payload):
        # Use the secret key for HMAC signature generation
        return hmac.new(
            self.secret.encode('utf-8'),
            json.dumps(payload, sort_keys=True).encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def initiate_installment(self, product_data):
        try:
            # Get access token first
            access_token = self._get_access_token()
            if not access_token:
                return {
                    'status': 'error',
                    'message': 'Failed to get access token'
                }

            endpoint = f"{self.base_url}/v1/online-installments/applications"
            
            # Format the payload according to TBC documentation
            payload = {
                "merchantKey": self.merchant_id,  # Using merchant_id as merchantKey
                "priceTotal": float(product_data['price']),  # Convert to float for decimal
                "campaignId": TBC_CAMPAIGN_ID,
                "invoiceId": f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "products": [
                    {
                        "name": product_data.get('name', 'Product'),
                        "price": float(product_data['price']),
                        "quantity": 1
                    }
                ]
            }

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            print("=== TBC API Request ===")
            print(f"Endpoint: {endpoint}")
            print(f"Headers: {headers}")
            print(f"Payload: {payload}")
            print("=====================")

            response = requests.post(endpoint, json=payload, headers=headers)
            
            print("=== TBC API Response ===")
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text}")
            print("=====================")

            if response.ok:
                try:
                    response_data = response.json()
                    if 'sessionId' in response_data:
                        # Get the redirect URL from Location header or construct it
                        redirect_url = response.headers.get('Location')
                        if not redirect_url:
                            # If no Location header, construct the URL (you may need to adjust this URL)
                            redirect_url = f"https://tbcinstallment.ge/checkout/{response_data['sessionId']}"
                        
                        return {
                            'status': 'success',
                            'sessionId': response_data['sessionId'],
                            'redirectUrl': redirect_url
                        }
                    return response_data
                except ValueError:
                    return {
                        'status': 'error',
                        'message': f"Invalid JSON response with status code {response.status_code}"
                    }
            else:
                error_msg = response.text
                try:
                    error_json = response.json()
                    if 'detail' in error_json:
                        error_msg = error_json['detail']
                except:
                    pass
                return {
                    'status': 'error',
                    'message': f"Payment initialization failed: {error_msg}"
                }

        except Exception as e:
            print(f"Exception in TBC API call: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def confirm_installment(self, session_id):
        access_token = self._get_access_token()
        if not access_token:
            return {'status': 'error', 'message': 'Failed to get access token'}

        endpoint = f"{self.base_url}/v1/online-installments/applications/{session_id}/confirm"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'merchant-id': self.merchant_id
        }

        try:
            response = requests.post(endpoint, headers=headers)
            return response.json()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def check_status(self, session_id):
        access_token = self._get_access_token()
        if not access_token:
            return {'status': 'error', 'message': 'Failed to get access token'}

        endpoint = f"{self.base_url}/v1/online-installments/applications/{session_id}"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
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
        print(f"Received product data: {product_data}")
        
        if not TBC_API_KEY or TBC_API_KEY == 'YOUR_API_KEY_HERE':
            return jsonify({
                'status': 'error',
                'message': 'TBC API key not configured'
            }), 500
            
        if not TBC_MERCHANT_ID or TBC_MERCHANT_ID == 'YOUR_MERCHANT_ID_HERE':
            return jsonify({
                'status': 'error',
                'message': 'TBC Merchant ID not configured'
            }), 500

        result = tbc_client.initiate_installment(product_data)
        print(f"TBC initiation result: {result}")

        if 'redirectUrl' in result:
            return jsonify({
                'status': 'success',
                'redirectUrl': result['redirectUrl']
            })
        else:
            return jsonify(result), 400

    except Exception as e:
        print(f"Exception in initiate_tbc_installment: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/tbc/confirm/<session_id>', methods=['POST'])
def confirm_tbc_installment(session_id):
    try:
        result = tbc_client.confirm_installment(session_id)
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

@app.route('/payment-success')
def payment_success():
    session_id = request.args.get('sessionId')
    if session_id:
        # Confirm the installment after successful redirect
        result = tbc_client.confirm_installment(session_id)
        if result.get('status') == 'success':
            return redirect(url_for('home', status='success'))
    return redirect(url_for('home', status='error'))

@app.route('/payment-failure')
def payment_failure():
    return redirect(url_for('home', status='failure'))

@app.route('/tbc-callback', methods=['POST'])
def tbc_callback():
    try:
        # Verify callback signature using secret
        signature = request.headers.get('signature')
        payload = request.get_data()
        
        expected_signature = hmac.new(
            TBC_SECRET.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature or '', expected_signature):
            return jsonify({'status': 'error', 'message': 'Invalid signature'}), 400
        
        data = request.json
        session_id = data.get('sessionId')
        
        if data['status'] == 'success':
            # Confirm the installment
            confirm_result = tbc_client.confirm_installment(session_id)
            if confirm_result.get('status') != 'success':
                return jsonify({'status': 'error', 'message': 'Confirmation failed'}), 500
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/tbc-credentials')
def tbc_credentials():
    return jsonify({
        'apiKey': TBC_API_KEY,
        'merchantId': TBC_MERCHANT_ID
    })

if __name__ == '__main__':
    # Ensure all required environment variables are set
    required_env_vars = ['TBC_API_KEY', 'TBC_MERCHANT_ID', 'FLASK_SECRET_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Using default/placeholder values for development.")
    
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
