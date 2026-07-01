import os
import re
from PIL import Image

def convert_png_to_webp(assets_dir):
    print("Scanning assets for PNG files to convert...")
    png_files = [f for f in os.listdir(assets_dir) if f.lower().endswith('.png') and f.lower() not in ['logo.png', 'favicon.png']]
    
    converted = {}
    for filename in png_files:
        png_path = os.path.join(assets_dir, filename)
        base_name, _ = os.path.splitext(filename)
        webp_filename = f"{base_name}.webp"
        webp_path = os.path.join(assets_dir, webp_filename)
        
        # Keep track of mapping
        converted[filename] = webp_filename
        
        if os.path.exists(webp_path):
            # If webp already exists, we skip unless PNG is newer
            if os.path.getmtime(png_path) <= os.path.getmtime(webp_path):
                continue
                
        try:
            with Image.open(png_path) as img:
                # Convert to RGB if RGBA/P to save space, but preserve transparency if needed
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    # Save as WebP keeping transparency
                    img.save(webp_path, 'WEBP', quality=82, method=6)
                else:
                    img.convert('RGB').save(webp_path, 'WEBP', quality=82, method=6)
            print(f"Converted: {filename} -> {webp_filename} (Saved {os.path.getsize(png_path) - os.path.getsize(webp_path)} bytes)")
        except Exception as e:
            print(f"Error converting {filename}: {e}")
            
    return converted

def update_html_references(root_dir, converted_map):
    print("Updating image references in HTML files...")
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'scratch' in dirs:
            dirs.remove('scratch')
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    updated_count = 0
    for fp in html_files:
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        original = content
        for png_name, webp_name in converted_map.items():
            # Match both relative and absolute paths, e.g. assets/filename.png, /assets/filename.png, etc.
            # We escape the filename for safe regex search
            escaped_png = re.escape(png_name)
            # Find any references to the PNG name in quotes or URLs
            pattern = re.compile(rf'assets/{escaped_png}', re.IGNORECASE)
            content = pattern.sub(f'assets/{webp_name}', content)
            
        if content != original:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f"Updated references in: {os.path.relpath(fp, root_dir)}")
            
    print(f"Done updating references in {updated_count} HTML files.")

def main():
    root_dir = r"d:\Hosterlo Official Site"
    assets_dir = os.path.join(root_dir, "assets")
    
    # 1. Convert PNGs
    converted_map = convert_png_to_webp(assets_dir)
    
    # 2. Update HTML files
    if converted_map:
        update_html_references(root_dir, converted_map)
    else:
        print("No new conversions performed.")

if __name__ == '__main__':
    main()
