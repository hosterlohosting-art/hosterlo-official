import os
import glob
import re

base_dir = r"d:\Hosterlo Official Site"

# The 10 pages that will exist in Spanish (/es/)
es_pages = [
    "index.html",
    "hosting/index.html",
    "hosting/shared-hosting/index.html",
    "hosting/wordpress-hosting/index.html",
    "hosting/business-email/index.html",
    "domains/index.html",
    "about-hosterlo/index.html",
    "contact-us/index.html",
    "pricing/index.html",
    "faq/index.html"
]

def get_slug(rel_path):
    url_path = rel_path.replace("\\", "/")
    if url_path.endswith("index.html"):
        url_path = url_path[:-10] # remove index.html
    return url_path

def main():
    # 1. Collect all root HTML files
    root_files = []
    for file in glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True):
        if ".git" in file or "scratch" in file or "ai-article-writer" in file:
            continue
        # Check if it's in a subdirectory like uk/, pk/, es/
        rel = os.path.relpath(file, base_dir)
        if rel.startswith("uk") or rel.startswith("pk") or rel.startswith("es"):
            continue
        if rel == "404.html":
            continue
        root_files.append(rel)

    print(f"Found {len(root_files)} root pages to check.")

    for rel_path in root_files:
        slug = get_slug(rel_path)
        
        # Check alternates
        alternates = {
            "en-us": f"https://hosterlo.com/{slug}",
            "x-default": f"https://hosterlo.com/{slug}"
        }

        # Check UK
        uk_path = os.path.join(base_dir, "uk", rel_path)
        if os.path.exists(uk_path):
            alternates["en-gb"] = f"https://hosterlo.com/uk/{slug}"

        # Check PK
        pk_path = os.path.join(base_dir, "pk", rel_path)
        if os.path.exists(pk_path):
            alternates["en-pk"] = f"https://hosterlo.com/pk/{slug}"

        # Check ES (we check if it's in our es_pages list since we might run this script before creating the files)
        norm_path = rel_path.replace("\\", "/")
        if norm_path in es_pages:
            alternates["es"] = f"https://hosterlo.com/es/{slug}"

        # If there are no actual alternates (only en-us and x-default), then no hreflang alternate links are strictly needed
        # But if there's at least one regional alternate, we apply hreflangs to all existing versions of this page.
        if len(alternates) > 2:
            print(f"Applying hreflangs for /{slug} (Alternates: {list(alternates.keys())})")
            
            # Apply to root file
            apply_hreflangs(os.path.join(base_dir, rel_path), alternates)

            # Apply to UK file if it exists
            if os.path.exists(uk_path):
                apply_hreflangs(uk_path, alternates)

            # Apply to PK file if it exists
            if os.path.exists(pk_path):
                apply_hreflangs(pk_path, alternates)

            # Apply to ES file if it exists (in case we run this after files are created)
            es_path = os.path.join(base_dir, "es", rel_path)
            if os.path.exists(es_path):
                apply_hreflangs(es_path, alternates)
        else:
            # Clean up any old hreflang tags if they exist and no alternates are left
            clean_hreflangs(os.path.join(base_dir, rel_path))

def apply_hreflangs(filepath, alternates):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # remove existing hreflang links
    content = re.sub(r'\s*<link[^>]*hreflang="[^"]*"[^>]*>', '', content)

    # build block
    lines = []
    # Sort keys for consistent ordering
    for lang in sorted(alternates.keys()):
        lines.append(f'    <link rel="alternate" hreflang="{lang}" href="{alternates[lang]}" />')
    
    hreflang_block = "\n" + "\n".join(lines) + "\n"

    # insert right after <head>
    head_match = re.search(r'(<head[^>]*>)', content, re.IGNORECASE)
    if head_match:
        pos = head_match.end()
        new_content = content[:pos] + hreflang_block + content[pos:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

def clean_hreflangs(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # remove existing hreflang links
    cleaned = re.sub(r'\s*<link[^>]*hreflang="[^"]*"[^>]*>', '', content)
    if cleaned != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)

if __name__ == "__main__":
    main()
