import os
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # 1. Fix padding collapses in button-shine <a> tags
    # Find all <a ... class="..." ...> elements
    # We want to replace classes that have py-4, py-3.5 etc but lack block/inline-block/flex/inline-flex/hidden
    # For simplicity, let's target the exact button classes used in the site:
    patterns = [
        (r'class="button-shine w-full text-center py-4', 'class="button-shine block w-full text-center py-4'),
        (r'class="button-shine w-full py-4 bg-primary', 'class="button-shine block w-full py-4 bg-primary'),
        (r'class="button-shine px-8 py-4 bg-primary', 'class="button-shine inline-block px-8 py-4 bg-primary'),
        (r'class="button-shine px-8 py-4 bg-\[#25D366\]', 'class="button-shine inline-block px-8 py-4 bg-[#25D366]'),
        (r'class="button-shine px-6 py-4 bg-primary', 'class="button-shine inline-block px-6 py-4 bg-primary'),
    ]
    
    for pat, rep in patterns:
        new_content, count = re.subn(pat, rep, content)
        if count > 0:
            content = new_content
            modified = True
            print(f"Fixed button padding: {pat} -> {rep} in {file_path}")
            
    # 2. Add linear-gradient fallback to any div using the primary-to-indigo gradient
    # Match: bg-gradient-to-r from-primary to-indigo-700
    # Make sure we don't duplicate the style attribute if it's already there
    gradient_pat = re.compile(r'(<div\s+[^>]*class="[^"]*bg-gradient-to-r from-primary to-indigo-700[^"]*"[^>]*>)')
    
    def add_style_fallback(match):
        tag = match.group(1)
        if 'style=' in tag:
            # If style already exists, don't overwrite but if it doesn't contain linear-gradient, append it
            if 'linear-gradient' not in tag:
                # Append to style attribute
                tag = re.sub(r'style="([^"]*)"', r'style="\1; background: linear-gradient(135deg, #4f17ce 0%, #31108c 100%);"', tag)
                return tag
            return tag
        else:
            # Insert style attribute
            # Insert before the closing '>' of the opening tag
            return tag[:-1] + ' style="background: linear-gradient(135deg, #4f17ce 0%, #31108c 100%);">'
            
    new_content, count = gradient_pat.subn(add_style_fallback, content)
    if count > 0:
        content = new_content
        modified = True
        print(f"Added gradient fallback to {count} divs in {file_path}")
        
    # Also support spelling variant: to-indigo-700 with text-centre / text-center
    # The regex already matches any class list containing 'bg-gradient-to-r from-primary to-indigo-700'
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    count = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                fix_file(file_path)
                count += 1
    print(f"Done! Scanned {count} files.")

if __name__ == '__main__':
    main()
