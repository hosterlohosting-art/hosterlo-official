import os

def localize_file(fp, replacements):
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Localized: {fp}")

def main():
    root_dir = r"d:\Hosterlo Official Site"
    
    # UK replacements
    uk_replacements = [
        # Canonical & URLs
        ('https://hosterlo.com/faq/', 'https://hosterlo.com/uk/faq/'),
        ('href="/faq/"', 'href="/uk/faq/"'),
        
        # Meta & Headers
        ('Hosterlo FAQs', 'Hosterlo UK FAQs'),
        ('$4.08/mo', '£3.25/mo'),
        ('$4.08/mo Website Launch Bundle', '£3.25/mo Website Launch Bundle'),
        ('for $4.08', 'for £3.25'),
        ('for $4.08/mo', 'for £3.25/mo'),
        ('just $4.08/mo', 'just £3.25/mo'),
        ('at $4.08/mo', 'at £3.25/mo'),
        ('$4.08 price', '£3.25 price'),
        ('The $4.08/mo price', 'The £3.25/mo price'),
        
        # Contact details
        ('+1 (618) 356-1311', '+44 7575 803760'),
        ('+16183561311', '447575803760'),
    ]
    localize_file(os.path.join(root_dir, 'uk', 'faq', 'index.html'), uk_replacements)
    
    # PK replacements
    pk_replacements = [
        # Canonical & URLs
        ('https://hosterlo.com/faq/', 'https://hosterlo.com/pk/faq/'),
        ('href="/faq/"', 'href="/pk/faq/"'),
        
        # Meta & Headers
        ('Hosterlo FAQs', 'Hosterlo Pakistan FAQs'),
        ('$4.08/mo', 'Rs. 1,150/mo'),
        ('$4.08/mo Website Launch Bundle', 'Rs. 1,150/mo Website Launch Bundle'),
        ('for $4.08', 'for Rs. 1,150'),
        ('for $4.08/mo', 'for Rs. 1,150/mo'),
        ('just $4.08/mo', 'just Rs. 1,150/mo'),
        ('at $4.08/mo', 'at Rs. 1,150/mo'),
        ('$4.08 price', 'Rs. 1,150 price'),
        ('The $4.08/mo price', 'The Rs. 1,150/mo price'),
        
        # Contact details
        ('+1 (618) 356-1311', '+92 3394437730'),
        ('+16183561311', '923394437730'),
    ]
    localize_file(os.path.join(root_dir, 'pk', 'faq', 'index.html'), pk_replacements)

if __name__ == '__main__':
    main()
