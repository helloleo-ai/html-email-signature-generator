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

def generate_email_signature(firstname, lastname, title, email, phone, avatar_url, template_path,
                             primary_color, secondary_color, font_style, layout, linkedin, twitter,
                             include_qr_code, signature_size, logo_url):
    with open(template_path, 'r') as file:
        template = file.read()
    
    avatar_direct_url = convert_drive_link_to_direct_url(avatar_url) if avatar_url else ''
    logo_direct_url = convert_drive_link_to_direct_url(logo_url) if logo_url else ''
    
    replacements = {
        '{{firstname}}': firstname,
        '{{lastname}}': lastname,
        '{{title}}': title,
        '{{email}}': email,
        '{{phone}}': phone,
        '{{avatar_url}}': avatar_direct_url,
        '{{primary_color}}': primary_color,
        '{{secondary_color}}': secondary_color,
        '{{font_style}}': font_style,
        '{{layout_class}}': 'signature-horizontal' if layout == 'horizontal' else 'signature-vertical',
        '{{linkedin_icon}}': '<a href="#"><img src="linkedin_icon.png" alt="LinkedIn"></a>' if linkedin else '',
        '{{twitter_icon}}': '<a href="#"><img src="twitter_icon.png" alt="Twitter"></a>' if twitter else '',
        '{{qr_code}}': '<img src="qr_code.png" alt="QR Code">' if include_qr_code else '',
        '{{signature_size}}': f'font-size: {signature_size}%;',
        '{{logo_url}}': logo_direct_url if logo_direct_url else 'https://drive.google.com/uc?export=view&id=1pCySh1accz-byDc4NNqbpc_ZBgG0zui0'
    }
    
    for placeholder, value in replacements.items():
        if value:
            template = template.replace(placeholder, str(value))
        else:
            # Remove the entire line if the value is empty
            template = re.sub(r'.*' + re.escape(placeholder) + r'.*\n?', '', template)
    
    return template
