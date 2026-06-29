import os
import re
import json

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print("Correcting blog post author schemas across all markets...")
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'scratch' in dirs:
            dirs.remove('scratch')
            
        # Check if under 2025 or 2026 folder
        parts = os.path.relpath(root, root_dir).replace('\\', '/').split('/')
        if '2025' in parts or '2026' in parts:
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
                    
    updated_count = 0
    for fp in html_files:
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        pattern = re.compile(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.DOTALL | re.IGNORECASE)
        
        modified = False
        def repl(match):
            nonlocal modified
            tag_start = match.group(1)
            json_str = match.group(2).strip()
            tag_end = match.group(3)
            
            try:
                data = json.loads(json_str)
            except Exception:
                return match.group(0)
                
            changed = False
            
            def traverse_and_fix(item):
                nonlocal changed
                if isinstance(item, dict):
                    if item.get("@type") == "Article":
                        item["author"] = {
                            "@type": "Organization",
                            "name": "Hosterlo Editorial Team",
                            "url": "https://hosterlo.com/blog/"
                        }
                        changed = True
                    else:
                        for k, v in item.items():
                            traverse_and_fix(v)
                elif isinstance(item, list):
                    for v in item:
                        traverse_and_fix(v)
                        
            traverse_and_fix(data)
            
            if changed:
                modified = True
                new_json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
                return f"{tag_start}{new_json_str}{tag_end}"
                
            return match.group(0)
            
        new_content = pattern.sub(repl, content)
        
        if modified and new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed author schema in: {os.path.relpath(fp, root_dir)}")
            updated_count += 1
            
    print(f"\nDone! Corrected authors in {updated_count} blog post files.")

if __name__ == '__main__':
    main()
