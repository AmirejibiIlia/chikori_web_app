import requests
import time
from config.settings import FLITT_CONFIG
from app.models.product import get_product_by_id
from app.utils.signature import generate_signature

def create_flitt_payment(product_id, amount):
    """Create a payment order using direct Flitt API call"""
    try:
        # Log incoming request details
        print("=== INCOMING PAYMENT REQUEST ===")
        print(f"Product ID: {product_id}")
        print(f"Amount: {amount}")
        
        # Get product details
        product = get_product_by_id(product_id)
        if not product:
            error_response = {'error': 'Product not found', 'product_id': product_id}
            print(f"Product not found: {error_response}")
            return {'success': False, 'error': 'Product not found', 'product_id': product_id}
        
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
            'server_callback_url': FLITT_CONFIG['base_url'] + '/payment-callback'
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
            return success_response
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
            return error_response
            
    except Exception as e:
        print(f"Exception in create_flitt_payment: {str(e)}")
        return {
            'success': False,
            'error': f'Server error: {str(e)}'
        } 