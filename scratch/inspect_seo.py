import os, glob, re

base = r'd:\Hosterlo Official Site'
stats = {'files': 0}
report = []

for html in glob.glob(os.path.join(base, '**', '*.html'), recursive=True):
    if '.git' in html:
        continue
    rel = os.path.relpath(html, base)
    stats['files'] += 1
    
    with open(html, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Get Title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else None
    
    # Get Meta Description
    desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="(.*?)"', content, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta[^>]*content="(.*?)"[^>]*name="description"', content, re.IGNORECASE)
    desc = desc_match.group(1).strip() if desc_match else None
    
    # Get Canonical
    canon_match = re.search(r'<link[^>]*rel="canonical"[^>]*href="(.*?)"', content, re.IGNORECASE)
    canon = canon_match.group(1).strip() if canon_match else None
    
    # Get Hreflangs
    hreflangs = re.findall(r'<link[^>]*hreflang="(.*?)"[^>]*href="(.*?)"', content, re.IGNORECASE)
    
    # Check H1s
    h1s = re.findall(r'<h1[\s>](.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    
    # Missing OG image or Twitter card
    og_image = 'property="og:image"' in content or 'og:image' in content
    twitter_card = 'twitter:card' in content
    
    # Schemas
    schemas = re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    
    # Check constraints
    issues = []
    if not title:
        issues.append("Missing Title")
    elif len(title) < 40 or len(title) > 70:
        issues.append(f"Title length ({len(title)}) not optimal (should be 40-70)")
        
    if not desc:
        issues.append("Missing Meta Description")
    elif len(desc) < 120 or len(desc) > 165:
        issues.append(f"Description length ({len(desc)}) not optimal (should be 120-165)")
        
    if not canon:
        issues.append("Missing Canonical")
        
    if not og_image:
        issues.append("Missing og:image")
        
    if not twitter_card:
        issues.append("Missing twitter:card")
        
    if len(h1s) == 0:
        issues.append("Missing H1 tag")
    elif len(h1s) > 1:
        issues.append(f"Multiple H1 tags ({len(h1s)})")
        
    if not schemas:
        issues.append("Missing JSON-LD Schema")
    else:
        for idx, s in enumerate(schemas):
            s_clean = s.strip()
            if s_clean == '{}' or not s_clean:
                issues.append(f"Schema {idx+1} is empty")
                
    if issues:
        report.append(f"{rel}:\n  Title: {title}\n  Issues:\n" + "\n".join(f"    - {iss}" for iss in issues))

print(f"Checked {stats['files']} files. Found {len(report)} files with SEO issues.")
with open(os.path.join(base, 'scratch', 'seo_report.txt'), 'w', encoding='utf-8') as f:
    f.write(f"=== SEO REPORT: {stats['files']} files, {len(report)} with issues ===\n\n")
    for r in report:
        f.write(r + '\n\n')
print("Report saved to scratch/seo_report.txt")
