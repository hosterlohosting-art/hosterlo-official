import os
import re

og_images = {
    "web-development": "/assets/web-development.png",
    "saas-development": "/assets/saas-development.png",
    "frontend-development": "/assets/frontend-development.png",
    "backend-development": "/assets/backend-development.png",
    "ui-ux-design": "/assets/ui-ux-design.png",
    "mobile-app-development": "/assets/mobile-app-development.png",
    "api-development": "/assets/api-development.png",
    "website-maintenance": "/assets/performance-monitoring-ui.webp"
}

for folder, img_path in og_images.items():
    file_path = f"services/{folder}/index.html"
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} - file does not exist.")
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace og:image content
    content = re.sub(
        r'<meta property="og:image" content="[^"]+">',
        f'<meta property="og:image" content="https://hosterlo.com{img_path}">',
        content
    )
    
    # Replace twitter:image content
    content = re.sub(
        r'<meta name="twitter:image" content="[^"]+">',
        f'<meta name="twitter:image" content="https://hosterlo.com{img_path}">',
        content
    )
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Updated og:image and twitter:image for {file_path} -> {img_path}")

print("Done updating services meta tags.")
