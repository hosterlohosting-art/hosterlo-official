import os
import re

def create_redirect_page(target_dir, destination_url, title_name):
    os.makedirs(target_dir, exist_ok=True)
    index_path = os.path.join(target_dir, 'index.html')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={destination_url}">
    <link rel="canonical" href="https://hosterlo.com{destination_url}">
    <title>Redirecting - {title_name} | Hosterlo</title>
    <script>window.location.replace("{destination_url}");</script>
</head>
<body>
    <p>Redirecting to <a href="{destination_url}">{title_name}</a>...</p>
</body>
</html>
"""
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Created redirect endpoint at: {os.path.relpath(index_path, r'd:\Hosterlo Official Site')}")

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print("Fixing all missing route endpoints and broken references...")
    
    # 1. Create missing redirect routes
    redirects = [
        ('es/blog', '/blog/', 'Hosterlo Blog'),
        ('es/free-tools', '/free-tools/', 'Free Tools'),
        ('es/terms-conditions', '/terms-conditions/', 'Terms of Service'),
        ('es/privacy-policy', '/privacy-policy/', 'Privacy Policy'),
        ('es/refund-policy', '/refund-policy/', 'Refund Policy'),
        ('es/legal/ai-writer-terms', '/legal/ai-writer-terms/', 'AI Writer Terms'),
        ('free-offer', '/pricing/', 'Exclusive Free Offer'),
        ('es/free-offer', '/pricing/', 'Oferta Especial'),
        ('es/website-migration', '/website-migration/', 'Website Migration'),
        ('infrastructure', '/hosting/', 'Cloud Infrastructure'),
    ]
    
    for rel_folder, dest, title in redirects:
        full_dir = os.path.join(root_dir, rel_folder)
        create_redirect_page(full_dir, dest, title)
        
    # 2. Fix /es/styles.css and /es/sitemap.xml references in HTML files
    print("\nCorrecting asset/sitemap paths in HTML files...")
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs or 'scratch' in dirs:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    updated = 0
    for fp in html_files:
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        orig = content
        content = content.replace('href="/es/styles.css"', 'href="/styles.css"')
        content = content.replace('href="/es/sitemap.xml"', 'href="/sitemap.xml"')
        
        if content != orig:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
            print(f"Fixed CSS/Sitemap path in: {os.path.relpath(fp, root_dir)}")
            
    print(f"\nDone! Corrected references in {updated} files.")

if __name__ == '__main__':
    main()
