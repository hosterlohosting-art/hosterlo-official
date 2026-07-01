import os

def update_redirect(fp):
    if not os.path.exists(fp):
        return
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        
    old_map = "var regionMap = { 'PK': '/pk/', 'GB': '/uk/' };"
    new_map = "var regionMap = { 'PK': '/pk/', 'GB': '/uk/', 'PH': '/ph/' };"
    
    if old_map in content:
        content = content.replace(old_map, new_map)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated Geo-IP mapping in: {fp}")

def main():
    root_dir = r"d:\Hosterlo Official Site"
    homepages = [
        os.path.join(root_dir, 'index.html'),
        os.path.join(root_dir, 'uk', 'index.html'),
        os.path.join(root_dir, 'es', 'index.html'),
        os.path.join(root_dir, 'pk', 'index.html'),
        os.path.join(root_dir, 'ph', 'index.html')
    ]
    for hp in homepages:
        update_redirect(hp)

if __name__ == '__main__':
    main()
