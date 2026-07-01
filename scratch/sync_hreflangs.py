import os
import re

def get_clean_url(market, rel_path):
    if rel_path == 'index.html':
        clean_path = ''
    elif rel_path.endswith('/index.html'):
        clean_path = rel_path[:-len('index.html')]
    else:
        clean_path = rel_path
        
    if market == 'us':
        return f"https://hosterlo.com/{clean_path}"
    else:
        return f"https://hosterlo.com/{market}/{clean_path}"

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print(f"Scanning root directory: {root_dir}")
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'scratch' in dirs:
            dirs.remove('scratch')
            
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                html_files.append(full_path)
                
    # Group files by relative path
    grouped_files = {}
    for fp in html_files:
        norm_path = os.path.relpath(fp, root_dir).replace('\\', '/')
        parts = norm_path.split('/')
        if parts[0] in ['uk', 'pk', 'es', 'ph']:
            market = parts[0]
            rel_path = '/'.join(parts[1:])
        else:
            market = 'us'
            rel_path = norm_path
            
        if rel_path not in grouped_files:
            grouped_files[rel_path] = {}
        grouped_files[rel_path][market] = fp

    print(f"Found {len(grouped_files)} unique relative HTML pages.")
    
    updated_count = 0
    for rel_path, markets in grouped_files.items():
        # Generate hreflangs
        hreflangs = []
        
        # Check markets
        if 'us' in markets:
            us_url = get_clean_url('us', rel_path)
            hreflangs.append(('en-us', us_url))
            hreflangs.append(('x-default', us_url))
        
        if 'uk' in markets:
            uk_url = get_clean_url('uk', rel_path)
            hreflangs.append(('en-gb', uk_url))
            if 'us' not in markets:
                # If US is missing, UK can be the x-default
                hreflangs.append(('x-default', uk_url))
                
        if 'pk' in markets:
            pk_url = get_clean_url('pk', rel_path)
            hreflangs.append(('en-pk', pk_url))
            
        if 'es' in markets:
            es_url = get_clean_url('es', rel_path)
            hreflangs.append(('es', es_url))
            
        if 'ph' in markets:
            ph_url = get_clean_url('ph', rel_path)
            hreflangs.append(('en-ph', ph_url))
            
        # Format the block
        indent = "    "
        lines = []
        for lang, url in sorted(hreflangs, key=lambda x: x[0]):
            lines.append(f'{indent}<link rel="alternate" hreflang="{lang}" href="{url}" />')
        hreflangs_str = '\n'.join(lines)
        
        # Inject into each file
        for market, fp in markets.items():
            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                
            # Remove any existing hreflangs
            # Match any <link ... hreflang="..." ...> tag and any whitespace around it
            cleaned_content = re.sub(r'\s*<link\s+[^>]*hreflang=[^>]*>', '', content)
            
            # Find the opening head tag
            head_match = re.search(r'<head\b[^>]*>', cleaned_content, re.IGNORECASE)
            if head_match:
                insert_pos = head_match.end()
                new_content = (
                    cleaned_content[:insert_pos] +
                    "\n" + hreflangs_str +
                    cleaned_content[insert_pos:]
                )
                
                # Write back if changed
                if new_content != content:
                    with open(fp, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated hreflangs in: {os.path.relpath(fp, root_dir)}")
                    updated_count += 1
            else:
                print(f"Warning: Could not find <head> in {fp}")
                
    print(f"\nDone! Updated hreflangs in {updated_count} files.")

if __name__ == '__main__':
    main()
