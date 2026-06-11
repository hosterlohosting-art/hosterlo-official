import os
import re

count = 0
# HTML pattern matching html tags with class attributes
html_pattern = re.compile(r'(<html\b[^>]*\bclass=")([^"]*)(")', re.IGNORECASE)

for root, dirs, files in os.walk('.'):
    # Skip git folder
    if '.git' in dirs:
        dirs.remove('.git')
        
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
                
            match = html_pattern.search(content)
            if match:
                classes = match.group(2)
                if 'opacity-0' in classes:
                    # Filter out opacity-0
                    class_list = [c for c in classes.split() if c != 'opacity-0']
                    new_classes = " ".join(class_list)
                    # Replace in content
                    # Using lambda to avoid issues with backslashes in replacement string
                    replacement = rf'\g<1>{new_classes}\g<3>'
                    content = html_pattern.sub(replacement, content)
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Removed opacity-0 from html tag class in: {file_path}")
                        count += 1
                    except Exception as e:
                        print(f"Error writing {file_path}: {e}")

print(f"Successfully processed and fixed {count} HTML files.")
