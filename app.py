from flask import Flask, render_template, request, send_file
from generate_signature import generate_email_signature, normalize_name
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    title = request.form['title']
    email = request.form['email']
    phone = request.form['phone']
    avatar_url = request.form['avatar_url']

    signature = generate_email_signature(firstname, lastname, title, email, phone, avatar_url)

    folder = "html_signatures"
    os.makedirs(folder, exist_ok=True)

    normalized_firstname = normalize_name(firstname)
    normalized_lastname = normalize_name(lastname)
    filename = f"{normalized_firstname}_{normalized_lastname}.html"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as file:
        file.write(signature)

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
from generate_signature import generate_email_signature, convert_drive_link_to_direct_url

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    return jsonify({'signature': signature})

if __name__ == '__main__':
    app.run(debug=True)
