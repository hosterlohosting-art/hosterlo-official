import os
import re

html_pattern = re.compile(r'<html\b[^>]*\bclass="([^"]*)"', re.IGNORECASE)
found = 0

for root, dirs, files in os.walk('.'):
    if '.git' in dirs:
        dirs.remove('.git')
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
            match = html_pattern.search(content)
            if match:
                classes = match.group(1)
                if 'opacity-0' in classes:
                    print(f"Warning: {file_path} still has opacity-0 in html class: {classes}")
                    found += 1

if found == 0:
    print("All HTML files are completely clear of opacity-0 on the html element!")
else:
    print(f"Found {found} files that still need fixing.")
