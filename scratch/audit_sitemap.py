import os
import glob
import xml.etree.ElementTree as ET

base_dir = r"d:\Hosterlo Official Site"
sitemaps = [
    os.path.join(base_dir, "sitemap.xml"),
    os.path.join(base_dir, "page-sitemap.xml")
]

# 1. Collect all valid HTML files
html_files = []
for file in glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True):
    if ".git" in file or "scratch" in file or "ai-article-writer" in file:
        continue
    rel = os.path.relpath(file, base_dir)
    if rel == "404.html":
        continue
    # Standardize url format
    url_path = rel.replace("\\", "/")
    if url_path.endswith("index.html"):
        url_path = url_path[:-10] # remove index.html
    url = "https://hosterlo.com/" + url_path
    html_files.append((url, rel))

# 2. Parse existing urls in sitemaps
indexed_urls = set()
for sm in sitemaps:
    if not os.path.exists(sm):
        print(f"Sitemap {sm} does not exist!")
        continue
    try:
        # Simple string search or xml parse
        with open(sm, 'r', encoding='utf-8') as f:
            content = f.read()
            # extract all <loc>contents</loc>
            import re
            locs = re.findall(r'<loc>(.*?)</loc>', content)
            for loc in locs:
                indexed_urls.add(loc.strip())
    except Exception as e:
        print(f"Error reading sitemap {sm}: {e}")

# 3. Compare
missing = []
for url, rel in html_files:
    # check both with and without trailing slash
    url_alt = url + "/" if not url.endswith("/") else url[:-1]
    if url not in indexed_urls and url_alt not in indexed_urls:
        missing.append((url, rel))

print(f"Total HTML files found in site: {len(html_files)}")
print(f"Total unique URLs indexed in sitemaps: {len(indexed_urls)}")
print(f"Total missing URLs from sitemaps: {len(missing)}")

if missing:
    print("\nMissing URLs:")
    for url, rel in missing:
        print(f"  - {url} ({rel})")
else:
    print("\nAll URLs are fully represented in the sitemaps!")
