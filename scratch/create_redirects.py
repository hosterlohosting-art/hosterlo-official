import os

def create_redirect_file(filepath, target_url, canonical_url):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Redirecting...</title>
    <link rel="canonical" href="{canonical_url}" />
    <meta http-equiv="refresh" content="0;url={target_url}">
    <script>
        window.location.replace("{target_url}");
    </script>
</head>
<body>
    <p>If you are not redirected automatically, follow this <a href="{target_url}">link</a>.</p>
</body>
</html>
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created redirect: {filepath} -> {target_url}")

def main():
    root_dir = r"d:\Hosterlo Official Site"
    
    redirects = [
        # Ecommerce redirects
        ('hosting-for-ecommerce/index.html', '/hosting/ecommerce-hosting/', 'https://hosterlo.com/hosting/ecommerce-hosting/'),
        ('uk/hosting-for-ecommerce/index.html', '/uk/hosting/ecommerce-hosting/', 'https://hosterlo.com/uk/hosting/ecommerce-hosting/'),
        ('pk/hosting-for-ecommerce/index.html', '/pk/hosting/ecommerce-hosting/', 'https://hosterlo.com/pk/hosting/ecommerce-hosting/'),
        ('es/hosting-for-ecommerce/index.html', '/es/hosting/ecommerce-hosting/', 'https://hosterlo.com/es/hosting/ecommerce-hosting/'),
        
        # Blogger redirects
        ('hosting-for-bloggers/index.html', '/hosting/blog-hosting/', 'https://hosterlo.com/hosting/blog-hosting/'),
        ('uk/hosting-for-bloggers/index.html', '/uk/hosting/blog-hosting/', 'https://hosterlo.com/uk/hosting/blog-hosting/'),
        ('pk/hosting-for-bloggers/index.html', '/pk/hosting/blog-hosting/', 'https://hosterlo.com/pk/hosting/blog-hosting/'),
        ('es/hosting-for-bloggers/index.html', '/es/hosting/blog-hosting/', 'https://hosterlo.com/es/hosting/blog-hosting/'),
    ]
    
    for rel_path, target, canonical in redirects:
        full_path = os.path.join(root_dir, rel_path)
        create_redirect_file(full_path, target, canonical)
        
if __name__ == '__main__':
    main()
