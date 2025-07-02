from flask import Flask, send_from_directory, request, jsonify, redirect, url_for, session, render_template_string
import os
import time
import hashlib
import requests
import json
from datetime import datetime
from config import FLITT_CONFIG, TBC_CONFIG, IS_PRODUCTION

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

# Set Flask environment and secret key for sessions
if IS_PRODUCTION:
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
else:
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True

# Secret key for sessions (you should set this in environment variables for production)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# User management functions
def load_users():
    """Load users from JSON file"""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": []}

def save_users(users_data):
    """Save users to JSON file"""
    with open('users.json', 'w') as f:
        json.dump(users_data, f, indent=2)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_user_exists(email):
    """Check if user already exists"""
    users_data = load_users()
    return any(user['email'] == email for user in users_data['users'])

def verify_user(email, password):
    """Verify user credentials"""
    users_data = load_users()
    hashed_password = hash_password(password)
    for user in users_data['users']:
        if user['email'] == email and user['password'] == hashed_password:
            return user
    return None

def generate_signature(order_data, secret_key):
    """Generate signature for Flitt API request (SHA1, Flitt format)"""
    # Format: secret_key|amount|currency|merchant_id|order_desc|order_id|server_callback_url
    signature_string = f"{secret_key}|{order_data['amount']}|{order_data['currency']}|{order_data['merchant_id']}|{order_data['order_desc']}|{order_data['order_id']}|{order_data['server_callback_url']}"
    signature = hashlib.sha1(signature_string.encode('utf-8')).hexdigest()
    print(f"Signature generation:")
    print(f"  String: {signature_string}")
    print(f"  Signature: {signature}")
    return signature

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/api/create-payment', methods=['POST'])
def create_payment():
    """Create a payment order using direct Flitt API call"""
    try:
        # Log incoming request details
        print("=== INCOMING PAYMENT REQUEST ===")
        print(f"Request Method: {request.method}")
        print(f"Request URL: {request.url}")
        print(f"Request Headers: {dict(request.headers)}")
        print(f"Request Content-Type: {request.content_type}")
        print(f"Request Content-Length: {request.content_length}")
        
        data = request.get_json()
        print(f"Request Body: {data}")
        
        product_id = data.get('product_id')
        amount = data.get('amount')
        
        print(f"Product ID: {product_id}")
        print(f"Amount: {amount}")
        
        # Get product details
        product = get_product_by_id(product_id)
        if not product:
            error_response = {'error': 'Product not found', 'product_id': product_id}
            print(f"Product not found: {error_response}")
            return jsonify(error_response), 404
        
        print(f"Product found: {product}")
        
        # Create order data in Flitt format
        order_id = f"order_{product_id}_{int(time.time())}"
        order_amount = int(amount * 100)  # Convert to cents
        
        order_data = {
            'merchant_id': int(FLITT_CONFIG['merchant_id']),
            'order_id': order_id,
            'currency': FLITT_CONFIG['currency'],
            'order_desc': f"შეძენა: {product['name']}",
            'amount': order_amount,
            'server_callback_url': request.host_url.rstrip('/') + '/payment-callback'
        }
        
        # Generate signature
        signature = generate_signature(order_data, FLITT_CONFIG['secret_key'])
        order_data['signature'] = signature
        
        # Create request payload in Flitt format
        request_payload = {
            'request': order_data
        }
        
        print("=== FLITT API REQUEST ===")
        print(f"API URL: https://pay.flitt.com/api/checkout/url")
        print(f"Merchant ID: {FLITT_CONFIG['merchant_id']}")
        print(f"Secret Key: {FLITT_CONFIG['secret_key'][:10]}...")
        print(f"Order data: {order_data}")
        print(f"Full request payload: {request_payload}")
        
        # Make direct HTTP request to Flitt API
        print("Making HTTP request to Flitt API...")
        response = requests.post(
            'https://pay.flitt.com/api/checkout/url',
            headers={'Content-Type': 'application/json'},
            json=request_payload,
            timeout=30
        )
        
        print("=== FLITT API RESPONSE ===")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        try:
            response_data = response.json()
            print(f"Response JSON: {response_data}")
        except Exception as e:
            print(f"Failed to parse JSON response: {e}")
            response_data = {'error': 'Invalid JSON response', 'text': response.text}
        
        if response.status_code == 200 and response_data.get('response', {}).get('response_status') == 'success':
            checkout_url = response_data['response']['checkout_url']
            
            success_response = {
                'success': True,
                'checkout_url': checkout_url,
                'debug_info': {
                    'request': {
                        'product_id': product_id,
                        'amount': amount,
                        'product': product
                    },
                    'flitt_request': request_payload,
                    'flitt_response': response_data,
                    'merchant_config': {
                        'merchant_id': FLITT_CONFIG['merchant_id'],
                        'test_mode': FLITT_CONFIG['test_mode'],
                        'base_url': FLITT_CONFIG['base_url']
                    }
                }
            }
            print(f"Success response: {success_response}")
            return jsonify(success_response)
        else:
            error_message = response_data.get('response', {}).get('error_message', 'Unknown error')
            error_code = response_data.get('response', {}).get('error_code', 'Unknown')
            
            error_response = {
                'success': False,
                'error': f"Flitt API error: {error_message} (Code: {error_code})",
                'details': response_data,
                'debug_info': {
                    'request': {
                        'product_id': product_id,
                        'amount': amount,
                        'product': product
                    },
                    'flitt_request': request_payload,
                    'flitt_response': response_data,
                    'merchant_config': {
                        'merchant_id': FLITT_CONFIG['merchant_id'],
                        'test_mode': FLITT_CONFIG['test_mode'],
                        'base_url': FLITT_CONFIG['base_url']
                    }
                }
            }
            print(f"Error response: {error_response}")
            return jsonify(error_response), 400
            
    except Exception as e:
        print("=== PAYMENT CREATION EXCEPTION ===")
        print(f"Exception type: {type(e)}")
        print(f"Exception message: {str(e)}")
        print(f"Exception args: {e.args}")
        
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        
        error_response = {
            'success': False,
            'error': str(e),
            'debug_info': {
                'exception_type': str(type(e)),
                'exception_message': str(e),
                'traceback': traceback.format_exc()
            }
        }
        return jsonify(error_response), 500

@app.route('/payment-result', methods=['GET', 'POST'])
def payment_result():
    status = request.args.get('status') or request.args.get('response_status') or request.form.get('response_status')
    payment_type = request.args.get('payment_type', 'flitt')
    
    if status == 'success':
        return redirect(url_for('home', status='success', payment_type=payment_type))
    else:
        return redirect(url_for('home', status='failure', payment_type=payment_type))

@app.route('/payment-callback', methods=['POST'])
def payment_callback():
    """Handle server callback from Flitt"""
    try:
        data = request.get_json()
        print("=== PAYMENT CALLBACK RECEIVED ===")
        print(f"Callback data: {data}")
        
        # Extract callback data
        order_id = data.get('order_id')
        status = data.get('response_status')
        amount = data.get('amount')
        signature = data.get('signature')
        
        # Verify signature manually (SHA1)
        if signature:
            # Format: secret_key|amount|currency|merchant_id|order_desc|order_id|server_callback_url
            callback_signature_string = f"{FLITT_CONFIG['secret_key']}|{amount}|{data.get('currency')}|{data.get('merchant_id')}|{data.get('order_desc')}|{order_id}|{data.get('server_callback_url')}"
            expected_signature = hashlib.sha1(callback_signature_string.encode('utf-8')).hexdigest()
            print(f"Signature verification:")
            print(f"  Received signature: {signature}")
            print(f"  Expected signature: {expected_signature}")
            print(f"  Signature string: {callback_signature_string}")
            if signature != expected_signature:
                print("❌ Invalid signature in callback")
                return jsonify({'error': 'Invalid signature'}), 400
            else:
                print("✅ Signature verified successfully")
        
        # Process the callback
        print(f"Payment callback processed: Order {order_id}, Status: {status}, Amount: {amount}")
        # Here you would typically update your DB, send emails, etc.
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Callback error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/tbc-installment-callback', methods=['GET', 'POST'])
def tbc_installment_callback():
    """Handle callback from TBC installment application"""
    try:
        print("=== TBC INSTALLMENT CALLBACK ===")
        print(f"Request Method: {request.method}")
        print(f"Request URL: {request.url}")
        print(f"Request Headers: {dict(request.headers)}")
        print(f"Request Args: {dict(request.args)}")
        
        if request.method == 'POST':
            print(f"Request Body: {request.get_data(as_text=True)}")
            callback_data = request.get_json()
        else:
            callback_data = dict(request.args)
        
        # Extract important fields
        session_id = callback_data.get('sessionId') or callback_data.get('session_id')
        invoice_id = callback_data.get('invoiceId') or callback_data.get('invoice_id')
        status = callback_data.get('status')
        
        print(f"TBC Installment callback: Session {session_id}, Invoice {invoice_id}, Status {status}")
        
        # Redirect to payment result page with status
        if status == 'success':
            return redirect(url_for('payment_result', status='success', payment_type='tbc_installment'))
        else:
            return redirect(url_for('payment_result', status='failure', payment_type='tbc_installment'))
            
    except Exception as e:
        print(f"TBC callback error: {str(e)}")
        return redirect(url_for('payment_result', status='failure', payment_type='tbc_installment'))

@app.route('/api/check-env')
def check_env():
    """Check environment variables (for debugging) - Only available in development"""
    if IS_PRODUCTION:
        return jsonify({'error': 'Environment check not available in production'}), 403
    
    env_vars = {
        'FLITT_MERCHANT_ID': os.environ.get('FLITT_MERCHANT_ID', 'NOT SET'),
        'FLITT_SECRET_KEY': os.environ.get('FLITT_SECRET_KEY', 'NOT SET')[:10] + '...' if os.environ.get('FLITT_SECRET_KEY') else 'NOT SET',
        'FLITT_BASE_URL': os.environ.get('FLITT_BASE_URL', 'NOT SET'),
        'FLITT_TEST_MODE': os.environ.get('FLITT_TEST_MODE', 'NOT SET'),
        'TBC_API_KEY': os.environ.get('TBC_API_KEY', 'NOT SET')[:10] + '...' if os.environ.get('TBC_API_KEY') else 'NOT SET',
        'TBC_API_SECRET': os.environ.get('TBC_API_SECRET', 'NOT SET')[:10] + '...' if os.environ.get('TBC_API_SECRET') else 'NOT SET',
        'TBC_MERCHANT_KEY': os.environ.get('TBC_MERCHANT_KEY', 'NOT SET')[:10] + '...' if os.environ.get('TBC_MERCHANT_KEY') else 'NOT SET',
        'TBC_TEST_MODE': os.environ.get('TBC_TEST_MODE', 'NOT SET'),
        'TBC_CAMPAIGN_ID': os.environ.get('TBC_CAMPAIGN_ID', 'NOT SET'),
        'FLASK_ENV': os.environ.get('FLASK_ENV', 'NOT SET'),
    }
    return jsonify({
        'status': 'Environment check',
        'environment': 'PRODUCTION' if IS_PRODUCTION else 'DEVELOPMENT',
        'variables': env_vars,
        'config': {
            'flitt': {
                'merchant_id': FLITT_CONFIG['merchant_id'],
                'base_url': FLITT_CONFIG['base_url'],
                'test_mode': FLITT_CONFIG['test_mode']
            },
            'tbc': {
                'base_url': TBC_CONFIG['base_url'],
                'test_mode': TBC_CONFIG['test_mode'],
                'campaign_id': TBC_CONFIG['campaign_id']
            },
            'is_production': IS_PRODUCTION
        }
    })



# TBC Online Installment Functions
def get_tbc_access_token():
    """Get TBC access token for API authentication"""
    try:
        print("=== TBC ACCESS TOKEN REQUEST ===")
        
        # Prepare OAuth request
        oauth_url = f"{TBC_CONFIG['base_url']}{TBC_CONFIG['oauth_url']}"
        
        # OAuth credentials should be sent as form data
        oauth_data = {
            'grant_type': 'client_credentials',
            'client_id': TBC_CONFIG['api_key'],
            'client_secret': TBC_CONFIG['api_secret']
        }
        
        print(f"OAuth URL: {oauth_url}")
        print(f"Client ID: {TBC_CONFIG['api_key']}")
        print(f"Client Secret: {TBC_CONFIG['api_secret'][:10]}...")
        
        # Make OAuth request
        response = requests.post(
            oauth_url,
            data=oauth_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=30
        )
        
        print(f"OAuth Response Status: {response.status_code}")
        print(f"OAuth Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            print(f"Access Token: {access_token[:20]}...")
            return access_token
        else:
            print(f"OAuth failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error getting TBC access token: {str(e)}")
        return None

def create_tbc_installment_application(product_id, amount, user_email=None):
    """Create TBC online installment application"""
    try:
        print("=== TBC INSTALLMENT APPLICATION REQUEST ===")
        
        # Get access token
        access_token = get_tbc_access_token()
        if not access_token:
            return {
                'success': False,
                'error': 'Failed to get TBC access token'
            }
        
        # Get product details
        product = get_product_by_id(product_id)
        if not product:
            return {
                'success': False,
                'error': 'Product not found'
            }
        
        # Generate unique invoice ID
        invoice_id = f"inv_{product_id}_{int(time.time())}"
        
        # Prepare installment application request
        installment_url = f"{TBC_CONFIG['base_url']}{TBC_CONFIG['installment_url']}"
        
        application_data = {
            'merchantKey': TBC_CONFIG['merchant_key'],
            'priceTotal': float(amount),
            'campaignId': str(TBC_CONFIG['campaign_id']),  # String as per TBC docs
            'invoiceId': invoice_id,
            'products': [
                {
                    'name': product['name'],
                    'price': float(amount),
                    'quantity': 1
                }
            ]
        }
        
        print(f"Installment URL: {installment_url}")
        print(f"Merchant Key: {TBC_CONFIG['merchant_key']}")
        print(f"Application Data: {application_data}")
        
        # Make installment application request
        response = requests.post(
            installment_url,
            json=application_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            },
            timeout=30
        )
        
        print(f"Installment Response Status: {response.status_code}")
        print(f"Installment Response Headers: {dict(response.headers)}")
        print(f"Installment Response: {response.text}")
        
        if response.status_code == 201:  # Created
            response_data = response.json()
            session_id = response_data.get('sessionId')
            redirect_url = response.headers.get('Location')
            
            if session_id and redirect_url:
                print(f"Session ID: {session_id}")
                print(f"Redirect URL: {redirect_url}")
                
                return {
                    'success': True,
                    'session_id': session_id,
                    'redirect_url': redirect_url,
                    'invoice_id': invoice_id,
                    'debug_info': {
                        'request': application_data,
                        'response': response_data,
                        'headers': dict(response.headers)
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'Missing session ID or redirect URL in response',
                    'response': response_data
                }
        else:
            try:
                error_data = response.json()
                error_message = error_data.get('message', 'Unknown error')
            except:
                error_message = response.text
            
            return {
                'success': False,
                'error': f'TBC API error: {error_message}',
                'status_code': response.status_code,
                'response': response.text
            }
            
    except Exception as e:
        print(f"Error creating TBC installment application: {str(e)}")
        return {
            'success': False,
            'error': f'Exception: {str(e)}'
        }

@app.route('/api/tbc-installment', methods=['POST'])
def tbc_installment():
    """Handle TBC online installment application"""
    try:
        print("=== TBC INSTALLMENT REQUEST ===")
        print(f"Request Method: {request.method}")
        print(f"Request URL: {request.url}")
        print(f"Request Headers: {dict(request.headers)}")
        
        data = request.get_json()
        print(f"Request Body: {data}")
        
        product_id = data.get('product_id')
        amount = data.get('amount')
        
        if not product_id or not amount:
            return jsonify({
                'success': False,
                'error': 'Product ID and amount are required'
            }), 400
        
        # Create installment application
        result = create_tbc_installment_application(product_id, amount)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        print(f"TBC installment error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/tbc-installment/<session_id>/cancel', methods=['POST'])
def cancel_tbc_installment(session_id):
    """Cancel TBC installment application"""
    try:
        print(f"=== CANCEL TBC INSTALLMENT: {session_id} ===")
        
        # Get access token
        access_token = get_tbc_access_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Failed to get TBC access token'
            }), 500
        
        # Cancel application
        cancel_url = f"{TBC_CONFIG['base_url']}/v1/online-installments/applications/{session_id}/cancel"
        
        response = requests.post(
            cancel_url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            },
            timeout=30
        )
        
        print(f"Cancel Response Status: {response.status_code}")
        print(f"Cancel Response: {response.text}")
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Installment application cancelled successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to cancel application: {response.status_code}'
            }), 400
            
    except Exception as e:
        print(f"Cancel installment error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/tbc-installment/<session_id>/confirm', methods=['POST'])
def confirm_tbc_installment(session_id):
    """Confirm TBC installment application"""
    try:
        print(f"=== CONFIRM TBC INSTALLMENT: {session_id} ===")
        
        # Get access token
        access_token = get_tbc_access_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Failed to get TBC access token'
            }), 500
        
        # Confirm application
        confirm_url = f"{TBC_CONFIG['base_url']}/v1/online-installments/applications/{session_id}/confirm"
        
        response = requests.post(
            confirm_url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            },
            timeout=30
        )
        
        print(f"Confirm Response Status: {response.status_code}")
        print(f"Confirm Response: {response.text}")
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Installment application confirmed successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to confirm application: {response.status_code}'
            }), 400
            
    except Exception as e:
        print(f"Confirm installment error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/tbc-installment/<session_id>/status', methods=['GET'])
def get_tbc_installment_status(session_id):
    """Get TBC installment application status"""
    try:
        print(f"=== GET TBC INSTALLMENT STATUS: {session_id} ===")
        
        # Get access token
        access_token = get_tbc_access_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Failed to get TBC access token'
            }), 500
        
        # Get application status
        status_url = f"{TBC_CONFIG['base_url']}/v1/online-installments/applications/{session_id}/status"
        
        response = requests.get(
            status_url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            },
            timeout=30
        )
        
        print(f"Status Response Status: {response.status_code}")
        print(f"Status Response: {response.text}")
        
        if response.status_code == 200:
            status_data = response.json()
            return jsonify({
                'success': True,
                'status': status_data
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to get status: {response.status_code}'
            }), 400
            
    except Exception as e:
        print(f"Get status error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/tbc-installment/merchant/status-changes', methods=['GET'])
def get_merchant_status_changes():
    """Get merchant application status changes"""
    try:
        print("=== GET MERCHANT STATUS CHANGES ===")
        
        # Get access token
        access_token = get_tbc_access_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Failed to get TBC access token'
            }), 500
        
        # Get merchant status changes
        status_url = f"{TBC_CONFIG['base_url']}/v1/online-installments/merchant/applications/status-changes"
        
        response = requests.get(
            status_url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            },
            timeout=30
        )
        
        print(f"Merchant Status Response Status: {response.status_code}")
        print(f"Merchant Status Response: {response.text}")
        
        if response.status_code == 200:
            status_data = response.json()
            return jsonify({
                'success': True,
                'status_changes': status_data
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to get merchant status changes: {response.status_code}'
            }), 400
            
    except Exception as e:
        print(f"Get merchant status changes error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/tbc-installment/merchant/status-changes-sync', methods=['POST'])
def sync_merchant_status_changes():
    """Confirm merchant application status synchronization"""
    try:
        print("=== SYNC MERCHANT STATUS CHANGES ===")
        
        # Get access token
        access_token = get_tbc_access_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Failed to get TBC access token'
            }), 500
        
        # Sync status changes
        sync_url = f"{TBC_CONFIG['base_url']}/v1/online-installments/merchant/applications/status-changes-sync"
        
        response = requests.post(
            sync_url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            },
            timeout=30
        )
        
        print(f"Sync Response Status: {response.status_code}")
        print(f"Sync Response: {response.text}")
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Status changes synchronized successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to sync status changes: {response.status_code}'
            }), 400
            
    except Exception as e:
        print(f"Sync status changes error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        if check_user_exists(email):
            return jsonify({'success': False, 'error': 'User already exists'}), 400
        
        # Create new user
        users_data = load_users()
        new_user = {
            'email': email,
            'password': hash_password(password),
            'created_at': datetime.now().isoformat()
        }
        users_data['users'].append(new_user)
        save_users(users_data)
        
        # Log user in
        session['user_email'] = email
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    # GET request - show registration form
    register_html = '''
    <!DOCTYPE html>
    <html lang="ka">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>რეგისტრაცია - ჩიკორი</title>
        <link rel="stylesheet" href="style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />
        <style>
            .auth-page {
                min-height: 100vh;
                background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .auth-container {
                background: var(--white);
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                width: 100%;
                max-width: 450px;
                position: relative;
            }
            .auth-header {
                background: var(--primary-color);
                color: var(--white);
                padding: 2rem;
                text-align: center;
            }
            .auth-header h1 {
                font-size: 1.75rem;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }
            .auth-header p {
                opacity: 0.9;
                font-size: 0.9rem;
            }
            .auth-body {
                padding: 2rem;
            }
            .auth-form {
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
            }
            .form-group {
                position: relative;
            }
            .form-group label {
                display: block;
                margin-bottom: 0.5rem;
                font-weight: 500;
                color: var(--text-color);
                font-size: 0.9rem;
            }
            .form-group input {
                width: 100%;
                padding: 0.875rem 1rem;
                border: 2px solid var(--border-color);
                border-radius: var(--border-radius);
                font-size: 1rem;
                transition: border-color 0.3s ease;
                background: var(--white);
            }
            .form-group input:focus {
                outline: none;
                border-color: var(--accent-color);
            }
            .form-group input::placeholder {
                color: #999;
            }
            .submit-btn {
                background: var(--primary-color);
                color: var(--white);
                border: none;
                padding: 1rem;
                border-radius: var(--border-radius);
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.2s ease;
                margin-top: 0.5rem;
            }
            .submit-btn:hover {
                background: var(--secondary-color);
                transform: translateY(-1px);
            }
            .submit-btn:active {
                transform: translateY(0);
            }
            .auth-links {
                text-align: center;
                margin-top: 1.5rem;
                padding-top: 1.5rem;
                border-top: 1px solid var(--border-color);
            }
            .auth-links a {
                color: var(--accent-color);
                text-decoration: none;
                font-weight: 500;
                transition: color 0.3s ease;
            }
            .auth-links a:hover {
                color: var(--secondary-color);
                text-decoration: underline;
            }
            .error-message {
                background: #fee;
                color: #c33;
                padding: 0.75rem;
                border-radius: var(--border-radius);
                text-align: center;
                font-size: 0.9rem;
                border: 1px solid #fcc;
                margin-top: 1rem;
                display: none;
            }
            .success-message {
                background: #efe;
                color: #363;
                padding: 0.75rem;
                border-radius: var(--border-radius);
                text-align: center;
                font-size: 0.9rem;
                border: 1px solid #cfc;
                margin-top: 1rem;
                display: none;
            }
            .back-home {
                position: absolute;
                top: 1rem;
                left: 1rem;
                color: var(--white);
                text-decoration: none;
                font-size: 0.9rem;
                opacity: 0.8;
                transition: opacity 0.3s ease;
            }
            .back-home:hover {
                opacity: 1;
            }
            .back-home i {
                margin-right: 0.5rem;
            }
            .loading {
                opacity: 0.7;
                pointer-events: none;
            }
            .loading .submit-btn {
                position: relative;
            }
            .loading .submit-btn::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 20px;
                height: 20px;
                margin: -10px 0 0 -10px;
                border: 2px solid transparent;
                border-top: 2px solid var(--white);
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .checkbox-label {
                display: inline-flex;
                align-items: center;
                cursor: pointer;
                font-size: 0.9rem;
                color: var(--text-color);
                gap: 0.5rem;
            }
            .checkbox-label input[type="checkbox"] {
                width: auto;
                margin: 0;
            }
            .checkbox-label a {
                color: var(--accent-color);
                text-decoration: none;
            }
            .checkbox-label a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="auth-page">
            <div class="auth-container">
                <a href="/" class="back-home">
                    <i class="fas fa-arrow-left"></i>
                    მთავარი გვერდი
                </a>
                <div class="auth-header">
                    <h1>შეუერთდით ჩიკორის</h1>
                    <p>შექმენით თქვენი ანგარიში</p>
                </div>
                <div class="auth-body">
                    <form class="auth-form" id="registerForm">
                        <div class="form-group">
                            <label for="email">ელ-ფოსტა</label>
                            <input type="email" id="email" placeholder="შეიყვანეთ თქვენი ელ-ფოსტა" required>
                        </div>
                        <div class="form-group">
                            <label for="password">პაროლი</label>
                            <input type="password" id="password" placeholder="შეიყვანეთ თქვენი პაროლი" required>
                        </div>
                        <div class="form-group">
                            <label class="checkbox-label">
                                <input type="checkbox" id="terms" required>
                                ვეთანხმები <a href="/info.html" target="_blank">წესებს და პირობებს</a>
                            </label>
                        </div>
                        <button type="submit" class="submit-btn">
                            <span>რეგისტრაცია</span>
                        </button>
                    </form>
                    <div class="auth-links">
                        <a href="/login">უკვე გაქვთ ანგარიში? <strong>შედით</strong></a>
                    </div>
                    <div id="errorMessage" class="error-message"></div>
                    <div id="successMessage" class="success-message"></div>
                </div>
            </div>
        </div>
        
        <script>
            document.getElementById('registerForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const form = document.getElementById('registerForm');
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                const errorMessage = document.getElementById('errorMessage');
                const successMessage = document.getElementById('successMessage');
                
                // Hide previous messages
                errorMessage.style.display = 'none';
                successMessage.style.display = 'none';
                
                // Add loading state
                form.classList.add('loading');
                
                try {
                    const response = await fetch('/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ email, password })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        successMessage.textContent = 'რეგისტრაცია წარმატებით დასრულდა! გადამისამართება...';
                        successMessage.style.display = 'block';
                        setTimeout(() => {
                            window.location.href = '/';
                        }, 1500);
                    } else {
                        errorMessage.textContent = data.error;
                        errorMessage.style.display = 'block';
                    }
                } catch (error) {
                    errorMessage.textContent = 'დაფიქსირებულია შეცდომა. გთხოვთ სცადოთ თავიდან.';
                    errorMessage.style.display = 'block';
                } finally {
                    form.classList.remove('loading');
                }
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(register_html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        user = verify_user(email, password)
        if not user:
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 400
        
        # Log user in
        session['user_email'] = email
        
        return jsonify({'success': True, 'message': 'Login successful'})
    
    # GET request - show login form
    login_html = '''
    <!DOCTYPE html>
    <html lang="ka">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>შესვლა - ჩიკორი</title>
        <link rel="stylesheet" href="style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />
        <style>
            .auth-page {
                min-height: 100vh;
                background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .auth-container {
                background: var(--white);
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                width: 100%;
                max-width: 450px;
                position: relative;
            }
            .auth-header {
                background: var(--primary-color);
                color: var(--white);
                padding: 2rem;
                text-align: center;
            }
            .auth-header h1 {
                font-size: 1.75rem;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }
            .auth-header p {
                opacity: 0.9;
                font-size: 0.9rem;
            }
            .auth-body {
                padding: 2rem;
            }
            .auth-form {
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
            }
            .form-group {
                position: relative;
            }
            .form-group label {
                display: block;
                margin-bottom: 0.5rem;
                font-weight: 500;
                color: var(--text-color);
                font-size: 0.9rem;
            }
            .form-group input {
                width: 100%;
                padding: 0.875rem 1rem;
                border: 2px solid var(--border-color);
                border-radius: var(--border-radius);
                font-size: 1rem;
                transition: border-color 0.3s ease;
                background: var(--white);
            }
            .form-group input:focus {
                outline: none;
                border-color: var(--accent-color);
            }
            .form-group input::placeholder {
                color: #999;
            }
            .submit-btn {
                background: var(--primary-color);
                color: var(--white);
                border: none;
                padding: 1rem;
                border-radius: var(--border-radius);
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.2s ease;
                margin-top: 0.5rem;
            }
            .submit-btn:hover {
                background: var(--secondary-color);
                transform: translateY(-1px);
            }
            .submit-btn:active {
                transform: translateY(0);
            }
            .auth-links {
                text-align: center;
                margin-top: 1.5rem;
                padding-top: 1.5rem;
                border-top: 1px solid var(--border-color);
            }
            .auth-links a {
                color: var(--accent-color);
                text-decoration: none;
                font-weight: 500;
                transition: color 0.3s ease;
            }
            .auth-links a:hover {
                color: var(--secondary-color);
                text-decoration: underline;
            }
            .error-message {
                background: #fee;
                color: #c33;
                padding: 0.75rem;
                border-radius: var(--border-radius);
                text-align: center;
                font-size: 0.9rem;
                border: 1px solid #fcc;
                margin-top: 1rem;
                display: none;
            }
            .success-message {
                background: #efe;
                color: #363;
                padding: 0.75rem;
                border-radius: var(--border-radius);
                text-align: center;
                font-size: 0.9rem;
                border: 1px solid #cfc;
                margin-top: 1rem;
                display: none;
            }
            .back-home {
                position: absolute;
                top: 1rem;
                left: 1rem;
                color: var(--white);
                text-decoration: none;
                font-size: 0.9rem;
                opacity: 0.8;
                transition: opacity 0.3s ease;
            }
            .back-home:hover {
                opacity: 1;
            }
            .back-home i {
                margin-right: 0.5rem;
            }
            .loading {
                opacity: 0.7;
                pointer-events: none;
            }
            .loading .submit-btn {
                position: relative;
            }
            .loading .submit-btn::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 20px;
                height: 20px;
                margin: -10px 0 0 -10px;
                border: 2px solid transparent;
                border-top: 2px solid var(--white);
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="auth-page">
            <div class="auth-container">
                <a href="/" class="back-home">
                    <i class="fas fa-arrow-left"></i>
                    მთავარი გვერდი
                </a>
                <div class="auth-header">
                    <h1>კეთილი იყოს თქვენი მობრძანება</h1>
                    <p>შედით თქვენს ანგარიშში</p>
                </div>
                <div class="auth-body">
                    <form class="auth-form" id="loginForm">
                        <div class="form-group">
                            <label for="email">ელ-ფოსტა</label>
                            <input type="email" id="email" placeholder="შეიყვანეთ თქვენი ელ-ფოსტა" required>
                        </div>
                        <div class="form-group">
                            <label for="password">პაროლი</label>
                            <input type="password" id="password" placeholder="შეიყვანეთ თქვენი პაროლი" required>
                        </div>
                        <button type="submit" class="submit-btn">
                            <span>შესვლა</span>
                        </button>
                    </form>
                    <div class="auth-links">
                        <a href="/register">არ გაქვთ ანგარიში? <strong>დარეგისტრირდით</strong></a>
                    </div>
                    <div id="errorMessage" class="error-message"></div>
                    <div id="successMessage" class="success-message"></div>
                </div>
            </div>
        </div>
        
        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const form = document.getElementById('loginForm');
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                const errorMessage = document.getElementById('errorMessage');
                const successMessage = document.getElementById('successMessage');
                
                // Hide previous messages
                errorMessage.style.display = 'none';
                successMessage.style.display = 'none';
                
                // Add loading state
                form.classList.add('loading');
                
                try {
                    const response = await fetch('/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ email, password })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        successMessage.textContent = 'წარმატებით შეხვედით! გადამისამართება...';
                        successMessage.style.display = 'block';
                        setTimeout(() => {
                            window.location.href = '/';
                        }, 1500);
                    } else {
                        errorMessage.textContent = data.error;
                        errorMessage.style.display = 'block';
                    }
                } catch (error) {
                    errorMessage.textContent = 'დაფიქსირებულია შეცდომა. გთხოვთ სცადოთ თავიდან.';
                    errorMessage.style.display = 'block';
                } finally {
                    form.classList.remove('loading');
                }
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(login_html)

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect('/')

@app.route('/api/user-status')
def user_status():
    """Check if user is logged in"""
    user_email = session.get('user_email')
    return jsonify({
        'logged_in': user_email is not None,
        'email': user_email
    })

@app.route('/terms')
def terms():
    return send_from_directory('.', 'terms.html')

# Serve static files (css, js, images, etc.) - This should be LAST
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)

def get_product_by_id(product_id):
    """Get product details by ID"""
    products = {
        'table': {
            'id': 'table',
            'name': 'კარადა',
            'price': 250
        },
        'bed': {
            'id': 'bed',
            'name': 'საწოლი',
            'price': 650
        },
        'sofa': {
            'id': 'sofa',
            'name': 'სამზარეულოს კუთხე',
            'price': 650
        },
        'desk': {
            'id': 'desk',
            'name': 'სამუშაო მაგიდა',
            'price': 400
        }
    }
    return products.get(product_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
