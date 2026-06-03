import os
import re

def modernize_headers():
    count_files = 0
    
    # Matching pattern for flat header style with dynamic whitespace handling
    pattern = r'<header class="sticky top-0 w-full z-50 bg-white/95 backdrop-blur-md border-b border-slate-200/50 shadow-sm">\s*<div class="max-w-\[1440px\] mx-auto px-6 h-\[80px\] flex items-center justify-between">'
    
    # Matching pattern in case max-w-[1280px] is still present in some untracked files
    pattern_1280 = r'<header class="sticky top-0 w-full z-50 bg-white/95 backdrop-blur-md border-b border-slate-200/50 shadow-sm">\s*<div class="max-w-\[1280px\] mx-auto px-6 h-\[80px\] flex items-center justify-between">'
    
    replacement = '<!-- TopNavBar -->\n<header class="sticky top-4 w-full z-50 px-4 sm:px-6 lg:px-8">\n    <div class="max-w-[1440px] mx-auto bg-white/95 backdrop-blur-md border border-slate-200/60 rounded-3xl sm:rounded-full px-6 sm:px-8 h-[80px] flex items-center justify-between shadow-lg shadow-indigo-900/5">'
    
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if file.endswith('.html') and file != 'index.html': # Update other pages only
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                modified = False
                
                # Check and replace
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    modified = True
                elif re.search(pattern_1280, content):
                    content = re.sub(pattern_1280, replacement, content)
                    modified = True
                
                # Also reduce logo size to match the premium bar profile (from w-[200px] to w-[185px] as on homepage)
                if modified and 'class="w-[200px] h-auto" src="/assets/logo.png"' in content:
                    content = content.replace('class="w-[200px] h-auto" src="/assets/logo.png"', 'class="w-[185px] h-auto" src="/assets/logo.png"')
                
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Modernized header in: {file_path}")
                    count_files += 1

    print(f"Completed! Modernized headers in {count_files} subpages.")

if __name__ == '__main__':
    modernize_headers()
