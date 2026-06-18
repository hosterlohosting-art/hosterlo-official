import os
import glob
import re
import json

base_dir = r"d:\Hosterlo Official Site"
html_files = []

for file in glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True):
    if ".git" in file or "scratch" in file or "ai-article-writer" in file:
        continue
    rel = os.path.relpath(file, base_dir)
    if rel == "404.html":
        continue
    url_path = rel.replace("\\", "/")
    if url_path.endswith("index.html"):
        url_path = url_path[:-10] # remove index.html
    url = "https://hosterlo.com/" + url_path
    html_files.append((url, file))

results = []
for url, filepath in html_files:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else ""
    
    # Meta Description
    desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="(.*?)"', content, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta[^>]*content="(.*?)"[^>]*name="description"', content, re.IGNORECASE)
    desc = desc_match.group(1).strip() if desc_match else ""
    
    # Determine type/category based on URL
    url_lower = url.lower()
    page_type = "webpage"
    if "/services/" in url_lower:
        page_type = "service"
    elif "/compare/" in url_lower:
        page_type = "comparison"
    elif "/alternatives/" in url_lower:
        page_type = "alternative"
    elif "/blog" in url_lower or re.search(r'/\d{4}/\d{2}/\d{2}/', url_lower):
        page_type = "article"
    elif "/legal/" in url_lower or "policy" in url_lower or "terms" in url_lower:
        page_type = "legal"
    elif "lookup" in url_lower or "tools" in url_lower:
        page_type = "tool"
    elif "/uk/" in url_lower:
        page_type = "uk-market"
    elif "/pk/" in url_lower:
        page_type = "pk-market"
    elif "/es/" in url_lower:
        page_type = "es-market"
    elif "get-a-quote" in url_lower:
        page_type = "contact"
    elif "faq" in url_lower:
        page_type = "support"
    elif "support" in url_lower:
        page_type = "support"
    
    results.append({
        "url": url,
        "title": title,
        "description": desc,
        "type": page_type
    })

results.sort(key=lambda x: x["url"])

with open(os.path.join(base_dir, "scratch", "extracted_metadata.json"), 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f"Extracted metadata for {len(results)} pages.")
