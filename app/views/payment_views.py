from flask import request, jsonify, redirect, url_for, send_from_directory
import hashlib
from config.settings import FLITT_CONFIG, EMAIL_CONFIG
from app.services.flitt_service import create_flitt_payment
from app.services.tbc_installment_service import create_tbc_installment_application
from app.services.tbc_ecommerce_service import create_tbc_ecommerce_payment
from app.services.payment_router import payment_router
from app.models.product import get_all_products
from config.products import get_payment_methods, get_price_ranges
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def init_payment_routes(app):
    """Initialize payment-related routes"""
    
    @app.route('/')
    def home():
        return send_from_directory('app/templates', 'index.html')

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
            
            # Use the service to create payment
            result = create_flitt_payment(product_id, amount)
            
            if result['success']:
                return jsonify(result)
            else:
                return jsonify(result), 400
                
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
        """Handle TBC installment callback"""
        try:
            print("=== TBC INSTALLMENT CALLBACK ===")
            print(f"Request Method: {request.method}")
            print(f"Request URL: {request.url}")
            print(f"Request Args: {dict(request.args)}")
            print(f"Request Form: {dict(request.form)}")
            print(f"Request JSON: {request.get_json() if request.is_json else 'Not JSON'}")
            
            # Extract callback data
            session_id = request.args.get('sessionId') or request.form.get('sessionId')
            status = request.args.get('status') or request.form.get('status')
            
            print(f"Session ID: {session_id}")
            print(f"Status: {status}")
            
            # Process the callback
            print(f"TBC installment callback processed: Session {session_id}, Status: {status}")
            # Here you would typically update your DB, send emails, etc.
            
            return jsonify({'status': 'ok'})
        except Exception as e:
            print(f"TBC installment callback error: {str(e)}")
            return jsonify({'error': str(e)}), 500

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
            
            # Create installment application using service
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

    @app.route('/api/tbc-ecommerce-payment', methods=['POST'])
    def tbc_ecommerce_payment():
        """Handle TBC E-Commerce payment"""
        try:
            print("=== TBC E-COMMERCE PAYMENT REQUEST ===")
            print(f"Request Method: {request.method}")
            print(f"Request URL: {request.url}")
            print(f"Request Headers: {dict(request.headers)}")
            
            data = request.get_json()
            print(f"Request Body: {data}")
            
            product_id = data.get('product_id')
            amount = data.get('amount')
            user_ip_address = request.remote_addr
            
            if not product_id or not amount:
                return jsonify({
                    'success': False,
                    'error': 'Product ID and amount are required'
                }), 400
            
            # Create E-Commerce payment using service
            result = create_tbc_ecommerce_payment(product_id, amount, user_ip_address)
            
            if result['success']:
                return jsonify(result)
            else:
                return jsonify(result), 400
                
        except Exception as e:
            print(f"TBC E-Commerce payment error: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Server error: {str(e)}'
            }), 500

    @app.route('/tbc-ecommerce-callback', methods=['POST'])
    def tbc_ecommerce_callback():
        """Handle TBC E-Commerce callback"""
        try:
            print("=== TBC E-COMMERCE CALLBACK ===")
            print(f"Request Method: {request.method}")
            print(f"Request URL: {request.url}")
            print(f"Request Headers: {dict(request.headers)}")
            print(f"Request JSON: {request.get_json()}")
            
            # Extract callback data
            data = request.get_json()
            payment_id = data.get('paymentId')
            status = data.get('status')
            
            print(f"Payment ID: {payment_id}")
            print(f"Status: {status}")
            
            # Process the callback
            print(f"TBC E-Commerce callback processed: Payment {payment_id}, Status: {status}")
            # Here you would typically update your DB, send emails, etc.
            
            return jsonify({'status': 'ok'})
        except Exception as e:
            print(f"TBC E-Commerce callback error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/terms')
    def terms():
        return send_from_directory('app/templates', 'terms.html')

    @app.route('/api/products')
    def api_products():
        return jsonify(get_all_products())

    @app.route('/api/dynamic-payment', methods=['POST'])
    def dynamic_payment():
        """Dynamic payment endpoint that routes to appropriate service"""
        try:
            data = request.get_json()
            method_type = data.get('method_type')  # 'later', 'installment', 'card'
            option_key = data.get('option_key')    # 'tbc_card', 'bog_installment', etc.
            product_id = data.get('product_id')
            amount = data.get('amount')
            user_ip_address = request.remote_addr
            
            if not all([method_type, option_key, product_id, amount]):
                return jsonify({
                    'success': False,
                    'error': 'Missing required parameters: method_type, option_key, product_id, amount'
                }), 400
            
            # Route payment to appropriate service
            result = payment_router.route_payment(
                method_type=method_type,
                option_key=option_key,
                product_id=product_id,
                amount=amount,
                user_ip_address=user_ip_address
            )
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Payment processing error: {str(e)}'
            }), 500

    @app.route('/api/payment-methods', methods=['GET'])
    def get_payment_methods_api():
        """Get available payment methods configuration"""
        try:
            methods = get_payment_methods()
            return jsonify({
                'success': True,
                'payment_methods': methods
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error fetching payment methods: {str(e)}'
            }), 500

    @app.route('/api/price-ranges', methods=['GET'])
    def get_price_ranges_api():
        """Get dynamic price ranges for filtering"""
        try:
            ranges = get_price_ranges()
            return jsonify({
                'success': True,
                'price_ranges': ranges
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error fetching price ranges: {str(e)}'
            }), 500

    @app.route('/api/send-order-email', methods=['POST'])
    def send_order_email():
        """Receive order info and send an email to the operator"""
        try:
            data = request.get_json()
            name = data.get('name')
            phone = data.get('phone')
            order_time = data.get('order_time')
            product_id = data.get('product_id')
            product_name = data.get('product_name')
            product_price = data.get('product_price')
            payment_method = data.get('payment_method')
            payment_option = data.get('payment_option')
            payment_option_name = data.get('payment_option_name')

            # Compose email using configuration
            from_email = EMAIL_CONFIG['from_email']
            to_email = EMAIL_CONFIG['to_email']
            app_password = EMAIL_CONFIG['app_password']

            subject = f'ახალი შეკვეთა საიტიდან - {order_time}'
            body = f'''
შეკვეთის დრო: {order_time}
სახელი და გვარი: {name or ''}
ტელეფონი: {phone}
პროდუქტი: {product_name} (ID: {product_id})
ფასი: {product_price} ლარი
გადახდის მეთოდი: {payment_method} ({payment_option_name})
'''
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Send email via Gmail SMTP
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(from_email, app_password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()

            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    # Serve static files (css, js, images, etc.) - This should be LAST
    @app.route('/<path:path>')
    def static_proxy(path):
        return send_from_directory('app/templates', path) 