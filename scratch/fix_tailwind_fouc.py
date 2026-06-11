import os
import re

count = 0
# HTML pattern matching html tags with class attributes
html_pattern = re.compile(r'(<html\b[^>]*\bclass=")([^"]*)(")', re.IGNORECASE)

for root, dirs, files in os.walk('.'):
    if '.git' in dirs:
        dirs.remove('.git')
        
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            match = html_pattern.search(content)
            if match:
                classes = match.group(2)
                if 'opacity-0' not in classes:
                    # Append opacity-0 to classes
                    new_classes = f"{classes} opacity-0".strip()
                    content = html_pattern.sub(rf'\1{new_classes}\3', content)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Added opacity-0 to html tag class in: {file_path}")
                    count += 1

print(f"Successfully processed {count} HTML files.")
