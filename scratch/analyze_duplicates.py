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
        lines = f.readlines()
    
    content = "".join(lines)
    
    # Check for duplicate IDs
    for id_name in ['back-to-top', 'mobile-menu-open', 'mobile-menu-close',
                    'mobile-menu-overlay', 'cookie-consent-banner', 'progress-bar']:
        matches = [idx+1 for idx, l in enumerate(lines) if f'id="{id_name}"' in l]
        if len(matches) > 1:
            report.append(f"[DUPE_ID] {rel}: id=\"{id_name}\" on lines {matches}")
            
    # Check for duplicate floating button HTML blocks
    wa_floats = [idx+1 for idx, l in enumerate(lines) if 'fixed bottom-6' in l and 'wa.me' in l]
    if len(wa_floats) > 1:
        report.append(f"[DUPE_WA_FLOAT] {rel}: WhatsApp float on lines {wa_floats}")
        
    phone_floats = [idx+1 for idx, l in enumerate(lines) if 'fixed bottom-28' in l and 'tel:' in l]
    if len(phone_floats) > 1:
        report.append(f"[DUPE_PHONE_FLOAT] {rel}: Phone float on lines {phone_floats}")
        
    b2t_floats = [idx+1 for idx, l in enumerate(lines) if 'id="back-to-top"' in l]
    if len(b2t_floats) > 1:
        report.append(f"[DUPE_B2T_FLOAT] {rel}: Back-to-top float on lines {b2t_floats}")

    # Check duplicate tags
    for tag in ['</body>', '</html>', '</footer>', '</main>', '<header', '<footer']:
        matches = [idx+1 for idx, l in enumerate(lines) if tag in l]
        if len(matches) > 1:
            report.append(f"[DUPE_TAG] {rel}: {tag} on lines {matches}")
            
    # Check duplicate scripts
    for script in ['aos.js', 'tailwindcss.com', 'Material+Symbols', 'fonts.googleapis.com', 'aos@next']:
        matches = [idx+1 for idx, l in enumerate(lines) if script in l]
        if len(matches) > 1:
            report.append(f"[DUPE_SCRIPT] {rel}: {script} on lines {matches}")

with open(os.path.join(base, 'scratch', 'duplicate_issues.txt'), 'w', encoding='utf-8') as f:
    f.write(f"=== DUPLICATE ANALYSIS: {stats['files']} files, {len(report)} issues ===\n\n")
    for r in report:
        f.write(r + '\n')
print(f"Analysis written to scratch/duplicate_issues.txt. Found {len(report)} issues.")
