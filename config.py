import os

FLITT_CONFIG = {
    'merchant_id': os.environ.get('FLITT_MERCHANT_ID', 'YOUR_MERCHANT_ID_HERE'),  # ← Set in environment variables
    'secret_key': os.environ.get('FLITT_SECRET_KEY', 'YOUR_SECRET_KEY_HERE'),      # ← Set in environment variables
    'api_domain': os.environ.get('FLITT_API_DOMAIN', 'pay.flitt.com'),
    'currency': os.environ.get('FLITT_CURRENCY', 'GEL'),
    'lang': os.environ.get('FLITT_LANG', 'ka'),
    'test_mode': os.environ.get('FLITT_TEST_MODE', 'false').lower() == 'true',  # Set to 'true' for testing
    'base_url': os.environ.get('FLITT_BASE_URL', 'http://localhost:8000'),  # ← Set your domain here
    # Optional fields for better payment processing
    'sender_email': os.environ.get('FLITT_SENDER_EMAIL', ''),
    'sender_phone': os.environ.get('FLITT_SENDER_PHONE', '')
}

FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'devsecret')

# ========================================
# 🔑 SECURITY WARNING:
# ========================================
# NEVER commit real credentials to git!
# Set these environment variables on your server:
# - FLITT_MERCHANT_ID=your_real_merchant_id
# - FLITT_SECRET_KEY=your_real_secret_key
# - FLITT_BASE_URL=https://www.ganvadeba.store
# - FLITT_TEST_MODE=false (for production)

