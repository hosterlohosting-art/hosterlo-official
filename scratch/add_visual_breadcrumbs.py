import os
import re

def clean_h1_text(h1_html):
    # Remove HTML tags
    cleaned = re.sub(r'<[^>]+>', '', h1_html)
    # Normalize whitespace
    cleaned = ' '.join(cleaned.split())
    return cleaned

def get_breadcrumbs_html(market, rel_path, h1_text):
    # Determine theme based on path
    dark_theme_paths = [
        'compare/', 'alternatives/', 'support/', 'about-hosterlo', 
        'contact-us', 'pricing', 'faq', 'dmarc-record-lookup', 
        'spf-record-lookup', 'legal/', 'blog/'
    ]
    is_dark_text = any(p in rel_path for p in dark_theme_paths)
    
    # Label translations
    home_label = 'Inicio' if market == 'es' else 'Home'
    
    # Class styles
    if is_dark_text:
        nav_class = "flex flex-wrap mb-4 text-xs font-semibold text-slate-500 gap-1.5 items-center relative z-20"
        link_class = "hover:text-primary transition-colors text-slate-500"
        separator_class = "material-symbols-outlined text-[10px] text-slate-400 select-none pointer-events-none"
        current_class = "text-slate-400 font-normal line-clamp-1 max-w-[200px] sm:max-w-none"
    else:
        nav_class = "flex flex-wrap mb-4 text-xs font-semibold text-indigo-300/80 gap-1.5 items-center relative z-20"
        link_class = "hover:text-white transition-colors text-indigo-300/80"
        separator_class = "material-symbols-outlined text-[10px] text-indigo-400/60 select-none pointer-events-none"
        current_class = "text-indigo-200/50 font-normal line-clamp-1 max-w-[200px] sm:max-w-none"
        
    home_url = f"/{market}/" if market != 'us' else '/'
    
    parts = []
    # Home link
    parts.append(f'<a href="{home_url}" class="{link_class}">{home_label}</a>')
    
    # Parse intermediate parts
    # e.g., hosting/shared-hosting/index.html -> ['hosting', 'shared-hosting']
    path_parts = [p for p in rel_path.split('/') if p and p != 'index.html']
    
    # Check if this is a blog post (path starts with year digits)
    is_blog_post = len(path_parts) > 0 and path_parts[0].isdigit()
    
    if is_blog_post:
        # For blog posts, intermediate path is just Blog
        blog_url = f"/{market}/blog/" if market != 'us' else '/blog/'
        parts.append(f'<span class="{separator_class}">chevron_right</span>')
        parts.append(f'<a href="{blog_url}" class="{link_class}">Blog</a>')
    else:
        # Build standard folders path
        current_accum = ""
        for i, folder in enumerate(path_parts[:-1]):
            # Clean folder name to display label
            display_label = folder.replace('-', ' ').title()
            if folder == 'uk':
                display_label = 'UK'
            elif folder == 'pk':
                display_label = 'Pakistan'
            elif folder == 'es':
                display_label = 'Español'
            
            # Map clean URLs
            current_accum += f"{folder}/"
            url = f"/{market}/{current_accum}" if market != 'us' else f"/{current_accum}"
            
            parts.append(f'<span class="{separator_class}">chevron_right</span>')
            parts.append(f'<a href="{url}" class="{link_class}">{display_label}</a>')
            
    # Add current page label
    parts.append(f'<span class="{separator_class}">chevron_right</span>')
    parts.append(f'<span class="{current_class}">{h1_text}</span>')
    
    return f'<nav class="{nav_class}" aria-label="Breadcrumb">{"".join(parts)}</nav>'

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print("Injecting visual breadcrumbs above H1 on inner subpages...")
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'scratch' in dirs:
            dirs.remove('scratch')
            
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    updated_count = 0
    for fp in html_files:
        norm_path = os.path.relpath(fp, root_dir).replace('\\', '/')
        parts = norm_path.split('/')
        if parts[0] in ['uk', 'pk', 'es']:
            market = parts[0]
            rel_path = '/'.join(parts[1:])
        else:
            market = 'us'
            rel_path = norm_path
            
        # Skip homepages (clean relative path is empty or index.html)
        if rel_path in ['index.html', '']:
            continue
            
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        # Do not inject if breadcrumb navigation already exists
        if 'aria-label="Breadcrumb"' in content:
            continue
            
        # Find H1
        h1_match = re.search(r'<h1\b[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            h1_full_tag = h1_match.group(0)
            h1_inner_text = clean_h1_text(h1_match.group(1))
            
            breadcrumbs = get_breadcrumbs_html(market, rel_path, h1_inner_text)
            
            # Inject breadcrumbs directly above the H1 tag block
            new_content = content.replace(h1_full_tag, f"{breadcrumbs}\n{h1_full_tag}")
            
            if new_content != content:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Injected breadcrumbs in: {os.path.relpath(fp, root_dir)}")
                updated_count += 1
                
    print(f"\nDone! Injected breadcrumbs into {updated_count} files.")

if __name__ == '__main__':
    main()
