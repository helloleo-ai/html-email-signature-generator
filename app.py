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