import os
import re
import json

def try_repair(json_str):
    # Try inserting a closing brace before the first trailing ']' that closes the FAQ mainEntity list
    # The broken pattern is typically:
    # "text": "..."
    # }
    # 
    # ]
    # }
    # ]
    # }
    #
    # We want to change the end from:
    # }
    # ]
    # }
    # ]
    # }
    #
    # to:
    # }
    # }
    # ]
    # }
    # ]
    # }
    
    # Let's search from the end for the closing pattern
    pattern = re.compile(r'\}\s*\]\s*\}\s*\]\s*\}\s*$', re.DOTALL)
    if pattern.search(json_str):
        repaired = pattern.sub('}\n      }\n    ]\n  }\n]\n}', json_str)
        try:
            json.loads(repaired)
            return repaired
        except Exception:
            pass
            
    # Try another common variant:
    # if it has a list of questions, and we have ... } } ] } ] }
    # Let's try matching a broader pattern:
    # We search for the last 'acceptedAnswer' block and check if it has a closing brace for the question.
    # A generic fallback is to count braces:
    # If open braces { count > close braces } count by exactly 1 in the mainEntity:
    # We can try to append a closing brace before the mainEntity closing bracket.
    return None

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print("Scanning for invalid JSON-LD schemas to repair...")
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'scratch' in dirs:
            dirs.remove('scratch')
            
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    fixed_count = 0
    for fp in html_files:
        rel_path = os.path.relpath(fp, root_dir)
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        pattern = re.compile(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.DOTALL | re.IGNORECASE)
        
        modified = False
        def repl(match):
            nonlocal modified
            tag_start = match.group(1)
            json_str = match.group(2).strip()
            tag_end = match.group(3)
            
            try:
                # Check if it parses
                json.loads(json_str)
                return match.group(0)
            except Exception:
                # Try to repair
                repaired = try_repair(json_str)
                if repaired:
                    modified = True
                    return f"{tag_start}\n{repaired}\n{tag_end}"
                else:
                    # Let's log if we couldn't repair it
                    return match.group(0)
                    
        new_content = pattern.sub(repl, content)
        if modified and new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Repaired JSON-LD in: {rel_path}")
            fixed_count += 1
            
    print(f"\nDone! Repaired JSON-LD in {fixed_count} files.")

if __name__ == '__main__':
    main()
