#!/usr/bin/env python3
"""quick_bug_scan.py — Scans all HTML files for common bugs."""
import os, glob, re

base = r'd:\Hosterlo Official Site'
issues = []
stats = {'files': 0}

for html in glob.glob(os.path.join(base, '**', '*.html'), recursive=True):
    if '.git' in html:
        continue
    rel = os.path.relpath(html, base)
    stats['files'] += 1

    with open(html, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Duplicate IDs
    for id_name in ['back-to-top', 'mobile-menu-open', 'mobile-menu-close',
                    'mobile-menu-overlay', 'cookie-consent-banner', 'progress-bar']:
        count = content.count(f'id="{id_name}"')
        if count > 1:
            issues.append(f'[DUPE_ID] {rel}: id="{id_name}" x{count}')

    # Duplicate scripts
    for script in ['aos@next', 'tailwindcss.com', 'Material+Symbols', 'fonts.googleapis.com']:
        count = content.count(script)
        if count > 1:
            issues.append(f'[DUPE_SCRIPT] {rel}: {script[:40]} x{count}')

    # Duplicate structural tags
    for tag in ['</body>', '</footer>', '</main>', '<header', '<footer']:
        count = content.count(tag)
        if count > 1:
            issues.append(f'[DUPE_TAG] {rel}: {tag} x{count}')

    # Missing canonical
    if '<link rel="canonical"' not in content:
        issues.append(f'[NO_CANONICAL] {rel}')

    # Missing meta description
    if 'name="description"' not in content:
        issues.append(f'[NO_META_DESC] {rel}')

    # opacity-0 on html tag
    if re.search(r'<html[^>]+opacity-0', content):
        issues.append(f'[FOUC_BUG] {rel}: html tag has opacity-0')

    # H1 count
    h1_count = len(re.findall(r'<h1[\s>]', content, re.IGNORECASE))
    if h1_count == 0:
        issues.append(f'[NO_H1] {rel}')
    elif h1_count > 1:
        issues.append(f'[MULTI_H1] {rel}: {h1_count} h1s')

    # Missing og:image
    if 'property="og:image"' not in content and 'og:image' not in content:
        issues.append(f'[NO_OG_IMAGE] {rel}')

    # Missing twitter card
    if 'twitter:card' not in content:
        issues.append(f'[NO_TWITTER_CARD] {rel}')

    # Missing JSON-LD
    if 'application/ld+json' not in content:
        issues.append(f'[NO_SCHEMA] {rel}')

    # Check img alt attributes
    imgs = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
    bad_alts = [i for i in imgs if 'alt=""' in i or ('alt' not in i and 'data-src' not in i)]
    if bad_alts:
        issues.append(f'[BAD_ALT] {rel}: {len(bad_alts)} img(s) missing/empty alt')

    # Duplicate floating buttons
    wa_count = content.count('wa.me/923394437730')
    if wa_count > 1:
        issues.append(f'[DUPE_WA_BTN] {rel}: WhatsApp float x{wa_count}')

    phone_float = content.count('fixed bottom-28')
    if phone_float > 1:
        issues.append(f'[DUPE_PHONE_BTN] {rel}: Phone float x{phone_float}')

print(f'=== SCAN: {stats["files"]} files, {len(issues)} issues ===\n')
# Group by type
by_type = {}
for iss in issues:
    t = iss.split(']')[0] + ']'
    by_type.setdefault(t, []).append(iss)

for t, items in sorted(by_type.items()):
    print(f'\n--- {t} ({len(items)}) ---')
    for i in items:
        print(f'  {i}')
