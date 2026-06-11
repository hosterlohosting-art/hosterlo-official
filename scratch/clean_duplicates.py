import os, glob, re

base = r'd:\Hosterlo Official Site'
stats = {'files': 0, 'cleaned': 0}
dry_run = False  # Set to False to write changes

for html in glob.glob(os.path.join(base, '**', '*.html'), recursive=True):
    if '.git' in html:
        continue
    rel = os.path.relpath(html, base)
    stats['files'] += 1
    
    with open(html, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    footer_end = content.find('</footer>')
    if footer_end == -1:
        continue
        
    # Search for back-to-top button after the footer
    b2t_pos = content.find('id="back-to-top"', footer_end)
    if b2t_pos == -1:
        continue
        
    # We found a duplicate back-to-top button after </footer>!
    # Backtrack to find <!-- Floating Elements --> or the start of the button tag
    start_tag_pos = content.rfind('<button', footer_end, b2t_pos)
    if start_tag_pos == -1:
        start_tag_pos = b2t_pos
        
    comment_pos = content.rfind('<!-- Floating Elements', footer_end, start_tag_pos)
    if comment_pos != -1 and (start_tag_pos - comment_pos) < 150:
        block_start = comment_pos
    else:
        block_start = start_tag_pos
        
    # Now find the end of the WhatsApp floating link after block_start
    wa_pos = content.find('wa.me/', block_start)
    if wa_pos == -1:
        # If no WhatsApp link, let's find the first </a> or </button> that ends this block
        # We can look for the next </a> or </button> within 500 chars
        block_end = content.find('</a>', b2t_pos)
        if block_end == -1:
            block_end = content.find('</button>', b2t_pos) + len('</button>')
        else:
            block_end += len('</a>')
    else:
        # WhatsApp link exists, find its closing </a> tag
        block_end = content.find('</a>', wa_pos)
        if block_end != -1:
            block_end += len('</a>')
        else:
            block_end = wa_pos + 200 # Fallback
            
    # Extract the block to be removed
    removed_block = content[block_start:block_end]
    print(f"File: {rel}")
    print(f"Removing duplicate block (chars {block_start} to {block_end}):")
    print("-" * 40)
    print(removed_block.strip())
    print("-" * 40)
    
    # Replace the duplicate block with whitespace
    new_content = content[:block_start] + "\n" + content[block_end:]
    
    if not dry_run:
        with open(html, 'w', encoding='utf-8') as f:
            f.write(new_content)
        stats['cleaned'] += 1

print(f"\nCompleted. Checked {stats['files']} files, cleaned {stats['cleaned']} files.")
