import os

base_dir = r"d:\Hosterlo Official Site"
sitemaps = [
    os.path.join(base_dir, "sitemap.xml"),
    os.path.join(base_dir, "page-sitemap.xml")
]

new_urls = [
    # US Niche Hosting
    "https://hosterlo.com/hosting/ecommerce-hosting/",
    "https://hosterlo.com/hosting/blog-hosting/",
    "https://hosterlo.com/hosting/cheap-hosting-with-domain/",
    # UK Niche Hosting
    "https://hosterlo.com/uk/hosting/ecommerce-hosting/",
    "https://hosterlo.com/uk/hosting/blog-hosting/",
    "https://hosterlo.com/uk/hosting/cheap-hosting-with-domain/",
    # PK Niche Hosting
    "https://hosterlo.com/pk/hosting/ecommerce-hosting/",
    "https://hosterlo.com/pk/hosting/blog-hosting/",
    "https://hosterlo.com/pk/hosting/cheap-hosting-with-domain/",
    
    # US Alternatives
    "https://hosterlo.com/alternatives/namecheap/",
    "https://hosterlo.com/alternatives/dreamhost/",
    "https://hosterlo.com/alternatives/wpengine/",
    # UK Alternatives
    "https://hosterlo.com/uk/alternatives/namecheap/",
    "https://hosterlo.com/uk/alternatives/dreamhost/",
    "https://hosterlo.com/uk/alternatives/wpengine/",
    # PK Alternatives
    "https://hosterlo.com/pk/alternatives/namecheap/",
    "https://hosterlo.com/pk/alternatives/dreamhost/",
    "https://hosterlo.com/pk/alternatives/wpengine/",
]

for sm in sitemaps:
    if not os.path.exists(sm):
        print(f"Sitemap {sm} not found!")
        continue
    
    with open(sm, "r", encoding="utf-8") as f:
        content = f.read()
    
    injected_count = 0
    injected_nodes = []
    
    for url in new_urls:
        if url in content:
            print(f"URL {url} is already registered in {os.path.basename(sm)}")
            continue
        
        priority = "0.80"
        image = "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
            
        node = f"""  <url>
    <loc>{url}</loc>
    <lastmod>2026-06-17</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
    <image:image><image:loc>{image}</image:loc></image:image>
  </url>"""
        injected_nodes.append(node)
        injected_count += 1
        
    if injected_nodes:
        nodes_str = "\n\n" + "\n\n".join(injected_nodes) + "\n"
        pos = content.rfind("</urlset>")
        if pos != -1:
            updated_content = content[:pos] + nodes_str + content[pos:]
            with open(sm, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Injected {injected_count} new URLs into {os.path.basename(sm)}")
        else:
            print(f"Could not find </urlset> in {os.path.basename(sm)}!")
    else:
        print(f"No new URLs to inject into {os.path.basename(sm)}")

print("Sitemap registration completed successfully.")
