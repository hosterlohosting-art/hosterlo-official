import os
import re
import datetime

def get_page_info(fp, root_dir):
    rel_path = os.path.relpath(fp, root_dir).replace('\\', '/')
    
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        
    # Skip meta redirects
    if '<meta http-equiv="refresh"' in content:
        return None
        
    # Calculate clean URL
    if rel_path == 'index.html':
        clean_url = "https://hosterlo.com/"
        priority = "1.00"
        freq = "daily"
    elif rel_path.endswith('/index.html'):
        sub = rel_path[:-10] # remove index.html
        clean_url = f"https://hosterlo.com/{sub}"
        
        # Priority rules
        if sub in ['uk/', 'pk/', 'es/', 'ph/']:
            priority = "0.85"
            freq = "daily"
        elif sub in ['hosting/', 'domains/', 'pricing/', 'services/']:
            priority = "0.90"
            freq = "weekly"
        elif sub.startswith(('compare/', 'alternatives/')):
            priority = "0.75"
            freq = "weekly"
        elif sub.startswith(('2025/', '2026/', 'blog/')):
            priority = "0.70"
            freq = "monthly"
        else:
            priority = "0.80"
            freq = "weekly"
    else:
        clean_url = f"https://hosterlo.com/{rel_path}"
        priority = "0.70"
        freq = "monthly"
        
    # Get lastmod date
    mtime = os.path.getmtime(fp)
    lastmod = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    
    # Extract primary image if available
    img_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', content, re.IGNORECASE)
    if not img_match:
        img_match = re.search(r'<img\s+[^>]*src="([^"]+)"', content, re.IGNORECASE)
        
    img_url = None
    if img_match:
        raw_img = img_match.group(1)
        if raw_img.startswith('https://'):
            img_url = raw_img
        elif raw_img.startswith('/'):
            img_url = f"https://hosterlo.com{raw_img}"
        elif not raw_img.startswith(('http', 'data:')):
            img_url = f"https://hosterlo.com/{raw_img}"
            
    return {
        'url': clean_url,
        'priority': priority,
        'freq': freq,
        'lastmod': lastmod,
        'img': img_url
    }

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print(f"Scanning workspace for sitemap generation...")
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs or 'scratch' in dirs:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    pages = []
    for fp in html_files:
        info = get_page_info(fp, root_dir)
        if info:
            pages.append(info)
            
    # Sort pages: higher priority first, then URL alphabetically
    pages.sort(key=lambda x: (-float(x['priority']), x['url']))
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
    ]
    
    for p in pages:
        xml_lines.append('  <url>')
        xml_lines.append(f"    <loc>{p['url']}</loc>")
        xml_lines.append(f"    <lastmod>{p['lastmod']}</lastmod>")
        xml_lines.append(f"    <changefreq>{p['freq']}</changefreq>")
        xml_lines.append(f"    <priority>{p['priority']}</priority>")
        if p['img']:
            xml_lines.append(f"    <image:image><image:loc>{p['img']}</image:loc></image:image>")
        xml_lines.append('  </url>')
        
    xml_lines.append('</urlset>')
    
    sitemap_path = os.path.join(root_dir, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
        
    print(f"Rebuilt sitemap.xml successfully! Included {len(pages)} valid indexed URLs.")

if __name__ == '__main__':
    main()
