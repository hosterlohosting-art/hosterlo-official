import os
import re
from urllib.parse import urlparse

def audit_site():
    root_dir = r"d:\Hosterlo Official Site"
    print(f"Auditing site at {root_dir} for broken internal links, images, and HTML bugs...")
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'scratch' in dirs:
            dirs.remove('scratch')
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    broken_links = []
    missing_images = []
    missing_alts = []
    empty_attrs = []
    
    for fp in html_files:
        rel_fp = os.path.relpath(fp, root_dir).replace('\\', '/')
        
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        # 1. Audit href links
        # Find all href="..." or href='...'
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
        for href in hrefs:
            if not href or href == '#' or href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:')):
                continue
                
            # Strip anchors and query params
            clean_href = href.split('#')[0].split('?')[0]
            if not clean_href:
                continue
                
            # Resolve path relative to root if starts with '/', or relative to file if relative
            if clean_href.startswith('/'):
                target_path = os.path.normpath(os.path.join(root_dir, clean_href.lstrip('/')))
            else:
                target_path = os.path.normpath(os.path.join(os.path.dirname(fp), clean_href))
                
            # Check if directory or file exists
            if os.path.isdir(target_path):
                index_path = os.path.join(target_path, 'index.html')
                if not os.path.exists(index_path):
                    broken_links.append((rel_fp, href, f"Index missing: {index_path}"))
            elif not os.path.exists(target_path):
                # Try adding /index.html if clean_href didn't have extension
                if not os.path.extsep in os.path.basename(clean_href):
                    index_path = target_path + '/index.html'
                    if not os.path.exists(index_path):
                        broken_links.append((rel_fp, href, f"File missing: {target_path}"))
                else:
                    broken_links.append((rel_fp, href, f"File missing: {target_path}"))

        # 2. Audit image src tags
        imgs = re.findall(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>', content, re.IGNORECASE)
        for src in imgs:
            if not src:
                empty_attrs.append((rel_fp, 'img src'))
                continue
            if src.startswith(('http://', 'https://', 'data:')):
                continue
                
            clean_src = src.split('#')[0].split('?')[0]
            if clean_src.startswith('/'):
                img_target = os.path.normpath(os.path.join(root_dir, clean_src.lstrip('/')))
            else:
                img_target = os.path.normpath(os.path.join(os.path.dirname(fp), clean_src))
                
            if not os.path.exists(img_target):
                missing_images.append((rel_fp, src, img_target))

        # 3. Check for img tags without alt attributes
        all_img_tags = re.findall(r'<img\s+[^>]*>', content, re.IGNORECASE)
        for img_tag in all_img_tags:
            if 'alt=' not in img_tag.lower():
                missing_alts.append((rel_fp, img_tag[:60]))

    print(f"\n--- AUDIT RESULTS ---")
    print(f"Total HTML files scanned: {len(html_files)}")
    
    # Aggregate broken links by target
    link_counts = {}
    for rel_fp, href, err in broken_links:
        link_counts[href] = link_counts.get(href, 0) + 1
        
    print(f"\nUnique Broken Link Targets ({len(link_counts)} total):")
    for target, count in sorted(link_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {target:<40} -> missing on {count} pages")
        
    print(f"\nMissing Local Images: {len(missing_images)}")
    print(f"Images Missing alt Attribute: {len(missing_alts)}")
    print(f"Empty Attributes: {len(empty_attrs)}")

if __name__ == '__main__':
    audit_site()
