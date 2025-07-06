import hashlib

def generate_signature(order_data, secret_key):
    """Generate signature for Flitt API request (SHA1, Flitt format)"""
    # Format: secret_key|amount|currency|merchant_id|order_desc|order_id|server_callback_url
    signature_string = f"{secret_key}|{order_data['amount']}|{order_data['currency']}|{order_data['merchant_id']}|{order_data['order_desc']}|{order_data['order_id']}|{order_data['server_callback_url']}"
    signature = hashlib.sha1(signature_string.encode('utf-8')).hexdigest()
    print(f"Signature generation:")
    print(f"  String: {signature_string}")
    print(f"  Signature: {signature}")
    return signature 