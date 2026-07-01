import os
import re
import json

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print("Starting SEO and code integrity verification...")
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'scratch' in dirs:
            dirs.remove('scratch')
            
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    errors = 0
    checked_files = 0
    
    for fp in html_files:
        rel_path = os.path.relpath(fp, root_dir)
        # Skip simple redirect pages
        if 'hosting-for-ecommerce' in rel_path or 'hosting-for-bloggers' in rel_path:
            continue
            
        checked_files += 1
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        # 1. Check for duplicate hreflangs
        hreflang_tags = re.findall(r'<link\s+[^>]*hreflang=["\']([^"\']+)["\']', content)
        if len(hreflang_tags) != len(set(hreflang_tags)):
            print(f"Error in {rel_path}: Duplicate hreflang tags found! {hreflang_tags}")
            errors += 1
            
        # 2. Check JSON-LD validation
        scripts = re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
        for s in scripts:
            try:
                json.loads(s.strip())
            except Exception as e:
                print(f"Error in {rel_path}: Invalid JSON-LD block! {e}")
                errors += 1
                
        # 3. Check visual breadcrumbs on non-homepages
        is_homepage = rel_path == 'index.html' or rel_path.endswith(r'\index.html') and len(rel_path.split('\\')) == 2 and rel_path.split('\\')[0] in ['uk', 'pk', 'es', 'ph']
        if not is_homepage and 'aria-label="Breadcrumb"' not in content:
            print(f"Warning in {rel_path}: Missing visual breadcrumbs!")
            # We treat this as a warning, not a hard error since some tools pages may not need them
            
    print(f"\nVerification finished: Checked {checked_files} main pages. Found {errors} block errors.")

if __name__ == '__main__':
    main()
