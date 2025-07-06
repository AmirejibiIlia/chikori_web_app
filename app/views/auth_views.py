from flask import request, jsonify, session, redirect, render_template_string
from datetime import datetime
from app.models.user import load_users, save_users, check_user_exists, verify_user, hash_password

def init_auth_routes(app):
    """Initialize authentication-related routes"""
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'success': False, 'error': 'Email and password are required'}), 400
            
            if check_user_exists(email):
                return jsonify({'success': False, 'error': 'User already exists'}), 400
            
            # Create new user
            users_data = load_users()
            new_user = {
                'email': email,
                'password': hash_password(password),
                'created_at': datetime.now().isoformat()
            }
            users_data['users'].append(new_user)
            save_users(users_data)
            
            # Log user in
            session['user_email'] = email
            
            return jsonify({'success': True, 'message': 'Registration successful'})
        
        # GET request - show registration form
        register_html = '''
        <!DOCTYPE html>
        <html lang="ka">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>რეგისტრაცია - ჩიკორი</title>
            <link rel="stylesheet" href="/static/css/style.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />
            <style>
                .auth-page {
                    min-height: 100vh;
                    background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                .auth-container {
                    background: var(--white);
                    border-radius: 16px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                    width: 100%;
                    max-width: 450px;
                    position: relative;
                }
                .auth-header {
                    background: var(--primary-color);
                    color: var(--white);
                    padding: 2rem;
                    text-align: center;
                }
                .auth-header h1 {
                    font-size: 1.75rem;
                    margin-bottom: 0.5rem;
                    font-weight: 600;
                }
                .auth-header p {
                    opacity: 0.9;
                    font-size: 0.9rem;
                }
                .auth-body {
                    padding: 2rem;
                }
                .auth-form {
                    display: flex;
                    flex-direction: column;
                    gap: 1.5rem;
                }
                .form-group {
                    position: relative;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 0.5rem;
                    font-weight: 500;
                    color: var(--text-color);
                    font-size: 0.9rem;
                }
                .form-group input {
                    width: 100%;
                    padding: 0.875rem 1rem;
                    border: 2px solid var(--border-color);
                    border-radius: var(--border-radius);
                    font-size: 1rem;
                    transition: border-color 0.3s ease;
                    background: var(--white);
                }
                .form-group input:focus {
                    outline: none;
                    border-color: var(--accent-color);
                }
                .form-group input::placeholder {
                    color: #999;
                }
                .submit-btn {
                    background: var(--primary-color);
                    color: var(--white);
                    border: none;
                    padding: 1rem;
                    border-radius: var(--border-radius);
                    font-size: 1rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background-color 0.3s ease, transform 0.2s ease;
                    margin-top: 0.5rem;
                }
                .submit-btn:hover {
                    background: var(--secondary-color);
                    transform: translateY(-1px);
                }
                .submit-btn:active {
                    transform: translateY(0);
                }
                .auth-links {
                    text-align: center;
                    margin-top: 1.5rem;
                    padding-top: 1.5rem;
                    border-top: 1px solid var(--border-color);
                }
                .auth-links a {
                    color: var(--accent-color);
                    text-decoration: none;
                    font-weight: 500;
                    transition: color 0.3s ease;
                }
                .auth-links a:hover {
                    color: var(--secondary-color);
                    text-decoration: underline;
                }
                .error-message {
                    background: #fee;
                    color: #c33;
                    padding: 0.75rem;
                    border-radius: var(--border-radius);
                    text-align: center;
                    font-size: 0.9rem;
                    border: 1px solid #fcc;
                    margin-top: 1rem;
                    display: none;
                }
                .success-message {
                    background: #efe;
                    color: #363;
                    padding: 0.75rem;
                    border-radius: var(--border-radius);
                    text-align: center;
                    font-size: 0.9rem;
                    border: 1px solid #cfc;
                    margin-top: 1rem;
                    display: none;
                }
                .back-home {
                    position: absolute;
                    top: 1rem;
                    left: 1rem;
                    color: var(--white);
                    text-decoration: none;
                    font-size: 0.9rem;
                    opacity: 0.8;
                    transition: opacity 0.3s ease;
                }
                .back-home:hover {
                    opacity: 1;
                }
                .back-home i {
                    margin-right: 0.5rem;
                }
                .loading {
                    opacity: 0.7;
                    pointer-events: none;
                }
                .loading .submit-btn {
                    position: relative;
                }
                .loading .submit-btn::after {
                    content: '';
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 20px;
                    height: 20px;
                    margin: -10px 0 0 -10px;
                    border: 2px solid transparent;
                    border-top: 2px solid var(--white);
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <div class="auth-page">
                <div class="auth-container">
                    <a href="/" class="back-home">
                        <i class="fas fa-arrow-left"></i>
                        მთავარი გვერდი
                    </a>
                    <div class="auth-header">
                        <h1>რეგისტრაცია</h1>
                        <p>შექმენით თქვენი ანგარიში</p>
                    </div>
                    <div class="auth-body">
                        <form class="auth-form" id="registerForm">
                            <div class="form-group">
                                <label for="email">ელ-ფოსტა</label>
                                <input type="email" id="email" placeholder="შეიყვანეთ თქვენი ელ-ფოსტა" required>
                            </div>
                            <div class="form-group">
                                <label for="password">პაროლი</label>
                                <input type="password" id="password" placeholder="შეიყვანეთ პაროლი" required>
                            </div>
                            <button type="submit" class="submit-btn">
                                <span>რეგისტრაცია</span>
                            </button>
                        </form>
                        <div class="auth-links">
                            <a href="/login">უკვე გაქვთ ანგარიში? <strong>შედით</strong></a>
                        </div>
                        <div id="errorMessage" class="error-message"></div>
                        <div id="successMessage" class="success-message"></div>
                    </div>
                </div>
            </div>
            
            <script>
                document.getElementById('registerForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const form = document.getElementById('registerForm');
                    const email = document.getElementById('email').value;
                    const password = document.getElementById('password').value;
                    const errorMessage = document.getElementById('errorMessage');
                    const successMessage = document.getElementById('successMessage');
                    
                    // Hide previous messages
                    errorMessage.style.display = 'none';
                    successMessage.style.display = 'none';
                    
                    // Add loading state
                    form.classList.add('loading');
                    
                    try {
                        const response = await fetch('/register', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ email, password })
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            successMessage.textContent = 'წარმატებით დარეგისტრირდით! გადამისამართება...';
                            successMessage.style.display = 'block';
                            setTimeout(() => {
                                window.location.href = '/';
                            }, 1500);
                        } else {
                            errorMessage.textContent = data.error;
                            errorMessage.style.display = 'block';
                        }
                    } catch (error) {
                        errorMessage.textContent = 'დაფიქსირებულია შეცდომა. გთხოვთ სცადოთ თავიდან.';
                        errorMessage.style.display = 'block';
                    } finally {
                        form.classList.remove('loading');
                    }
                });
            </script>
        </body>
        </html>
        '''
        return render_template_string(register_html)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'success': False, 'error': 'Email and password are required'}), 400
            
            user = verify_user(email, password)
            if not user:
                return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
            
            # Log user in
            session['user_email'] = email
            
            return jsonify({'success': True, 'message': 'Login successful'})
        
        # GET request - show login form
        login_html = '''
        <!DOCTYPE html>
        <html lang="ka">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>შესვლა - ჩიკორი</title>
            <link rel="stylesheet" href="/static/css/style.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />
            <style>
                .auth-page {
                    min-height: 100vh;
                    background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                .auth-container {
                    background: var(--white);
                    border-radius: 16px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                    width: 100%;
                    max-width: 450px;
                    position: relative;
                }
                .auth-header {
                    background: var(--primary-color);
                    color: var(--white);
                    padding: 2rem;
                    text-align: center;
                }
                .auth-header h1 {
                    font-size: 1.75rem;
                    margin-bottom: 0.5rem;
                    font-weight: 600;
                }
                .auth-header p {
                    opacity: 0.9;
                    font-size: 0.9rem;
                }
                .auth-body {
                    padding: 2rem;
                }
                .auth-form {
                    display: flex;
                    flex-direction: column;
                    gap: 1.5rem;
                }
                .form-group {
                    position: relative;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 0.5rem;
                    font-weight: 500;
                    color: var(--text-color);
                    font-size: 0.9rem;
                }
                .form-group input {
                    width: 100%;
                    padding: 0.875rem 1rem;
                    border: 2px solid var(--border-color);
                    border-radius: var(--border-radius);
                    font-size: 1rem;
                    transition: border-color 0.3s ease;
                    background: var(--white);
                }
                .form-group input:focus {
                    outline: none;
                    border-color: var(--accent-color);
                }
                .form-group input::placeholder {
                    color: #999;
                }
                .submit-btn {
                    background: var(--primary-color);
                    color: var(--white);
                    border: none;
                    padding: 1rem;
                    border-radius: var(--border-radius);
                    font-size: 1rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background-color 0.3s ease, transform 0.2s ease;
                    margin-top: 0.5rem;
                }
                .submit-btn:hover {
                    background: var(--secondary-color);
                    transform: translateY(-1px);
                }
                .submit-btn:active {
                    transform: translateY(0);
                }
                .auth-links {
                    text-align: center;
                    margin-top: 1.5rem;
                    padding-top: 1.5rem;
                    border-top: 1px solid var(--border-color);
                }
                .auth-links a {
                    color: var(--accent-color);
                    text-decoration: none;
                    font-weight: 500;
                    transition: color 0.3s ease;
                }
                .auth-links a:hover {
                    color: var(--secondary-color);
                    text-decoration: underline;
                }
                .error-message {
                    background: #fee;
                    color: #c33;
                    padding: 0.75rem;
                    border-radius: var(--border-radius);
                    text-align: center;
                    font-size: 0.9rem;
                    border: 1px solid #fcc;
                    margin-top: 1rem;
                    display: none;
                }
                .success-message {
                    background: #efe;
                    color: #363;
                    padding: 0.75rem;
                    border-radius: var(--border-radius);
                    text-align: center;
                    font-size: 0.9rem;
                    border: 1px solid #cfc;
                    margin-top: 1rem;
                    display: none;
                }
                .back-home {
                    position: absolute;
                    top: 1rem;
                    left: 1rem;
                    color: var(--white);
                    text-decoration: none;
                    font-size: 0.9rem;
                    opacity: 0.8;
                    transition: opacity 0.3s ease;
                }
                .back-home:hover {
                    opacity: 1;
                }
                .back-home i {
                    margin-right: 0.5rem;
                }
                .loading {
                    opacity: 0.7;
                    pointer-events: none;
                }
                .loading .submit-btn {
                    position: relative;
                }
                .loading .submit-btn::after {
                    content: '';
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 20px;
                    height: 20px;
                    margin: -10px 0 0 -10px;
                    border: 2px solid transparent;
                    border-top: 2px solid var(--white);
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <div class="auth-page">
                <div class="auth-container">
                    <a href="/" class="back-home">
                        <i class="fas fa-arrow-left"></i>
                        მთავარი გვერდი
                    </a>
                    <div class="auth-header">
                        <h1>კეთილი იყოს თქვენი მობრძანება</h1>
                        <p>შედით თქვენს ანგარიშში</p>
                    </div>
                    <div class="auth-body">
                        <form class="auth-form" id="loginForm">
                            <div class="form-group">
                                <label for="email">ელ-ფოსტა</label>
                                <input type="email" id="email" placeholder="შეიყვანეთ თქვენი ელ-ფოსტა" required>
                            </div>
                            <div class="form-group">
                                <label for="password">პაროლი</label>
                                <input type="password" id="password" placeholder="შეიყვანეთ თქვენი პაროლი" required>
                            </div>
                            <button type="submit" class="submit-btn">
                                <span>შესვლა</span>
                            </button>
                        </form>
                        <div class="auth-links">
                            <a href="/register">არ გაქვთ ანგარიში? <strong>დარეგისტრირდით</strong></a>
                        </div>
                        <div id="errorMessage" class="error-message"></div>
                        <div id="successMessage" class="success-message"></div>
                    </div>
                </div>
            </div>
            
            <script>
                document.getElementById('loginForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const form = document.getElementById('loginForm');
                    const email = document.getElementById('email').value;
                    const password = document.getElementById('password').value;
                    const errorMessage = document.getElementById('errorMessage');
                    const successMessage = document.getElementById('successMessage');
                    
                    // Hide previous messages
                    errorMessage.style.display = 'none';
                    successMessage.style.display = 'none';
                    
                    // Add loading state
                    form.classList.add('loading');
                    
                    try {
                        const response = await fetch('/login', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ email, password })
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            successMessage.textContent = 'წარმატებით შეხვედით! გადამისამართება...';
                            successMessage.style.display = 'block';
                            setTimeout(() => {
                                window.location.href = '/';
                            }, 1500);
                        } else {
                            errorMessage.textContent = data.error;
                            errorMessage.style.display = 'block';
                        }
                    } catch (error) {
                        errorMessage.textContent = 'დაფიქსირებულია შეცდომა. გთხოვთ სცადოთ თავიდან.';
                        errorMessage.style.display = 'block';
                    } finally {
                        form.classList.remove('loading');
                    }
                });
            </script>
        </body>
        </html>
        '''
        return render_template_string(login_html)

    @app.route('/logout')
    def logout():
        session.pop('user_email', None)
        return redirect('/')

    @app.route('/api/user-status')
    def user_status():
        """Check if user is logged in"""
        user_email = session.get('user_email')
        return jsonify({
            'logged_in': user_email is not None,
            'email': user_email
        }) 