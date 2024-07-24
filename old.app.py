from flask import Flask, render_template, request, jsonify
from generate_signature import generate_email_signature, convert_drive_link_to_direct_url

app = Flask(__name__)

@app.route('/')
# Code for: def index():

@app.route('/generate_signature', methods=['POST'])
# Code for: def generate_signature():

if __name__ == '__main__':
    app.run(debug=True)