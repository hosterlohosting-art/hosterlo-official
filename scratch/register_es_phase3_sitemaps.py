import os

base_dir = r"d:\Hosterlo Official Site"
sitemaps = [
    os.path.join(base_dir, "sitemap.xml"),
    os.path.join(base_dir, "page-sitemap.xml")
]

es_new_urls = [
    {
        "loc": "https://hosterlo.com/es/services/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/logo.png"
    },
    {
        "loc": "https://hosterlo.com/es/services/web-development/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/web-development.png"
    },
    {
        "loc": "https://hosterlo.com/es/services/saas-development/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/saas-development.png"
    },
    {
        "loc": "https://hosterlo.com/es/services/frontend-development/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/frontend-development.png"
    },
    {
        "loc": "https://hosterlo.com/es/services/backend-development/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/backend-development.png"
    },
    {
        "loc": "https://hosterlo.com/es/services/ui-ux-design/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/ui-ux-design.png"
    },
    {
        "loc": "https://hosterlo.com/es/services/mobile-app-development/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/mobile-app-development.png"
    },
    {
        "loc": "https://hosterlo.com/es/services/api-development/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/api-development.png"
    },
    {
        "loc": "https://hosterlo.com/es/services/website-maintenance/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/performance-monitoring-ui.webp"
    },
    {
        "loc": "https://hosterlo.com/es/portfolio/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/logo.png"
    },
    {
        "loc": "https://hosterlo.com/es/get-a-quote/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/logo.png"
    },
    {
        "loc": "https://hosterlo.com/es/hosting/ecommerce-hosting/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/hosting/blog-hosting/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/hosting/cheap-hosting-with-domain/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/alternatives/namecheap/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/alternatives/dreamhost/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/alternatives/wpengine/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/compare/hosterlo-vs-bluehost/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/compare/hosterlo-vs-hostinger/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/compare/hosterlo-vs-siteground/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/compare/hosterlo-vs-godaddy/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/compare/hosterlo-vs-namecheap/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/compare/hosterlo-vs-dreamhost/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/es/compare/hosterlo-vs-wpengine/",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
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
    
    for url in es_new_urls:
        if url["loc"] in content:
            print(f"URL {url['loc']} is already registered in {os.path.basename(sm)}")
            continue
            
        node = f"""  <url>
    <loc>{url['loc']}</loc>
    <lastmod>2026-06-18</lastmod>
    <changefreq>weekly</changefreq>
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
            print(f"Injected {injected_count} new Spanish URLs into {os.path.basename(sm)}")
        else:
            print(f"Could not find </urlset> in {os.path.basename(sm)}!")
    else:
        print(f"No new Spanish URLs to inject into {os.path.basename(sm)}")

print("Sitemap registration for Spanish pages completed.")
