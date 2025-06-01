from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def home():
    with open('index.html', 'r') as f:
        html = f.read()
    return render_template_string(html)

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Use PORT env variable if set, else 8080
    app.run(debug=True, host='0.0.0.0', port=port)  # Bind to all interfaces for deployment
