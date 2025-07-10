import requests
import time
from config.settings import TBC_ECOMMERCE_CONFIG
from app.models.product import get_product_by_id

def get_tbc_ecommerce_access_token():
    """Get TBC E-Commerce access token for API authentication"""
    try:
        print("=== TBC E-COMMERCE ACCESS TOKEN REQUEST ===")
        
        # Prepare access token request
        token_url = f"{TBC_ECOMMERCE_CONFIG['base_url']}{TBC_ECOMMERCE_CONFIG['oauth_url']}"
        
        # Access token credentials should be sent as form data
        token_data = {
            'client_Id': TBC_ECOMMERCE_CONFIG['client_id'],
            'client_secret': TBC_ECOMMERCE_CONFIG['client_secret']
        }
        
        print(f"Token URL: {token_url}")
        print(f"Client ID: {TBC_ECOMMERCE_CONFIG['client_id']}")
        print(f"Client Secret: {TBC_ECOMMERCE_CONFIG['client_secret'][:10]}...")
        
        # Make access token request
        response = requests.post(
            token_url,
            data=token_data,
            headers={
                'Accept': 'application/json',
                'apikey': TBC_ECOMMERCE_CONFIG['api_key'],
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            timeout=30
        )
        
        print(f"Token Response Status: {response.status_code}")
        print(f"Token Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            print(f"Access Token: {access_token[:20]}...")
            return access_token
        else:
            print(f"Token request failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error getting TBC E-Commerce access token: {str(e)}")
        return None

def create_tbc_ecommerce_payment(product_id, amount, user_ip_address=None):
    """Create TBC E-Commerce payment using method 4 (installment)"""
    try:
        print("=== TBC E-COMMERCE PAYMENT REQUEST ===")
        
        # Get access token first (required for Bearer authentication)
        access_token = get_tbc_ecommerce_access_token()
        if not access_token:
            return {
                'success': False,
                'error': 'Failed to get TBC E-Commerce access token - credentials may not be configured or are invalid'
            }
        
        # Get product details
        product = get_product_by_id(product_id)
        if not product:
            return {
                'success': False,
                'error': 'Product not found'
            }
        
        # Generate unique payment ID
        merchant_payment_id = f"payment_{product_id}_{int(time.time())}"
        
        # Prepare payment request according to TBC E-Commerce API documentation
        payment_url = f"{TBC_ECOMMERCE_CONFIG['base_url']}{TBC_ECOMMERCE_CONFIG['payment_url']}"
        
        payment_data = {
            "amount": {
                "currency": "GEL",
                "total": float(amount),
                "subTotal": float(amount),
                "tax": 0,
                "shipping": 0
            },
            "extra": merchant_payment_id,
            "userIpAddress": user_ip_address or '127.0.0.1',
            "expirationMinutes": "12",
            "methods": [4],  # Method 4 for installment payments
            "installmentProducts": [
                {
                    "Name": product['name'],
                    "Price": float(amount),
                    "Quantity": 1
                }
            ],
            "preAuth": False,
            "language": "KA",
            "merchantPaymentId": merchant_payment_id,
            "saveCard": False
        }
        
        print(f"Payment URL: {payment_url}")
        print(f"Payment Data: {payment_data}")
        
        # Make payment request with Bearer token authentication
        response = requests.post(
            payment_url,
            json=payment_data,
            headers={
                'Content-Type': 'application/json',
                'apikey': TBC_ECOMMERCE_CONFIG['api_key'],
                'Authorization': f'Bearer {access_token}'
            },
            timeout=30
        )
        
        print(f"Payment Response Status: {response.status_code}")
        print(f"Payment Response Headers: {dict(response.headers)}")
        print(f"Payment Response: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            pay_id = response_data.get('payId')
            approval_url = None
            
            # Extract approval URL from links
            links = response_data.get('links', [])
            for link in links:
                if link.get('rel') == 'approval_url':
                    approval_url = link.get('uri')
                    break
            
            if pay_id and approval_url:
                print(f"Payment ID: {pay_id}")
                print(f"Approval URL: {approval_url}")
                
                return {
                    'success': True,
                    'pay_id': pay_id,
                    'approval_url': approval_url,
                    'merchant_payment_id': merchant_payment_id,
                    'debug_info': {
                        'request': payment_data,
                        'response': response_data,
                        'headers': dict(response.headers)
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'Missing payment ID or approval URL in response',
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
                'error': f'TBC E-Commerce API error: {error_message}',
                'status_code': response.status_code,
                'response': response.text
            }
            
    except Exception as e:
        print(f"Error creating TBC E-Commerce payment: {str(e)}")
        return {
            'success': False,
            'error': f'Exception: {str(e)}'
        } 