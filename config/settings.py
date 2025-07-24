import os

# Environment detection
IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production' or os.environ.get('ENVIRONMENT') == 'production'

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

# TBC Online Installment Configuration
TBC_CONFIG = {
    'api_key': os.environ.get('TBC_API_KEY', 'YOUR_TBC_API_KEY_HERE'),
    'api_secret': os.environ.get('TBC_API_SECRET', 'YOUR_TBC_API_SECRET_HERE'),
    'merchant_key': os.environ.get('TBC_MERCHANT_KEY', 'YOUR_MERCHANT_KEY_HERE'),
    'base_url': os.environ.get('TBC_BASE_URL', 'https://api.tbcbank.ge'),
    'test_mode': os.environ.get('TBC_TEST_MODE', 'true').lower() == 'true',
    'campaign_id': os.environ.get('TBC_CAMPAIGN_ID', 'YOUR_CAMPAIGN_ID'),
    'oauth_url': '/oauth/token',
    'installment_url': '/v1/online-installments/applications'
}

# TBC E-Commerce Configuration for installment payments
TBC_ECOMMERCE_CONFIG = {
    'api_key': os.environ.get('TBC_ECOMMERCE_API_KEY', 'lXcDL8JJiAN8Vjlu6NW3kNeceOQolwnF'),
    'api_secret': os.environ.get('TBC_ECOMMERCE_API_SECRET', 'YOUR_TBC_ECOMMERCE_SECRET_HERE'),
    'merchant_key': os.environ.get('TBC_ECOMMERCE_MERCHANT_KEY', 'YOUR_TBC_ECOMMERCE_MERCHANT_KEY_HERE'),
    'base_url': os.environ.get('TBC_ECOMMERCE_BASE_URL', 'https://api.tbcbank.ge'),
    'test_mode': os.environ.get('TBC_ECOMMERCE_TEST_MODE', 'true').lower() == 'true',
    'oauth_url': '/v1/tpay/access-token',
    'payment_url': '/v1/tpay/payments',
    'callback_url': os.environ.get('TBC_ECOMMERCE_CALLBACK_URL', 'https://ganvadeba.store/tbc-ecommerce-callback'),
    'merchant_id': os.environ.get('TBC_ECOMMERCE_MERCHANT_ID', 'YOUR_TBC_ECOMMERCE_MERCHANT_ID_HERE'),
    'client_id': os.environ.get('TBC_ECOMMERCE_CLIENT_ID', 'YOUR_TBC_ECOMMERCE_CLIENT_ID_HERE'),
    'client_secret': os.environ.get('TBC_ECOMMERCE_CLIENT_SECRET', 'YOUR_TBC_ECOMMERCE_CLIENT_SECRET_HERE')
}

FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'devsecret')

# Email Configuration for Order Notifications
EMAIL_CONFIG = {
    'from_email': os.environ.get('EMAIL_FROM', 'Ilia.amirejibi.07@gmail.com'),
    'to_email': os.environ.get('EMAIL_TO', 'Ilikoamirejibi@gmail.com'),
    'app_password': os.environ.get('EMAIL_APP_PASSWORD', 'YOUR_EMAIL_APP_PASSWORD_HERE'),
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

# ========================================
# 🔑 SECURITY WARNING:
# ========================================
# NEVER commit real credentials to git!
# 
# For LOCAL DEVELOPMENT:
# 1. Copy env.example to .env
# 2. Fill in your test credentials
# 3. Set FLITT_BASE_URL=http://localhost:8000
# 4. Set FLITT_TEST_MODE=true
# 5. Set TBC_TEST_MODE=true
#
# For PRODUCTION (Render):
# Set these environment variables in Render:
# - FLITT_MERCHANT_ID=your_real_merchant_id
# - FLITT_SECRET_KEY=your_real_secret_key
# - FLITT_BASE_URL=https://www.ganvadeba.store
# - FLITT_TEST_MODE=false
# - TBC_API_KEY=your_real_tbc_api_key
# - TBC_API_SECRET=your_real_tbc_api_secret
# - TBC_MERCHANT_KEY=your_real_merchant_key
# - TBC_TEST_MODE=false
# - TBC_CAMPAIGN_ID=your_production_campaign_id
# - TBC_ECOMMERCE_API_KEY=your_real_tbc_ecommerce_api_key
# - TBC_ECOMMERCE_API_SECRET=your_real_tbc_ecommerce_api_secret
# - TBC_ECOMMERCE_MERCHANT_KEY=your_real_tbc_ecommerce_merchant_key
# - TBC_ECOMMERCE_MERCHANT_ID=your_real_tbc_ecommerce_merchant_id
# - TBC_ECOMMERCE_CLIENT_ID=your_real_tbc_ecommerce_client_id
# - TBC_ECOMMERCE_CLIENT_SECRET=your_real_tbc_ecommerce_client_secret
# - TBC_ECOMMERCE_TEST_MODE=false
# - TBC_ECOMMERCE_CALLBACK_URL=https://ganvadeba.store/tbc-ecommerce-callback
# - EMAIL_FROM=your_gmail_address
# - EMAIL_TO=your_operator_email
# - EMAIL_APP_PASSWORD=your_gmail_app_password

# - FLASK_ENV=production
# - FLASK_SECRET_KEY=your_secure_production_secret

# ========================================
# 🌍 ENVIRONMENT INFO:
# ========================================
print(f"🌍 Environment: {'PRODUCTION' if IS_PRODUCTION else 'DEVELOPMENT'}")
print(f"🔗 Base URL: {FLITT_CONFIG['base_url']}")
print(f"🧪 Test Mode: {FLITT_CONFIG['test_mode']}")
print(f"🏪 Merchant ID: {FLITT_CONFIG['merchant_id']}")
print(f"🏦 TBC Test Mode: {TBC_CONFIG['test_mode']}")
print(f"🏦 TBC Campaign ID: {TBC_CONFIG['campaign_id']}")
print(f"🏦 TBC E-Commerce Test Mode: {TBC_ECOMMERCE_CONFIG['test_mode']}")
print(f"🏦 TBC E-Commerce API Key: {TBC_ECOMMERCE_CONFIG['api_key'][:10]}...") 