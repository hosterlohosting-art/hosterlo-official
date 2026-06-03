import os
import re

def extract_premium_blocks():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract header block
    header_start = content.find('<!-- TopNavBar -->')
    header_end = content.find('<!-- Hero Section -->')
    if header_start == -1 or header_end == -1:
        # Fallback to search using regular tags
        header_start = content.find('<header')
        header_end = content.find('</header>') + len('</header>')
    
    header_block = content[header_start:header_end].strip()
    
    # Extract footer block
    footer_start = content.find('<!-- Footer: Standardized White Background, Black Text -->')
    footer_end = content.find('</footer>') + len('</footer>')
    if footer_start == -1 or footer_end == -1:
        footer_start = content.find('<footer')
        footer_end = content.find('</footer>') + len('</footer>')
        
    footer_block = content[footer_start:footer_end].strip()
    
    return header_block, footer_block

def sync_subpage(file_path, header_block, footer_block):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace header
    # Find existing header
    sub_header_start = content.find('<header')
    sub_header_end = content.find('</header>') + len('</header>')
    
    # Also find if there is an overlay mobile menu overlay in the header segment
    sub_overlay_end = content.find('<!-- Mobile Menu Overlay -->')
    if sub_overlay_end != -1:
        # Let's find the closing divs of the mobile menu overlay
        search_start = sub_overlay_end
        div_open_count = 0
        div_close_count = 0
        idx = search_start
        # Search forward for matching closing divs for the overlay container
        overlay_content = content[search_start:]
        # Find three closing </div> tags after the overlay start
        match_idx = 0
        closes_found = 0
        for m in re.finditer(r'</div>', overlay_content):
            closes_found += 1
            if closes_found == 3:
                match_idx = m.end()
                break
        if match_idx > 0:
            sub_header_end = search_start + match_idx

    if sub_header_start != -1 and sub_header_end != -1:
        content = content[:sub_header_start] + header_block + "\n" + content[sub_header_end:]
        
    # Replace footer
    sub_footer_start = content.find('<footer')
    sub_footer_end = content.find('</footer>') + len('</footer>')
    
    if sub_footer_start != -1 and sub_footer_end != -1:
        content = content[:sub_footer_start] + footer_block + "\n" + content[sub_footer_end:]
        
    # Standardize maximum layout widths
    content = content.replace('max-w-[1280px]', 'max-w-[1440px]')
    content = content.replace('"container-max": "1280px"', '"container-max": "1440px"')
    
    # Align head links & fonts
    # Replace Lexend/Inter font with Outfit/Plus Jakarta Sans on all pages to match home page
    old_font_link = 'https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&amp;family=Inter:wght@400;500;600;700&amp;display=swap'
    old_font_link_clean = 'https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&family=Inter:wght@400;500;600;700&display=swap'
    new_font_link = 'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap'
    
    content = content.replace(old_font_link, new_font_link)
    content = content.replace(old_font_link_clean, new_font_link)
    
    # Also look for any basic Inter font links
    old_inter_link = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
    content = content.replace(old_inter_link, new_font_link)
    
    # If font family config exists in inline tailwind theme, update it to match Outfit / Plus Jakarta Sans
    if '"fontFamily": {' in content:
        content = re.sub(
            r'"fontFamily":\s*\{[^}]*\}', 
            '"fontFamily": {\n                    "h3": ["Outfit", "sans-serif"],\n                    "body-sm": ["Plus Jakarta Sans", "sans-serif"],\n                    "body-md": ["Plus Jakarta Sans", "sans-serif"],\n                    "h1": ["Outfit", "sans-serif"],\n                    "body-lg": ["Plus Jakarta Sans", "sans-serif"],\n                    "label-caps": ["Plus Jakarta Sans", "sans-serif"],\n                    "h2": ["Outfit", "sans-serif"]\n            }',
            content
        )
        
    # Save aligned page
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Synchronized branding on page: {file_path}")

def main():
    header_block, footer_block = extract_premium_blocks()
    print("Extracted premium header and footer blocks successfully!")
    
    count = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                file_path = os.path.join(root, file)
                sync_subpage(file_path, header_block, footer_block)
                count += 1
                
    print(f"\nCompleted! Fully synchronized branding across {count} subpages.")

if __name__ == '__main__':
    main()
