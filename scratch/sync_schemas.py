import os
import re
import json

def update_organization(org, market):
    # Set default fields
    org["name"] = "Hosterlo"
    org["url"] = "https://hosterlo.com/"
    
    # Configure contactPoint based on market
    if market == 'uk':
        org["contactPoint"] = {
            "@type": "ContactPoint",
            "telephone": "+44 7575 803760",
            "contactType": "customer support",
            "availableLanguage": ["English"],
            "areaServed": {"@type": "Country", "name": "United Kingdom"}
        }
    elif market == 'pk':
        org["contactPoint"] = {
            "@type": "ContactPoint",
            "telephone": "+92 3394437730",
            "contactType": "customer support",
            "availableLanguage": ["English"],
            "areaServed": {"@type": "Country", "name": "Pakistan"}
        }
    else: # us, es, etc.
        org["contactPoint"] = {
            "@type": "ContactPoint",
            "telephone": "+1 (618) 356-1311",
            "contactType": "customer support",
            "availableLanguage": ["English"],
            "areaServed": {"@type": "Country", "name": "United States"}
        }
        
    # Standard subOrganization structure
    org["subOrganization"] = [
        {
            "@type": "Organization",
            "name": "Hosterlo LLC",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "16192 Coastal Highway",
                "addressLocality": "Lewes",
                "addressRegion": "DE",
                "postalCode": "19958",
                "addressCountry": "US"
            },
            "telephone": "+1 (618) 356-1311"
        },
        {
            "@type": "Organization",
            "name": "Hosterlo Ltd",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "1A North Rd",
                "addressLocality": "Woking",
                "postalCode": "GU21 5DS",
                "addressCountry": "GB"
            },
            "telephone": "+44 7575 803760"
        },
        {
            "@type": "Organization",
            "name": "Hosterlo Pakistan",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "4th Floor Venture Drive, Model Town",
                "addressLocality": "Lahore",
                "addressCountry": "PK"
            },
            "telephone": "+92 3394437730"
        }
    ]

def update_generic_area_served(item, market):
    country_map = {
        'us': {"@type": "Country", "name": "United States"},
        'uk': {"@type": "Country", "name": "United Kingdom"},
        'pk': {"@type": "Country", "name": "Pakistan"},
        'es': {"@type": "Country", "name": "Worldwide"}
    }
    target_country = country_map.get(market, {"@type": "Country", "name": "United States"})
    
    if "areaServed" in item:
        item["areaServed"] = target_country

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print(f"Scanning root directory for schema updates: {root_dir}")
    
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
        norm_path = os.path.relpath(fp, root_dir).replace('\\', '/')
        parts = norm_path.split('/')
        if parts[0] in ['uk', 'pk', 'es']:
            market = parts[0]
        else:
            market = 'us'
            
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        # Find all script blocks
        pattern = re.compile(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.DOTALL | re.IGNORECASE)
        
        modified = False
        def repl(match):
            nonlocal modified
            tag_start = match.group(1)
            json_str = match.group(2).strip()
            tag_end = match.group(3)
            
            try:
                data = json.loads(json_str)
            except Exception as e:
                return match.group(0)
                
            changed = False
            
            # Helper to recursively traverse and update keys
            def traverse_and_update(item):
                nonlocal changed
                if isinstance(item, dict):
                    # Check if Organization
                    if item.get("@type") == "Organization":
                        update_organization(item, market)
                        changed = True
                        # Do not traverse deeper into the same organization to avoid recursion loops
                        return
                    else:
                        # Update areaServed on generic items like Service, Offer, WebPage
                        if "areaServed" in item:
                            update_generic_area_served(item, market)
                            changed = True
                            
                    for k, v in item.items():
                        traverse_and_update(v)
                elif isinstance(item, list):
                    for v in item:
                        traverse_and_update(v)
                        
            traverse_and_update(data)
            
            if changed:
                modified = True
                new_json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
                return f"{tag_start}{new_json_str}{tag_end}"
            
            return match.group(0)
            
        new_content = pattern.sub(repl, content)
        
        if modified and new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated schema in: {os.path.relpath(fp, root_dir)}")
            updated_count += 1
            
    print(f"\nDone! Updated schemas in {updated_count} files.")

if __name__ == '__main__':
    main()
