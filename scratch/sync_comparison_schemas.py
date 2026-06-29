import os
import re
import json

def get_script_blocks(content):
    pattern = re.compile(r'<script\b[^>]*type="application/ld\+json"[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)
    return pattern.findall(content)

def remove_script_blocks(content):
    pattern = re.compile(r'\s*<script\b[^>]*type="application/ld\+json"[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)
    return pattern.sub('', content)

def localize_schema(schema_str, market, rel_path):
    # Adjust canonical domain paths in JSON
    schema_str = schema_str.replace('https://hosterlo.com/compare/', f'https://hosterlo.com/{market}/compare/')
    schema_str = schema_str.replace('https://hosterlo.com/alternatives/', f'https://hosterlo.com/{market}/alternatives/')
    
    # Adjust pricing and currency
    if market == 'uk':
        schema_str = schema_str.replace('4.08', '3.25')
        schema_str = schema_str.replace('USD', 'GBP')
        schema_str = schema_str.replace('$4.08', '£3.25')
        schema_str = schema_str.replace('+1 (618) 356-1311', '+44 7575 803760')
    elif market == 'pk':
        schema_str = schema_str.replace('4.08', '1150')
        schema_str = schema_str.replace('USD', 'PKR')
        schema_str = schema_str.replace('$4.08', 'Rs. 1,150')
        schema_str = schema_str.replace('+1 (618) 356-1311', '+92 3394437730')
    elif market == 'es':
        # ES keeps USD but updates page path
        schema_str = schema_str.replace('https://hosterlo.com/', 'https://hosterlo.com/es/')
        
    return schema_str

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print(f"Scanning for comparison and alternative schemas...")
    
    # We want to sync schemas for all pages under compare/ and alternatives/
    subdirs = ['compare', 'alternatives']
    
    sync_count = 0
    for subdir in subdirs:
        us_dir = os.path.join(root_dir, subdir)
        if not os.path.exists(us_dir):
            continue
            
        for root, dirs, files in os.walk(us_dir):
            for file in files:
                if file.endswith('.html'):
                    us_fp = os.path.join(root, file)
                    rel_path = os.path.relpath(us_fp, root_dir).replace('\\', '/')
                    
                    with open(us_fp, 'r', encoding='utf-8', errors='replace') as f:
                        us_content = f.read()
                        
                    us_scripts = get_script_blocks(us_content)
                    if not us_scripts:
                        continue
                        
                    # Sync to other markets
                    for market in ['uk', 'pk', 'es']:
                        market_fp = os.path.join(root_dir, market, rel_path)
                        if os.path.exists(market_fp):
                            with open(market_fp, 'r', encoding='utf-8', errors='replace') as f:
                                market_content = f.read()
                                
                            # Remove existing JSON-LD schemas
                            cleaned_content = remove_script_blocks(market_content)
                            
                            # Localize the US scripts
                            local_scripts = []
                            for script in us_scripts:
                                local_scripts.append(localize_schema(script, market, rel_path))
                            scripts_str = '\n'.join(local_scripts)
                            
                            # Inject into the head
                            head_match = re.search(r'<head\b[^>]*>', cleaned_content, re.IGNORECASE)
                            if head_match:
                                insert_pos = head_match.end()
                                new_content = (
                                    cleaned_content[:insert_pos] +
                                    "\n" + scripts_str +
                                    cleaned_content[insert_pos:]
                                )
                                
                                with open(market_fp, 'w', encoding='utf-8') as f:
                                    f.write(new_content)
                                print(f"Synced compare schema to: {market}/{rel_path}")
                                sync_count += 1
                                
    print(f"\nDone! Synced {sync_count} comparison/alternative schemas.")

if __name__ == '__main__':
    main()
