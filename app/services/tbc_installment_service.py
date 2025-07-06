import requests
import time
from config.settings import TBC_CONFIG
from app.models.product import get_product_by_id

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