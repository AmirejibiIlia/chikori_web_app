from flask import Flask, send_from_directory
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
from config.settings import IS_PRODUCTION, FLASK_SECRET_KEY

# Import route handlers
from app.views.payment_views import init_payment_routes
from app.views.auth_views import init_auth_routes
from app.views.tbc_views import init_tbc_routes

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, static_folder='app/static', static_url_path='/static')
    
    # Set Flask environment and secret key for sessions
    if IS_PRODUCTION:
        app.config['ENV'] = 'production'
        app.config['DEBUG'] = False
    else:
        app.config['ENV'] = 'development'
        app.config['DEBUG'] = True

    # Secret key for sessions (you should set this in environment variables for production)
    app.secret_key = os.environ.get('SECRET_KEY', FLASK_SECRET_KEY)
    
    # Initialize routes
    init_payment_routes(app)
    init_auth_routes(app)
    init_tbc_routes(app)
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000) 