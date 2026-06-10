import os
import re

tailwind_config_code = """
    <script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "secondary-container": "#6860ef",
                    "surface-container-high": "#dee8ff",
                    "surface-dim": "#cfdaf2",
                    "surface-variant": "#d8e3fb",
                    "surface-container-low": "#f0f3ff",
                    "secondary": "#4e45d5",
                    "tertiary-container": "#596267",
                    "on-tertiary-fixed": "#141d21",
                    "surface-tint": "#6439e3",
                    "surface-container-lowest": "#ffffff",
                    "on-tertiary-fixed-variant": "#3f484d",
                    "on-error": "#ffffff",
                    "outline": "#797487",
                    "surface-container-highest": "#d8e3fb",
                    "background": "#f9f9ff",
                    "primary": "#4f17ce",
                    "on-primary": "#ffffff",
                    "on-background": "#111c2d",
                    "tertiary-fixed": "#dbe4ea",
                    "tertiary-fixed-dim": "#bfc8ce",
                    "primary-container": "#673de6",
                    "inverse-on-surface": "#ecf1ff",
                    "inverse-surface": "#263143",
                    "primary-fixed-dim": "#ccbeff",
                    "on-primary-fixed-variant": "#4c10cc",
                    "on-secondary-fixed": "#100069",
                    "error": "#ba1a1a",
                    "inverse-primary": "#ccbeff",
                    "surface-bright": "#f9f9ff",
                    "on-secondary": "#ffffff",
                    "on-primary-container": "#e1d7ff",
                    "on-secondary-fixed-variant": "#372abf",
                    "on-error-container": "#93000a",
                    "on-secondary-container": "#fffbff",
                    "on-primary-fixed": "#1e0060",
                    "tertiary": "#414a4f",
                    "on-surface": "#111c2d",
                    "primary-fixed": "#e7deff",
                    "on-tertiary-container": "#d4dde3",
                    "surface": "#f9f9ff",
                    "secondary-fixed-dim": "#c3c0ff",
                    "surface-container": "#e7eeff",
                    "on-tertiary": "#ffffff",
                    "outline-variant": "#cac3d8",
                    "on-surface-variant": "#484455",
                    "secondary-fixed": "#e3dfff",
                    "error-container": "#ffdad6"
            },
            "borderRadius": {
                    "DEFAULT": "0.25rem",
                    "lg": "0.5rem",
                    "xl": "0.75rem",
                    "full": "9999px"
            },
            "spacing": {
                    "md": "24px",
                    "xs": "4px",
                    "lg": "48px",
                    "gutter": "24px",
                    "base": "8px",
                    "sm": "12px",
                    "container-max": "1440px",
                    "xl": "80px"
            },
            "fontFamily": {
                    "h3": ["Outfit", "sans-serif"],
                    "body-sm": ["Plus Jakarta Sans", "sans-serif"],
                    "body-md": ["Plus Jakarta Sans", "sans-serif"],
                    "h1": ["Outfit", "sans-serif"],
                    "body-lg": ["Plus Jakarta Sans", "sans-serif"],
                    "label-caps": ["Plus Jakarta Sans", "sans-serif"],
                    "h2": ["Outfit", "sans-serif"]
            },
            "fontSize": {
                    "h3": ["20px", {"lineHeight": "1.4", "fontWeight": "700", "letterSpacing": "-0.01em"}],
                    "body-sm": ["14px", {"lineHeight": "1.6", "fontWeight": "400"}],
                    "body-md": ["16px", {"lineHeight": "1.6", "fontWeight": "400"}],
                    "h1": ["42px", {"lineHeight": "1.15", "letterSpacing": "-0.03em", "fontWeight": "800"}],
                    "body-lg": ["17px", {"lineHeight": "1.6", "fontWeight": "400"}],
                    "label-caps": ["11px", {"lineHeight": "1", "letterSpacing": "0.15em", "fontWeight": "700"}],
                    "h2": ["32px", {"lineHeight": "1.2", "letterSpacing": "-0.02em", "fontWeight": "800"}]
            }
          },
        },
      }
    </script>
"""

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has cdn.tailwindcss.com script but lacks tailwind.config
    if 'cdn.tailwindcss.com' in content and 'tailwind.config' not in content:
        # Find the closing tag of the cdn.tailwindcss.com script
        pattern = re.compile(r'(<script[^>]*src="[^"]*cdn\.tailwindcss\.com[^"]*"[^>]*>\s*</script>)', re.IGNORECASE)
        match = pattern.search(content)
        if match:
            script_tag = match.group(1)
            # Insert our tailwind_config_code right after the script tag
            new_content = content.replace(script_tag, script_tag + tailwind_config_code)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Added tailwind.config block to {file_path}")

def main():
    count = 0
    fixed = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                count += 1
                if 'cdn.tailwindcss.com' in open(file_path, 'r', encoding='utf-8').read() and 'tailwind.config' not in open(file_path, 'r', encoding='utf-8').read():
                    fix_file(file_path)
                    fixed += 1
    print(f"Done! Scanned {count} files. Fixed {fixed} files.")

if __name__ == '__main__':
    main()
