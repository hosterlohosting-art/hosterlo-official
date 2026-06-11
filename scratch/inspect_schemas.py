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
        
    # Find all type="application/ld+json" script tags
    pattern = re.compile(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
    for idx, match in enumerate(pattern.finditer(content)):
        schema_text = match.group(1).strip()
        if schema_text == '{}' or not schema_text:
            report.append(f"{rel}: empty schema at occurrence {idx+1}")
        else:
            # Let's check if it's valid JSON
            import json
            try:
                data = json.loads(schema_text)
            except Exception as e:
                report.append(f"{rel}: invalid JSON in schema {idx+1}: {e}")

print(f"Checked {stats['files']} files. Found {len(report)} issues:")
for r in report:
    print(f"  {r}")
with open(os.path.join(base, 'scratch', 'schema_issues.txt'), 'w', encoding='utf-8') as f:
    f.write("\n".join(report))
