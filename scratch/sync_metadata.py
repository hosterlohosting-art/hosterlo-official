import os
import re

def sync_page_metadata(fp, root_dir):
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        
    # Skip meta redirects
    if '<meta http-equiv="refresh"' in content:
        return False
        
    rel_path = os.path.relpath(fp, root_dir).replace('\\', '/')
    parts = rel_path.split('/')
    market = parts[0] if parts[0] in ['uk', 'pk', 'es', 'ph'] else 'us'
    
    # 1. Extract Title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Hosterlo | Web Hosting & Domains"
    
    # 2. Extract Description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content, re.IGNORECASE)
    description = desc_match.group(1).strip() if desc_match else "Get fast NVMe web hosting, free .com domain, SSL, and custom business email with Hosterlo."
    
    # 3. Extract Image
    img_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', content, re.IGNORECASE)
    if img_match:
        image_url = img_match.group(1)
    else:
        image_url = "https://hosterlo.com/assets/hero-section-image.webp"
        
    # Clean image URL to absolute WebP
    if not image_url.startswith('http'):
        if image_url.startswith('/'):
            image_url = f"https://hosterlo.com{image_url}"
        else:
            image_url = f"https://hosterlo.com/{image_url}"
            
    # Determine locale
    locale = "es_ES" if market == 'es' else "en_US"
    
    # Determine clean URL
    if rel_path == 'index.html':
        canonical_url = "https://hosterlo.com/"
    elif rel_path.endswith('/index.html'):
        canonical_url = f"https://hosterlo.com/{rel_path[:-10]}"
    else:
        canonical_url = f"https://hosterlo.com/{rel_path}"
        
    # Check if OG tags exist
    has_og = 'property="og:title"' in content or 'property="og:site_name"' in content
    
    meta_block = f"""
    <!-- Open Graph / Facebook -->
    <meta property="og:locale" content="{locale}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Hosterlo">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image_url}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@hosterlo">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image_url}">"""

    orig = content
    if not has_og:
        # Inject metadata before </head>
        head_end = content.find('</head>')
        if head_end != -1:
            content = content[:head_end] + meta_block + "\n" + content[head_end:]
    else:
        # Update existing og:title and og:description if out of date
        content = re.sub(r'<meta\s+property="og:title"\s+content="[^"]*"', f'<meta property="og:title" content="{title}"', content)
        content = re.sub(r'<meta\s+property="og:description"\s+content="[^"]*"', f'<meta property="og:description" content="{description}"', content)
        content = re.sub(r'<meta\s+name="twitter:title"\s+content="[^"]*"', f'<meta name="twitter:title" content="{title}"', content)
        content = re.sub(r'<meta\s+name="twitter:description"\s+content="[^"]*"', f'<meta name="twitter:description" content="{description}"', content)
        
    if content != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Synced Open Graph metadata in: {rel_path}")
        return True
    return False

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print("Auditing and syncing Open Graph metadata across all pages...")
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs or 'scratch' in dirs:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    count = 0
    for fp in html_files:
        if sync_page_metadata(fp, root_dir):
            count += 1
            
    print(f"\nDone! Synced Open Graph metadata in {count} files.")

if __name__ == '__main__':
    main()
