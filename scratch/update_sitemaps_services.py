import os

sitemap_path = r"D:\Hosterlo Official Site\sitemap.xml"

new_urls = [
    {
        "loc": "https://hosterlo.com/services/",
        "lastmod": "2026-06-11",
        "changefreq": "weekly",
        "priority": "0.90",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/services/web-development/",
        "lastmod": "2026-06-11",
        "changefreq": "weekly",
        "priority": "0.85",
        "image": "https://hosterlo.com/assets/web-development.png"
    },
    {
        "loc": "https://hosterlo.com/services/saas-development/",
        "lastmod": "2026-06-11",
        "changefreq": "weekly",
        "priority": "0.85",
        "image": "https://hosterlo.com/assets/saas-development.png"
    },
    {
        "loc": "https://hosterlo.com/services/frontend-development/",
        "lastmod": "2026-06-11",
        "changefreq": "weekly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/frontend-development.png"
    },
    {
        "loc": "https://hosterlo.com/services/backend-development/",
        "lastmod": "2026-06-11",
        "changefreq": "weekly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/backend-development.png"
    },
    {
        "loc": "https://hosterlo.com/services/ui-ux-design/",
        "lastmod": "2026-06-11",
        "changefreq": "weekly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/ui-ux-design.png"
    },
    {
        "loc": "https://hosterlo.com/services/mobile-app-development/",
        "lastmod": "2026-06-11",
        "changefreq": "weekly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/mobile-app-development.png"
    },
    {
        "loc": "https://hosterlo.com/services/api-development/",
        "lastmod": "2026-06-11",
        "changefreq": "weekly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/api-development.png"
    },
    {
        "loc": "https://hosterlo.com/services/website-maintenance/",
        "lastmod": "2026-06-11",
        "changefreq": "monthly",
        "priority": "0.80",
        "image": "https://hosterlo.com/assets/performance-monitoring-ui.webp"
    },
    {
        "loc": "https://hosterlo.com/portfolio/",
        "lastmod": "2026-06-11",
        "changefreq": "weekly",
        "priority": "0.85",
        "image": "https://hosterlo.com/assets/secure-enterprise-hosting.webp"
    },
    {
        "loc": "https://hosterlo.com/get-a-quote/",
        "lastmod": "2026-06-11",
        "changefreq": "monthly",
        "priority": "0.85",
        "image": "https://hosterlo.com/assets/logo.png"
    }
]

with open(sitemap_path, "r", encoding="utf-8") as f:
    sitemap_content = f.read()

# Build sitemap URL nodes
url_nodes = []
for url in new_urls:
    if url["loc"] in sitemap_content:
        print(f"URL already in sitemap: {url['loc']}")
        continue
    
    node = f"""  <url>
    <loc>{url['loc']}</loc>
    <lastmod>{url['lastmod']}</lastmod>
    <changefreq>{url['changefreq']}</changefreq>
    <priority>{url['priority']}</priority>
    <image:image><image:loc>{url['image']}</image:loc></image:image>
  </url>"""
    url_nodes.append(node)

if url_nodes:
    # Inject before </urlset>
    url_nodes_str = "\n\n".join(url_nodes)
    pos = sitemap_content.rfind("</urlset>")
    if pos != -1:
        updated_content = sitemap_content[:pos] + url_nodes_str + "\n" + sitemap_content[pos:]
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Successfully injected {len(url_nodes)} new URLs into sitemap.xml")
else:
    print("No new URLs to inject.")
