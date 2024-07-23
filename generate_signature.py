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
    
    avatar_direct_url = convert_drive_link_to_direct_url(avatar_url)
    
    html_template = template.replace('{{firstname}}', firstname)\
                            .replace('{{lastname}}', lastname)\
                            .replace('{{title}}', title)\
                            .replace('{{email}}', email)\
                            .replace('{{phone}}', phone)\
                            .replace('{{avatar_url}}', avatar_direct_url)
    return html_template

# The main() function and other input processing functions have been removed
# as they are not needed for the web application.
