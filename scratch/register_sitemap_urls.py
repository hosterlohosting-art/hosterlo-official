import os

base_dir = r"d:\Hosterlo Official Site"
sitemaps = [
    os.path.join(base_dir, "sitemap.xml"),
    os.path.join(base_dir, "page-sitemap.xml")
]

missing_urls_data = [
    {
        "loc": "https://hosterlo.com/2026/06/03/react-vs-vue-vs-angular-which-for-your-project/",
        "lastmod": "2026-06-16",
        "changefreq": "weekly",
        "priority": "0.75",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/gemini-pro/",
        "lastmod": "2026-06-16",
        "changefreq": "weekly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/logo.png"
    },
    {
        "loc": "https://hosterlo.com/hosting/business-email/",
        "lastmod": "2026-06-16",
        "changefreq": "weekly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/logo.png"
    },
    {
        "loc": "https://hosterlo.com/hosting-for-small-business/",
        "lastmod": "2026-06-16",
        "changefreq": "weekly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/logo.png"
    },
    {
        "loc": "https://hosterlo.com/pk/hosting/business-email/",
        "lastmod": "2026-06-16",
        "changefreq": "weekly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/logo.png"
    },
    {
        "loc": "https://hosterlo.com/uk/hosting/business-email/",
        "lastmod": "2026-06-16",
        "changefreq": "weekly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/logo.png"
    }
]

for sm in sitemaps:
    if not os.path.exists(sm):
        print(f"Sitemap {sm} not found!")
        continue
    
    with open(sm, "r", encoding="utf-8") as f:
        content = f.read()
    
    injected_count = 0
    injected_nodes = []
    
    for url in missing_urls_data:
        # Check if already present
        if url["loc"] in content:
            print(f"URL {url['loc']} is already in {os.path.basename(sm)}")
            continue
            
        node = f"""  <url>
    <loc>{url['loc']}</loc>
    <lastmod>{url['lastmod']}</lastmod>
    <changefreq>{url['changefreq']}</changefreq>
    <priority>{url['priority']}</priority>
    <image:image><image:loc>{url['image']}</image:loc></image:image>
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
            print(f"Injected {injected_count} URLs into {os.path.basename(sm)}")
        else:
            print(f"Could not find </urlset> in {os.path.basename(sm)}!")
    else:
        print(f"No new URLs to inject into {os.path.basename(sm)}")
