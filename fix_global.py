import re, os

ROOT = r'd:\Hosterlo Official Site'

# Global text replacements (old -> new)
REPLACEMENTS = [
    # WhatsApp links
    ('wa.me/442046155575', 'wa.me/923394437730'),
    # Phone in href
    ('tel:+442046155575', 'tel:+923394437730'),
    # Phone as text (various formats)
    ('+44 20 4615 5575', '+92 339 443 7730'),
    ('020 4615 5575', '+92 339 443 7730'),
    ('Call: 020 4615 5575', 'WhatsApp: +92 339 443 7730'),
    # Uptime claim
    ('99.99% uptime', '99.9% uptime commitment'),
    ('99.99% Uptime', '99.9% Uptime Commitment'),
    # Remove AI clichés
    ('revolutionary', 'modern'),
    ('game-changing', 'practical'),
    ('unlock your potential', 'grow your online presence'),
    ('Revolutionize', 'Improve'),
    ('seamless digital transformation', 'a smooth website launch'),
    ('Seamless', 'Simple'),
]

count = 0
files_changed = 0

for root, dirs, files in os.walk(ROOT):
    # Skip git directory
    dirs[:] = [d for d in dirs if d != '.git']
    
    for file in files:
        if not file.endswith(('.html', '.txt', '.xml')):
            continue
        
        fp = os.path.join(root, file)
        try:
            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            original = content
            for old, new in REPLACEMENTS:
                content = content.replace(old, new)
            
            if content != original:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_changed += 1
                print(f'Updated: {os.path.relpath(fp, ROOT)}')
        except Exception as e:
            print(f'ERROR {fp}: {e}')

print(f'\nDone! Updated {files_changed} files.')
