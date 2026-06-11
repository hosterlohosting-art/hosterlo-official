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

def add_breadcrumbs():
    root_dir = r"d:\Hosterlo Official Site"
    
    # Mapping of relative paths (using forward slashes) to short titles
    blog_posts = {
        "2026/06/03/bluehost-vs-siteground-vs-hosterlo-2026/index.html": "Bluehost vs SiteGround vs Hosterlo 2026",
        "2026/06/03/why-is-my-website-down-common-causes-and-fixes/index.html": "Why Is My Website Down?",
        "2026/06/03/how-to-migrate-website-to-new-host-without-downtime/index.html": "Website Migration Guide",
        "2026/06/03/cpanel-tutorial-for-beginners-complete-guide/index.html": "cPanel Guide for Beginners",
        "2026/06/03/ssl-certificate-guide-website-security-2026/index.html": "SSL & Security Guide",
        "2026/05/05/where-to-purchase-a-domain-name/index.html": "Where to Purchase a Domain",
        "2026/05/04/web-hosting-trends-2026-ai/index.html": "Web Hosting Trends 2026",
        "2026/05/01/checks-before-godaddy-or-hostinger-hosting/index.html": "GoDaddy or Hostinger Checks",
        "2026/04/30/best-web-hosting-for-websites-2026/index.html": "Best Web Hosting 2026",
        "2026/04/29/how-to-start-a-website-domain-hosting/index.html": "How to Start a Website",
        "2025/10/29/go-green-go-fast-why-eco-friendly-wordpress-hosting-isnt-just-a-trend-its-your-business-advantage/index.html": "Eco-Friendly WordPress Hosting"
    }

    count = 0
    for rel_path, title in blog_posts.items():
        file_path = os.path.join(root_dir, rel_path.replace('/', os.sep))
        if not os.path.exists(file_path):
            print(f"Warning: File not found: {file_path}")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check if breadcrumbs are already present
            if 'class="breadcrumb-nav"' in content or 'aria-label="Breadcrumb"' in content:
                print(f"Breadcrumbs already present in: {rel_path}. Skipping or updating...")
                # We can remove existing breadcrumb block if it exists to refresh it, but let's see.
                # Let's remove any existing breadcrumb-nav block to be clean
                content = re.sub(r'<nav class="breadcrumb-nav".*?</nav>', '', content, flags=re.DOTALL)
                
            # Find the end of mobile menu overlay
            o_start, o_end = find_div_bounds(content, 'id="mobile-menu-overlay"')
            if o_end == -1:
                print(f"Error: Could not find mobile-menu-overlay bounds in: {rel_path}")
                continue
                
            breadcrumb_html = f"""
<nav class="breadcrumb-nav max-w-4xl mx-auto px-6 pt-8 pb-2 relative z-20" aria-label="Breadcrumb">
    <ol class="flex items-center gap-2 text-xs text-slate-400 font-semibold">
        <li><a href="/" class="hover:text-primary transition-colors">Home</a></li>
        <li><span class="mx-1">›</span></li>
        <li><a href="/blog/" class="hover:text-primary transition-colors">Blog</a></li>
        <li><span class="mx-1">›</span></li>
        <li class="text-primary font-bold">{title}</li>
    </ol>
</nav>
"""
            # Insert breadcrumb_html right after o_end
            new_content = content[:o_end] + "\n" + breadcrumb_html.strip() + "\n" + content[o_end:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Added visual breadcrumbs to: {rel_path}")
            count += 1
            
        except Exception as e:
            print(f"Error processing {rel_path}: {e}")
            
    print(f"Completed! Total files modified: {count}")

if __name__ == "__main__":
    add_breadcrumbs()
