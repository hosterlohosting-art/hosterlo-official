import os

root_dir = r"D:\Hosterlo Official Site"

replacements = {
    'href="/pk/styles.css"': 'href="/styles.css"',
    'href="/uk/styles.css"': 'href="/styles.css"',
    'href="/pk/sitemap.xml"': 'href="/sitemap.xml"',
    'href="/uk/sitemap.xml"': 'href="/sitemap.xml"'
}

count = 0
for root, dirs, files in os.walk(root_dir):
    if '.git' in dirs:
        dirs.remove('.git')
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            modified = False
            for target, rep in replacements.items():
                if target in content:
                    content = content.replace(target, rep)
                    modified = True
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Corrected paths in: {file_path}")
                count += 1

print(f"Path correction complete. Modified {count} files.")
