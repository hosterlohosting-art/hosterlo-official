import os
import re

def find_tag_bounds(content, tag_name, start_search=0):
    start_pos = content.find(f'<{tag_name}', start_search)
    if start_pos == -1:
        return -1, -1
    
    end_pos = content.find(f'</{tag_name}>', start_pos)
    if end_pos == -1:
        return -1, -1
    end_pos += len(f'</{tag_name}>')
    return start_pos, end_pos

def find_div_bounds(content, identifier, start_search=0):
    id_pos = content.find(identifier, start_search)
    if id_pos == -1:
        return -1, -1
    
    start_pos = content.rfind('<div', 0, id_pos)
    if start_pos == -1:
        return -1, -1
        
    depth = 0
    pattern = re.compile(r'<div\b|</div>', re.IGNORECASE)
    for match in pattern.finditer(content, start_pos):
        tag = match.group(0).lower()
        if tag.startswith('<div'):
            depth += 1
        elif tag == '</div>':
            depth -= 1
            if depth == 0:
                return start_pos, match.end()
                
    return -1, -1

def extract_premium_blocks_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find the header bounds
    h_start, h_end = find_tag_bounds(content, 'header')
    if h_start == -1 or h_end == -1:
        raise ValueError(f"Could not find <header> block in {file_path}")
        
    # Find the overlay bounds
    o_start, o_end = find_div_bounds(content, 'id="mobile-menu-overlay"')
    
    # The header block to extract starts at min(h_start, o_start) and ends at max(h_end, o_end)
    zone_start = min(h_start, o_start) if o_start != -1 else h_start
    zone_end = max(h_end, o_end) if o_end != -1 else h_end
    
    # Backtrack zone_start to include comment "<!-- TopNavBar -->" if it is just before
    comment_pos = content.rfind('<!-- TopNavBar -->', 0, zone_start)
    if comment_pos != -1 and zone_start - comment_pos < 100:
        zone_start = comment_pos
        
    header_block = content[zone_start:zone_end].strip()
    
    # Find the footer bounds
    f_start, f_end = find_tag_bounds(content, 'footer')
    if f_start == -1 or f_end == -1:
        raise ValueError(f"Could not find <footer> block in {file_path}")
        
    # Backtrack f_start to include footer comment if present
    comment_pos = content.rfind('<!-- Footer', 0, f_start)
    if comment_pos != -1 and f_start - comment_pos < 150:
        f_start = comment_pos
        
    footer_block = content[f_start:f_end].strip()
    
    return header_block, footer_block

def extract_premium_blocks():
    return extract_premium_blocks_from_file('index.html')

def sync_subpage(file_path, header_block, footer_block):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find header bounds
    h_start, h_end = find_tag_bounds(content, 'header')
    
    # Find all occurrences of mobile-menu-overlay
    overlay_ranges = []
    search_pos = 0
    while True:
        o_start, o_end = find_div_bounds(content, 'id="mobile-menu-overlay"', search_pos)
        if o_start == -1:
            break
        overlay_ranges.append((o_start, o_end))
        search_pos = o_end
        
    if not overlay_ranges:
        comment_pos = content.find('<!-- Mobile Menu Overlay -->')
        if comment_pos != -1:
            o_start, o_end = find_div_bounds(content, 'id="mobile-menu-overlay"', comment_pos)
            if o_start != -1:
                overlay_ranges.append((o_start, o_end))
                
    starts = []
    ends = []
    if h_start != -1:
        starts.append(h_start)
        ends.append(h_end)
    for o_s, o_e in overlay_ranges:
        starts.append(o_s)
        ends.append(o_e)
        
    if starts:
        zone_start = min(starts)
        zone_end = max(ends)
        
        # Include preceding comments if they exist
        comment_pos = content.rfind('<!-- TopNavBar -->', 0, zone_start)
        if comment_pos != -1 and zone_start - comment_pos < 100:
            zone_start = comment_pos
            
        comment_pos = content.rfind('<!-- Mobile Menu Overlay -->', 0, zone_start)
        if comment_pos != -1 and zone_start - comment_pos < 100:
            zone_start = comment_pos
            
        # Replace the entire zone with the new header block
        content = content[:zone_start] + header_block + "\n" + content[zone_end:]
        
    # Replace footer
    f_start, f_end = find_tag_bounds(content, 'footer')
    if f_start != -1:
        # Include preceding comment
        comment_pos = content.rfind('<!-- Footer', 0, f_start)
        if comment_pos != -1 and f_start - comment_pos < 155:
            f_start = comment_pos
            
        content = content[:f_start] + footer_block + "\n" + content[f_end:]
        
    # Standardize maximum layout widths
    content = content.replace('max-w-[1280px]', 'max-w-[1440px]')
    content = content.replace('"container-max": "1280px"', '"container-max": "1440px"')
    
    # Align font links
    old_font_link = 'https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&amp;family=Inter:wght@400;500;600;700&amp;display=swap'
    old_font_link_clean = 'https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&family=Inter:wght@400;500;600;700&display=swap'
    new_font_link = 'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap'
    
    content = content.replace(old_font_link, new_font_link)
    content = content.replace(old_font_link_clean, new_font_link)
    
    old_inter_link = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
    content = content.replace(old_inter_link, new_font_link)
    
    if '"fontFamily": {' in content:
        content = re.sub(
            r'"fontFamily":\s*\{[^}]*\}', 
            '"fontFamily": {\n                    "h3": ["Outfit", "sans-serif"],\n                    "body-sm": ["Plus Jakarta Sans", "sans-serif"],\n                    "body-md": ["Plus Jakarta Sans", "sans-serif"],\n                    "h1": ["Outfit", "sans-serif"],\n                    "body-lg": ["Plus Jakarta Sans", "sans-serif"],\n                    "label-caps": ["Plus Jakarta Sans", "sans-serif"],\n                    "h2": ["Outfit", "sans-serif"]\n            }',
            content
        )
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Synchronized branding on page: {file_path}")

def main():
    us_header, us_footer = extract_premium_blocks()
    print("Extracted premium US header and footer blocks successfully!")
    
    uk_header, uk_footer = None, None
    if os.path.exists(os.path.join('uk', 'index.html')):
        try:
            uk_header, uk_footer = extract_premium_blocks_from_file(os.path.join('uk', 'index.html'))
            print("Extracted UK premium header and footer blocks successfully!")
        except Exception as e:
            print(f"Warning: Could not extract UK blocks: {e}")
            
    pk_header, pk_footer = None, None
    if os.path.exists(os.path.join('pk', 'index.html')):
        try:
            pk_header, pk_footer = extract_premium_blocks_from_file(os.path.join('pk', 'index.html'))
            print("Extracted PK premium header and footer blocks successfully!")
        except Exception as e:
            print(f"Warning: Could not extract PK blocks: {e}")
            
    count = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                norm_path = os.path.normpath(file_path)
                
                # Skip the homepages of each market to avoid overwriting their template source
                if norm_path in ['index.html', os.path.join('.', 'index.html'), os.path.join('uk', 'index.html'), os.path.join('pk', 'index.html')]:
                    continue
                    
                # Determine which market blocks to use
                norm_path_lower = norm_path.lower()
                if os.sep + 'uk' + os.sep in norm_path_lower or norm_path_lower.startswith('uk' + os.sep):
                    h_block = uk_header if uk_header else us_header
                    f_block = uk_footer if uk_footer else us_footer
                elif os.sep + 'pk' + os.sep in norm_path_lower or norm_path_lower.startswith('pk' + os.sep):
                    h_block = pk_header if pk_header else us_header
                    f_block = pk_footer if pk_footer else us_footer
                else:
                    h_block = us_header
                    f_block = us_footer
                    
                sync_subpage(file_path, h_block, f_block)
                count += 1
                
    print(f"\nCompleted! Fully synchronized branding across {count} subpages.")

if __name__ == '__main__':
    main()
