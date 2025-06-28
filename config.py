import os

FLITT_CONFIG = {
    'merchant_id': os.environ.get('FLITT_MERCHANT_ID', '4054082'),  
    'secret_key': os.environ.get('FLITT_SECRET_KEY', 'APvSrPJZn6TZkqd2mmAv6PfYvDSqBKpI'),  
    'api_domain': os.environ.get('FLITT_API_DOMAIN', 'pay.flitt.com'),
    'currency': os.environ.get('FLITT_CURRENCY', 'GEL'),
    'lang': os.environ.get('FLITT_LANG', 'ka'),
    'test_mode': os.environ.get('FLITT_TEST_MODE', 'false').lower() == 'false',  # Set to 'true' for testing
    'base_url': os.environ.get('https://www.ganvadeba.store/', 'http://localhost:8000'),
    # Optional fields for better payment processing
    'sender_email': os.environ.get('FLITT_SENDER_EMAIL', ''),
    'sender_phone': os.environ.get('FLITT_SENDER_PHONE', '')
}

FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'devsecret')

