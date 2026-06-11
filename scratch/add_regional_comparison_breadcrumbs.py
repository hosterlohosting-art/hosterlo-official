import os
import re

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

def add_regional_breadcrumbs():
    root_dir = r"d:\Hosterlo Official Site"
    
    competitors = {
        "bluehost": "Bluehost",
        "godaddy": "GoDaddy",
        "hostinger": "Hostinger",
        "siteground": "SiteGround"
    }
    
    regions = ["uk", "pk"]
    
    count = 0
    for region in regions:
        for comp_slug, comp_name in competitors.items():
            rel_path = f"{region}/compare/hosterlo-vs-{comp_slug}/index.html"
            file_path = os.path.join(root_dir, rel_path.replace('/', os.sep))
            
            if not os.path.exists(file_path):
                print(f"Warning: File not found: {file_path}")
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Clean existing breadcrumb-nav if any
                if 'class="breadcrumb-nav"' in content or 'aria-label="Breadcrumb"' in content:
                    content = re.sub(r'<nav class="breadcrumb-nav".*?</nav>', '', content, flags=re.DOTALL)
                    
                # Find mobile menu overlay bounds
                o_start, o_end = find_div_bounds(content, 'id="mobile-menu-overlay"')
                if o_end == -1:
                    print(f"Error: Could not find mobile-menu-overlay bounds in: {rel_path}")
                    continue
                    
                breadcrumb_html = f"""
<nav class="breadcrumb-nav max-w-[1440px] mx-auto px-6 pt-6 pb-2 relative z-20" aria-label="Breadcrumb">
    <ol class="flex items-center gap-2 text-xs text-slate-400 font-semibold">
        <li><a href="/{region}/" class="hover:text-primary transition-colors">Home</a></li>
        <li><span class="mx-1">›</span></li>
        <li class="text-primary font-bold">Hosterlo vs {comp_name}</li>
    </ol>
</nav>
"""
                new_content = content[:o_end] + "\n" + breadcrumb_html.strip() + "\n" + content[o_end:]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Added visual breadcrumbs to regional page: {rel_path}")
                count += 1
                
            except Exception as e:
                print(f"Error processing {rel_path}: {e}")
                
    print(f"Completed! Total regional files modified: {count}")

if __name__ == "__main__":
    add_regional_breadcrumbs()
