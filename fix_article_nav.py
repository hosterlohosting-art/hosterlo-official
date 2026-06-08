import re, os

with open('index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

header_start = idx_content.find('<!-- TopNavBar -->')
header_end_marker = idx_content.find('<!-- Hero Section -->')
header_block = idx_content[header_start:header_end_marker].strip()

footer_start = idx_content.find('<!-- Footer: Standardized White Background, Black Text -->')
footer_end = idx_content.rfind('</footer>') + len('</footer>')
footer_block = idx_content[footer_start:footer_end].strip()

articles = [
    '2026/06/03/bluehost-vs-siteground-vs-hosterlo-2026/index.html',
    '2026/06/03/cpanel-tutorial-for-beginners-complete-guide/index.html',
    '2026/06/03/ssl-certificate-guide-website-security-2026/index.html',
    '2026/06/03/why-is-my-website-down-common-causes-and-fixes/index.html',
]

for fp in articles:
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        sub = f.read()

    sub_header_start = sub.find('<header')
    # Try hero banner markers
    hero_pos = sub.find('<!-- Hero Banner -->')
    if hero_pos == -1:
        hero_pos = sub.find('<!-- Article Hero -->')
    if hero_pos == -1:
        # Find the first big div section after the header closes
        header_end_in_sub = sub.find('</header>', sub_header_start)
        if header_end_in_sub != -1:
            hero_pos = header_end_in_sub + len('</header>')

    if sub_header_start != -1 and hero_pos != -1:
        new_content = sub[:sub_header_start] + header_block + '\n' + sub[hero_pos:]

        sub_footer_start = new_content.find('<footer')
        sub_footer_end = new_content.rfind('</footer>') + len('</footer>')
        if sub_footer_start != -1 and sub_footer_end > sub_footer_start:
            new_content = new_content[:sub_footer_start] + footer_block + '\n' + new_content[sub_footer_end:]

        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Synced:', fp)
    else:
        print('SKIP:', fp, 'header_start:', sub_header_start, 'hero_pos:', hero_pos)
