import os
import json
import re

def verify_address_substitution():
    old_address = "3338 S National Ave"
    offending_files = []
    
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'scratch' in dirs:
            dirs.remove('scratch')
            
        for file in files:
            if file.endswith('.html') or file.endswith('.txt') or file.endswith('.xml') or file.endswith('.md'):
                # Skip audit files and this verification script itself
                if 'audit' in file.lower() or 'verify_seo' in file.lower():
                    continue
                    
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if old_address in content:
                    offending_files.append(file_path)
                    
    if offending_files:
        print("FAIL: Old address still found in the following files:")
        for f_path in offending_files:
            print(f" - {f_path}")
        return False
    else:
        print("PASS: No occurrences of the old address found in production files!")
        return True

def verify_json_schemas():
    files_to_check = [
        "index.html",
        "services/index.html",
        "services/web-development/index.html",
        "services/saas-development/index.html",
        "services/frontend-development/index.html",
        "services/backend-development/index.html",
        "services/ui-ux-design/index.html",
        "services/mobile-app-development/index.html",
        "services/api-development/index.html",
        "services/website-maintenance/index.html"
    ]
    
    all_passed = True
    for file in files_to_check:
        file_path = os.path.join(os.getcwd(), file)
        if not os.path.exists(file_path):
            print(f"FAIL: File not found {file}")
            all_passed = False
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all JSON-LD blocks
        matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        if not matches:
            print(f"WARNING: No JSON-LD schema found in {file}")
            continue
            
        for idx, match in enumerate(matches):
            try:
                json.loads(match.strip())
                print(f"PASS: Valid JSON schema block {idx+1} in {file}")
            except Exception as e:
                print(f"FAIL: Schema block {idx+1} in {file} is invalid JSON: {e}")
                all_passed = False
                
    return all_passed

def main():
    address_ok = verify_address_substitution()
    schema_ok = verify_json_schemas()
    
    if address_ok and schema_ok:
        print("\nALL SEO AND ADDRESS VERIFICATIONS PASSED SUCCESSFULLY!")
    else:
        print("\nSOME VERIFICATIONS FAILED. PLEASE CORRECT THEM.")

if __name__ == '__main__':
    main()
