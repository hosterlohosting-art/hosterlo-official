import os
import re

style_block = """    <style>
        /* Prevent FOUT (Flash of Unstyled Icons) */
        .material-symbols-outlined {
            display: inline-block !important;
            width: 1em !important;
            height: 1em !important;
            overflow: hidden !important;
            white-space: nowrap !important;
            word-wrap: normal !important;
            direction: ltr !important;
        }
    </style>
</head>"""

def re_replace_head(content, style_block):
    pattern = re.compile(r'</head>', re.IGNORECASE)
    return pattern.sub(style_block, content, count=1)

count = 0
for root, dirs, files in os.walk('.'):
    # Skip git directory
    if '.git' in dirs:
        dirs.remove('.git')
        
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
                
            if '/* Prevent FOUT (Flash of Unstyled Icons) */' not in content:
                new_content = re_replace_head(content, style_block)
                if new_content != content:
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Injected FOUT prevention style in: {file_path}")
                        count += 1
                    except Exception as e:
                        print(f"Error writing {file_path}: {e}")

print(f"Successfully processed and fixed FOUT in {count} HTML files.")
