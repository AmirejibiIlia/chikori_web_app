import json
import hashlib

def load_users():
    """Load users from JSON file"""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": []}

def save_users(users_data):
    """Save users to JSON file"""
    with open('users.json', 'w') as f:
        json.dump(users_data, f, indent=2)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_user_exists(email):
    """Check if user already exists"""
    users_data = load_users()
    return any(user['email'] == email for user in users_data['users'])

def verify_user(email, password):
    """Verify user credentials"""
    users_data = load_users()
    hashed_password = hash_password(password)
    for user in users_data['users']:
        if user['email'] == email and user['password'] == hashed_password:
            return user
    return None 