import os

replacements = {
    "items-centre": "items-center",
    "justify-centre": "justify-center",
    "text-centre": "text-center",
    "self-centre": "self-center",
    "content-centre": "content-center",
    "place-items-centre": "place-items-center",
    "place-content-centre": "place-content-center",
    "place-self-centre": "place-self-center",
    "background-colour": "background-color",
    "border-colour": "border-color",
    "transition-colours": "transition-colors",
    '"colours":': '"colors":',
    "'colours':": "'colors':",
    "colour:": "color:",
    "colour-": "color-",
    "help_centre": "help_center",
    "align-items: centre;": "align-items: center;",
    "background-position: centre;": "background-position: center;",
    "justify-content: centre;": "justify-content: center;",
}

def fix_html_files(root_dir):
    fixed_count = 0
    total_replacements = 0
    
    for dirpath, _, filenames in os.walk(root_dir):
        if ".git" in dirpath:
            continue
            
        for filename in filenames:
            if filename.endswith(".html"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    new_content = content
                    file_modified = False
                    
                    for target, replacement in replacements.items():
                        if target in new_content:
                            count = new_content.count(target)
                            new_content = new_content.replace(target, replacement)
                            total_replacements += count
                            file_modified = True
                            
                    if file_modified:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Fixed {file_path}")
                        fixed_count += 1
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
    print(f"\nCompleted! Fixed {fixed_count} files with {total_replacements} total replacements.")

if __name__ == "__main__":
    project_root = r"d:\Hosterlo Official Site"
    fix_html_files(project_root)
