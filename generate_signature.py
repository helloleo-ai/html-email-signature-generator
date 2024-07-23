import re
import os
import csv

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

def process_manual_input():
    firstname = input("Enter your first name: ")
    lastname = input("Enter your last name: ")
    title = input("Enter your work title: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    avatar_url = input("Enter your avatar URL: ")

    return [(firstname, lastname, title, email, phone, avatar_url)]

def process_csv_input(csv_path):
    data = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print("row:", row)
            data.append((row['firstname'], row['lastname'], row['title'], row['email'], row['phone'], row['avatar_url']))
    return data

def main():
    choice = input("Choose option 1 (manual input) or option 2 (from CSV template): ")
    if choice == '1':
        user_data = process_manual_input()
    elif choice == '2':
        csv_path = input("Enter the path to the CSV file: ")
        user_data = process_csv_input(csv_path)
    else:
        print("Invalid choice. Exiting.")
        return

    folder = "html_signatures"
    os.makedirs(folder, exist_ok=True)

    for data in user_data:
        firstname, lastname, title, email, phone, avatar_url = data
        signature = generate_email_signature(firstname, lastname, title, email, phone, avatar_url)
        
        normalized_firstname = normalize_name(firstname)
        normalized_lastname = normalize_name(lastname)
        filename = f"{normalized_firstname}_{normalized_lastname}.html"
        filepath = os.path.join(folder, filename)
        
        with open(filepath, "w") as file:
            file.write(signature)
        
        print(f"\nGenerated HTML Signature for {firstname} {lastname}:\n")
        print(signature)
        print(f"\nThe signature has been saved to '{filepath}'.")

if __name__ == "__main__":
    main()
