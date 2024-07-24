from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from generate_signature import generate_email_signature, normalize_name
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate_signature', methods=['POST'])
def generate_signature():
    data = request.json
    firstname = data['firstname']
    lastname = data['lastname']
    title = data['title']
    email = data['email']
    phone = data['phone']
    avatar_url = data['avatar_url']

    signature = generate_email_signature(firstname, lastname, title, email, phone, avatar_url)

    folder = "html_signatures"
    os.makedirs(folder, exist_ok=True)

    normalized_firstname = normalize_name(firstname)
    normalized_lastname = normalize_name(lastname)
    filename = f"{normalized_firstname}_{normalized_lastname}.html"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as file:
        file.write(signature)

    return jsonify({'signature': signature, 'filename': filename})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f"html_signatures/{filename}", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
