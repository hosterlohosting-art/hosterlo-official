import os

def replace_in_file(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping: {file_path} (does not exist)")
        return
        
    print(f"Processing: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original_content = content
    
    # Define replacements
    replacements = [
        # Full address replacements
        ("3338 S National Ave, Springfield, MO 65807, United States", "16192 Coastal Highway, Lewes, DE 19958, United States"),
        ("3338 S National Ave, Springfield, MO 65807, USA", "16192 Coastal Highway, Lewes, DE 19958, USA"),
        ("3338 S National Ave, Springfield, MO 65807", "16192 Coastal Highway, Lewes, DE 19958"),
        
        # Schema with spacing variations
        ('"streetAddress":"3338 S National Ave"', '"streetAddress":"16192 Coastal Highway"'),
        ('"streetAddress": "3338 S National Ave"', '"streetAddress": "16192 Coastal Highway"'),
        ('"addressLocality":"Springfield"', '"addressLocality":"Lewes"'),
        ('"addressLocality": "Springfield"', '"addressLocality": "Lewes"'),
        ('"addressRegion":"MO"', '"addressRegion":"DE"'),
        ('"addressRegion": "MO"', '"addressRegion": "DE"'),
        ('"postalCode":"65807"', '"postalCode":"19958"'),
        ('"postalCode": "65807"', '"postalCode": "19958"'),
        ('"addressCountry":"US"', '"addressCountry":"US"'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")
    else:
        print(f"No changes in: {file_path}")

def main():
    files_to_update = [
        "index.html",
        "about-hosterlo/index.html",
        "faq/index.html",
        "legal/index.html",
        "pk/about-hosterlo/index.html",
        "uk/about-hosterlo/index.html",
        "llms.txt",
        "llms-full.txt"
    ]
    
    for file_path in files_to_update:
        replace_in_file(file_path)
        
if __name__ == '__main__':
    main()
