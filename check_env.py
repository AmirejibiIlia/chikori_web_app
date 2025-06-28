#!/usr/bin/env python3
"""
Check Environment Variables for Flitt Integration
"""

import os
from config import FLITT_CONFIG

def check_environment():
    """Check if all required environment variables are set"""
    print("🔍 Checking Environment Variables")
    print("=" * 50)
    
    # Check required variables
    required_vars = [
        'FLITT_MERCHANT_ID',
        'FLITT_SECRET_KEY',
        'FLITT_BASE_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {'*' * len(value)} (hidden)")
        else:
            print(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    print("\n📋 Current Configuration:")
    print(f"Merchant ID: {FLITT_CONFIG['merchant_id']}")
    print(f"Secret Key: {'*' * len(FLITT_CONFIG['secret_key'])} (hidden)")
    print(f"Base URL: {FLITT_CONFIG['base_url']}")
    print(f"Test Mode: {FLITT_CONFIG['test_mode']}")
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        print("\n📝 To fix this, set these environment variables on your server:")
        for var in missing_vars:
            print(f"export {var}=your_value_here")
        return False
    else:
        print("\n✅ All required environment variables are set!")
        return True

if __name__ == "__main__":
    check_environment() 