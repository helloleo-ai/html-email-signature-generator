import re
import os

def convert_drive_link_to_direct_url(drive_link):
    file_id_match = re.search(r'd/([a-zA-Z0-9_-]+)', drive_link)
    if file_id_match:
        file_id = file_id_match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    else:
        return drive_link

def normalize_name(name):
    return re.sub(r'\W+', '_', name).lower()

def generate_email_signature(firstname, lastname, title, email, phone, avatar_url, template_path='template.html'):
    with open(template_path, 'r') as file:
        template = file.read()
    
    avatar_direct_url = convert_drive_link_to_direct_url(avatar_url) if avatar_url else ''
    
    replacements = {
        '{{firstname}}': firstname,
        '{{lastname}}': lastname,
        '{{title}}': title,
        '{{email}}': email,
        '{{phone}}': phone,
        '{{avatar_url}}': avatar_direct_url
    }
    
    for placeholder, value in replacements.items():
        if value:
            template = template.replace(placeholder, value)
        else:
            # Remove the entire line if the value is empty
            template = re.sub(r'.*' + re.escape(placeholder) + r'.*\n?', '', template)
    
    return template

# The main() function and other input processing functions have been removed
# as they are not needed for the web application.
