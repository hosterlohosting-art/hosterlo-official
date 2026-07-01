import os
import shutil

def localize_content(content):
    # 1. Canonical and link mapping
    content = content.replace("https://hosterlo.com/uk/", "https://hosterlo.com/ph/")
    content = content.replace("href=\"/uk/", "href=\"/ph/")
    content = content.replace("href='/uk/", "href='/ph/")
    content = content.replace("\"/uk/", "\"/ph/")
    
    # 2. Pricing & Currency replacement
    content = content.replace("£3.25/mo", "₱239/mo")
    content = content.replace("£3.25", "₱239")
    content = content.replace("GBP", "PHP")
    content = content.replace("priceCurrency\":\"GBP\"", "priceCurrency\":\"PHP\"")
    content = content.replace("price\":\"3.25\"", "price\":\"239\"")
    content = content.replace("£", "₱")
    
    # 3. Market Name replacements (Case Sensitive/Varied)
    content = content.replace("UK Web Hosting", "Philippines Web Hosting")
    content = content.replace("Web Hosting UK", "Web Hosting Philippines")
    content = content.replace("web hosting UK", "web hosting Philippines")
    content = content.replace("WordPress hosting UK", "WordPress hosting Philippines")
    content = content.replace("UK Shared Hosting", "Philippines Shared Hosting")
    content = content.replace("UK shared hosting", "Philippines shared hosting")
    content = content.replace("UK business", "Philippine business")
    content = content.replace("in the UK", "in the Philippines")
    content = content.replace("UK flat-rate", "Philippines flat-rate")
    content = content.replace("UK customer", "Philippine customer")
    content = content.replace("UK market", "Philippine market")
    content = content.replace("UK servers", "Philippine servers")
    
    # 4. Meta and Schema fixes
    content = content.replace("en_GB", "en_PH")
    content = content.replace("en-gb", "en-ph")
    
    return content

def main():
    root_dir = r"d:\Hosterlo Official Site"
    uk_dir = os.path.join(root_dir, "uk")
    ph_dir = os.path.join(root_dir, "ph")
    
    print("Cloning and localizing UK templates for the Philippines (ph)...")
    
    if os.path.exists(ph_dir):
        print("PH directory already exists. Overwriting HTML pages...")
        
    copied_count = 0
    for root, dirs, files in os.walk(uk_dir):
        # Calculate relative path from uk_dir
        rel_path = os.path.relpath(root, uk_dir)
        if rel_path == '.':
            target_folder = ph_dir
        else:
            target_folder = os.path.join(ph_dir, rel_path)
            
        os.makedirs(target_folder, exist_ok=True)
        
        for file in files:
            if file.endswith('.html'):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(target_folder, file)
                
                with open(src_file, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    
                localized = localize_content(content)
                
                with open(dest_file, 'w', encoding='utf-8') as f:
                    f.write(localized)
                
                copied_count += 1
                
    print(f"\nSuccessfully cloned and localized {copied_count} files to /ph/.")

if __name__ == '__main__':
    main()
