from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from generate_signature import generate_email_signature, normalize_name
import os
import markdown
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Sample blog posts
blog_posts = [
    {
        'id': 1,
        'title': 'The Importance of Professional Email Signatures',
        'content': 'content/blog_post_1.md',
        'date': datetime(2023, 7, 1),
        'author': 'John Doe',
        'cover_image': 'https://images.unsplash.com/photo-1596526131083-e8c633c948d2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
    },
    {
        'id': 2,
        'title': 'How to Design an Effective HTML Email Signature',
        'content': 'content/blog_post_2.md',
        'date': datetime(2023, 7, 15),
        'author': 'Jane Smith',
        'cover_image': 'https://images.unsplash.com/photo-1555421689-d68471e189f2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
    },
    {
        'id': 3,
        'title': 'Top 5 Email Signature Generators in 2023',
        'content': 'content/blog_post_3.md',
        'date': datetime(2023, 8, 1),
        'author': 'Mike Johnson',
        'cover_image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
    }
]

TEMPLATES = {
    'default': 'templates/template.html',
    'minimalist': 'templates/template_minimalist.html',
    'colorful': 'templates/template_colorful.html',
    'modern': 'templates/template_modern.html',
    'creative': 'templates/template_creative.html',
    'corporate': 'templates/template_corporate.html'
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

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=blog_posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post:
        with open(post['content'], 'r') as file:
            content = markdown.markdown(file.read())
        return render_template('blog_post.html', post=post, content=content)
    return 'Post not found', 404

if __name__ == '__main__':
    app.run(debug=True)
