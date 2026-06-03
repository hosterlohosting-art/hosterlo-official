import os

def align_branding():
    count_files = 0
    count_replacements = 0
    
    # Walk through the Hosterlo project directory
    for root, dirs, files in os.walk('.'):
        # Skip internal git directories
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                modified = False
                
                # 1. Replace 1280px container limits with 1440px layout width
                if 'max-w-[1280px]' in content:
                    content = content.replace('max-w-[1280px]', 'max-w-[1440px]')
                    modified = True
                    
                # 2. Update Tailwind configuration spacing token
                if '"container-max": "1280px"' in content:
                    content = content.replace('"container-max": "1280px"', '"container-max": "1440px"')
                    modified = True
                
                # 3. Clean Google AI / Gemini text tags in tabs if present
                if 'google-ai' in content and 'Google AI' in content:
                    content = content.replace('Google AI', 'Gemini Pro')
                    modified = True
                
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Aligned branding in: {file_path}")
                    count_files += 1

    print(f"Completed! Aligned branding in {count_files} HTML pages.")

if __name__ == '__main__':
    align_branding()
