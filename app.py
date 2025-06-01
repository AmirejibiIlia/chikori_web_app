from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def home():
    with open('index.html', 'r') as f:
        html = f.read()
    return render_template_string(html)

# optional: handle favicon or other paths if needed
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True)
