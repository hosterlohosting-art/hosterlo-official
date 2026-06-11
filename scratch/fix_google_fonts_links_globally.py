import os

def fix_font_links():
    root_dir = r"d:\Hosterlo Official Site"
    target_link_1 = 'href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap"'
    target_link_2 = 'href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"'
    target_link_3 = 'href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1"'
    target_link_4 = 'href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap"'
    
    replacement_link = 'href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap"'
    
    target_import = "@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');"
    replacement_import = "@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');"

    count = 0
    for root, dirs, files in os.walk(root_dir):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if file.endswith('.html') or file.endswith('.css'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    new_content = new_content.replace(target_link_1, replacement_link)
                    new_content = new_content.replace(target_link_2, replacement_link)
                    new_content = new_content.replace(target_link_3, replacement_link)
                    new_content = new_content.replace(target_link_4, replacement_link)
                    new_content = new_content.replace(target_import, replacement_import)
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed fonts in: {file_path}")
                        count += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
    print(f"Completed! Total files modified: {count}")

if __name__ == "__main__":
    fix_font_links()
