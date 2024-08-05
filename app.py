from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from generate_signature import generate_email_signature, normalize_name
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

TEMPLATES = {
    'default': 'template.html',
    'minimalist': 'template_minimalist.html',
    'colorful': 'template_colorful.html',
    'modern': 'template_modern.html',
    'creative': 'template_creative.html',
    'corporate': 'template_corporate.html'
}

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
    template = data['template']
    primary_color = data.get('primary_color', '#4a90e2')
    secondary_color = data.get('secondary_color', '#333333')
    font_style = data.get('font_style', 'Arial, sans-serif')
    layout = data.get('layout', 'horizontal')
    linkedin = data.get('linkedin', False)
    twitter = data.get('twitter', False)
    include_qr_code = data.get('include_qr_code', False)
    signature_size = data.get('signature_size', '100')
    logo_url = data.get('logo_url', '')

    template_path = TEMPLATES.get(template, 'template.html')
    signature = generate_email_signature(
        firstname, lastname, title, email, phone, avatar_url,
        template_path=template_path, primary_color=primary_color,
        secondary_color=secondary_color, font_style=font_style,
        layout=layout, linkedin=linkedin, twitter=twitter,
        include_qr_code=include_qr_code, signature_size=signature_size,
        logo_url=logo_url
    )

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
