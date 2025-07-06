from flask import request, jsonify
import requests
from config.settings import TBC_CONFIG, FLITT_CONFIG, TBC_ECOMMERCE_CONFIG
from app.services.tbc_installment_service import get_tbc_access_token

def init_tbc_routes(app):
    """Initialize TBC-specific routes"""
    
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

    @app.route('/api/check-env')
    def check_env():
        """Check environment configuration"""
        try:
            print("=== ENVIRONMENT CHECK ===")
            
            env_info = {
                'flitt_config': {
                    'merchant_id': FLITT_CONFIG['merchant_id'],
                    'test_mode': FLITT_CONFIG['test_mode'],
                    'base_url': FLITT_CONFIG['base_url'],
                    'currency': FLITT_CONFIG['currency']
                },
                'tbc_config': {
                    'test_mode': TBC_CONFIG['test_mode'],
                    'base_url': TBC_CONFIG['base_url'],
                    'campaign_id': TBC_CONFIG['campaign_id']
                },
                'tbc_ecommerce_config': {
                    'test_mode': TBC_ECOMMERCE_CONFIG['test_mode'],
                    'base_url': TBC_ECOMMERCE_CONFIG['base_url']
                }
            }
            
            print(f"Environment info: {env_info}")
            
            return jsonify({
                'success': True,
                'environment': env_info
            })
            
        except Exception as e:
            print(f"Environment check error: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Server error: {str(e)}'
            }), 500 