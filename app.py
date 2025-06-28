from flask import Flask, send_from_directory, request, jsonify, redirect, url_for
import os
import time
from config import FLITT_CONFIG

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import Flitt SDK
from cloudipsp import Api, Checkout

app = Flask(__name__, static_folder='.', static_url_path='')

# Initialize Flitt API
flitt_api = Api(
    merchant_id=int(FLITT_CONFIG['merchant_id']),
    secret_key=FLITT_CONFIG['secret_key']
)
flitt_checkout = Checkout(api=flitt_api)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Serve static files (css, js, images, etc.)
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)

@app.route('/api/create-payment', methods=['POST'])
def create_payment():
    """Create a payment order and redirect to Flitt using official SDK"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        amount = data.get('amount')
        
        # Get product details
        product = get_product_by_id(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Create order data for Flitt using official SDK
        order_data = {
            'currency': FLITT_CONFIG['currency'],
            'amount': int(amount * 100),  # Convert to cents
            'order_id': f"order_{product_id}_{int(time.time())}",
            'order_desc': f"შეძენა: {product['name']}",
            'response_url': request.host_url.rstrip('/') + '/payment-result',
            'server_callback_url': request.host_url.rstrip('/') + '/payment-callback',
            'lang': FLITT_CONFIG['lang']
        }
        
        # Add optional fields if available
        if FLITT_CONFIG.get('sender_email'):
            order_data['sender_email'] = FLITT_CONFIG['sender_email']
        if FLITT_CONFIG.get('sender_phone'):
            order_data['sender_phone'] = FLITT_CONFIG['sender_phone']
        
        print(f"Creating payment with Flitt SDK...")
        print(f"Merchant ID: {FLITT_CONFIG['merchant_id']}")
        print(f"Test Mode: {FLITT_CONFIG['test_mode']}")
        print(f"Order data: {order_data}")
        
        # Use official Flitt SDK to create checkout URL
        response = flitt_checkout.url(order_data)
        
        print(f"Flitt SDK response: {response}")
        
        if response.get('response_status') == 'success':
            return jsonify({
                'success': True,
                'checkout_url': response['checkout_url']
            })
        else:
            error_message = response.get('error_message', 'Unknown error')
            error_code = response.get('error_code', 'Unknown')
            
            return jsonify({
                'error': f"Flitt API error: {error_message} (Code: {error_code})",
                'details': response
            }), 400
            
    except Exception as e:
        print(f"Exception in create_payment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/payment-result')
def payment_result():
    """Handle payment result redirect from Flitt"""
    status = request.args.get('response_status')
    
    if status == 'success':
        return redirect(url_for('home', status='success'))
    else:
        return redirect(url_for('home', status='failure'))

@app.route('/payment-callback', methods=['POST'])
def payment_callback():
    """Handle server callback from Flitt using official SDK"""
    try:
        data = request.get_json()
        
        # Verify signature using Flitt SDK
        if not flitt_api.verify_signature(data):
            return jsonify({'error': 'Invalid signature'}), 400
        
        # Process the callback
        order_id = data.get('order_id')
        status = data.get('response_status')
        amount = data.get('amount')
        
        # Here you would typically:
        # 1. Update your database with payment status
        # 2. Send confirmation emails
        # 3. Update inventory
        # 4. Log the transaction
        
        print(f"Payment callback received: Order {order_id}, Status: {status}, Amount: {amount}")
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
