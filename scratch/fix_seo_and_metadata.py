import os
import re
import json

base_dir = r"d:\Hosterlo Official Site"

def read_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# Helper to find/replace/insert meta/link tags in HTML content
def set_meta_tag(content, name, value, is_property=False):
    # Regex to find meta tag with name or property
    attr = "property" if is_property else "name"
    pattern = re.compile(rf'<meta\b[^>]*\b{attr}="{re.escape(name)}"[^>]*>', re.IGNORECASE)
    new_tag = f'<meta {attr}="{name}" content="{value}" />'
    
    if pattern.search(content):
        # Replace existing
        content = pattern.sub(new_tag, content)
    else:
        # Insert before </head>
        content = content.replace('</head>', f'    {new_tag}\n</head>')
    return content

def set_link_tag(content, rel, href, extra_attrs=""):
    # Regex to find link tag with rel
    pattern = re.compile(rf'<link\b[^>]*\brel="{re.escape(rel)}"[^>]*>', re.IGNORECASE)
    new_tag = f'<link rel="{rel}" {extra_attrs} href="{href}" />'
    
    if pattern.search(content):
        # Replace existing
        content = pattern.sub(new_tag, content)
    else:
        # Insert before </head>
        content = content.replace('</head>', f'    {new_tag}\n</head>')
    return content

def set_title(content, title_text):
    pattern = re.compile(r'<title>(.*?)</title>', re.IGNORECASE)
    new_tag = f'<title>{title_text}</title>'
    if pattern.search(content):
        content = pattern.sub(new_tag, content)
    else:
        content = content.replace('</head>', f'    {new_tag}\n</head>')
    return content

def add_schema(content, schema_dict):
    schema_str = json.dumps(schema_dict, indent=2)
    schema_block = f'\n    <script type="application/ld+json">\n{schema_str}\n    </script>\n'
    content = content.replace('</head>', f'{schema_block}</head>')
    return content

# 1. Fix 404.html
def fix_404():
    path = os.path.join(base_dir, "404.html")
    if not os.path.exists(path):
        return
    print("Fixing 404.html...")
    content = read_file(path)
    
    content = set_title(content, "404 Page Not Found - Web Hosting & Support | Hosterlo")
    content = set_meta_tag(content, "description", "Oops! The page you are looking for at Hosterlo cannot be found. Go back to our homepage to find fast web hosting, domains, business email, and support.")
    content = set_link_tag(content, "canonical", "https://hosterlo.com/404.html")
    content = set_meta_tag(content, "og:image", "https://hosterlo.com/assets/logo.png", is_property=True)
    content = set_meta_tag(content, "twitter:card", "summary_large_image")
    
    # Simple WebPage schema
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "404 Page Not Found | Hosterlo",
        "description": "Oops! The page you are looking for at Hosterlo cannot be found.",
        "url": "https://hosterlo.com/404.html"
    }
    content = add_schema(content, schema)
    write_file(path, content)

# 2. Fix faq/index.html
def fix_faq():
    path = os.path.join(base_dir, "faq", "index.html")
    if not os.path.exists(path):
        return
    print("Fixing faq/index.html...")
    content = read_file(path)
    content = set_meta_tag(content, "og:image", "https://hosterlo.com/assets/logo.png", is_property=True)
    content = set_meta_tag(content, "twitter:card", "summary_large_image")
    write_file(path, content)

# 3. Fix gemini-pro/index.html
def fix_gemini_pro():
    path = os.path.join(base_dir, "gemini-pro", "index.html")
    if not os.path.exists(path):
        return
    print("Fixing gemini-pro/index.html...")
    content = read_file(path)
    content = set_meta_tag(content, "og:image", "https://hosterlo.com/assets/logo.png", is_property=True)
    content = set_meta_tag(content, "twitter:card", "summary_large_image")
    
    # Gemini Pro Bundle schema
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "@id": "https://hosterlo.com/gemini-pro/#product",
                "name": "Hosterlo Website Launch Bundle with Gemini Pro Bonus",
                "image": "https://hosterlo.com/assets/logo.png",
                "description": "Get Hosterlo’s $59/year Website Launch Bundle with hosting, free .com domain, SSL, business email, setup support, and Gemini Pro bonus for 18 months.",
                "brand": {
                    "@type": "Brand",
                    "name": "Hosterlo"
                },
                "offers": {
                    "@type": "Offer",
                    "url": "https://hosterlo.com/gemini-pro/",
                    "priceCurrency": "USD",
                    "price": "59.00",
                    "priceValidUntil": "2027-12-31",
                    "availability": "https://schema.org/InStock",
                    "seller": {
                        "@type": "Organization",
                        "name": "Hosterlo",
                        "url": "https://hosterlo.com/"
                    }
                }
            },
            {
                "@type": "WebPage",
                "@id": "https://hosterlo.com/gemini-pro/#webpage",
                "url": "https://hosterlo.com/gemini-pro/",
                "name": "Hosting Bundle with Gemini Pro Bonus for 18 Months — Hosterlo",
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": "https://hosterlo.com/#website",
                    "name": "Hosterlo",
                    "url": "https://hosterlo.com/"
                },
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://hosterlo.com/"},
                        {"@type": "ListItem", "position": 2, "name": "Gemini Pro Offer", "item": "https://hosterlo.com/gemini-pro/"}
                    ]
                }
            }
        ]
    }
    content = add_schema(content, schema)
    write_file(path, content)

# 4. Fix business email hosting (root, uk, pk)
def fix_business_email():
    paths = [
        ("hosting/business-email/index.html", "https://hosterlo.com/hosting/business-email/", "https://hosterlo.com/"),
        ("uk/hosting/business-email/index.html", "https://hosterlo.com/uk/hosting/business-email/", "https://hosterlo.com/uk/"),
        ("pk/hosting/business-email/index.html", "https://hosterlo.com/pk/hosting/business-email/", "https://hosterlo.com/pk/")
    ]
    for rel_path, url, home_url in paths:
        abs_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(abs_path):
            continue
        print(f"Fixing {rel_path}...")
        content = read_file(abs_path)
        content = set_meta_tag(content, "og:image", "https://hosterlo.com/assets/logo.png", is_property=True)
        content = set_meta_tag(content, "twitter:card", "summary_large_image")
        
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Service",
                    "@id": f"{url}#service",
                    "name": "Business Email Hosting",
                    "serviceType": "Email Hosting",
                    "description": "Create professional business email addresses with your domain. Hosterlo's bundle includes hosting, free .com domain, SSL, and support.",
                    "provider": {
                        "@type": "Organization",
                        "name": "Hosterlo",
                        "url": "https://hosterlo.com/"
                    },
                    "offers": {
                        "@type": "Offer",
                        "priceCurrency": "USD",
                        "price": "59.00",
                        "url": url
                    }
                },
                {
                    "@type": "WebPage",
                    "@id": f"{url}#webpage",
                    "url": url,
                    "name": "Business Email Hosting for Your Domain — Hosterlo",
                    "breadcrumb": {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": home_url},
                            {"@type": "ListItem", "position": 2, "name": "Business Email Hosting", "item": url}
                        ]
                    }
                }
            ]
        }
        content = add_schema(content, schema)
        write_file(abs_path, content)

# 5. Fix legal/index.html
def fix_legal():
    path = os.path.join(base_dir, "legal", "index.html")
    if not os.path.exists(path):
        return
    print("Fixing legal/index.html...")
    content = read_file(path)
    content = set_title(content, "Legal Notices, Policies, & Terms of Service | Hosterlo")
    write_file(path, content)

# 6. Fix legal/gemini-pro-terms/index.html
def fix_gemini_pro_terms():
    path = os.path.join(base_dir, "legal", "gemini-pro-terms", "index.html")
    if not os.path.exists(path):
        return
    print("Fixing legal/gemini-pro-terms/index.html...")
    content = read_file(path)
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Google Gemini Pro AI Bonus Terms | Hosterlo",
        "description": "Terms of service and conditions for Google Gemini Pro AI bonus package provided with Hosterlo's Website Launch Bundle.",
        "url": "https://hosterlo.com/legal/gemini-pro-terms/"
    }
    content = add_schema(content, schema)
    write_file(path, content)

# 7. Fix contact-us (root, uk, pk)
def fix_contact_us():
    paths = [
        "contact-us/index.html",
        "uk/contact-us/index.html",
        "pk/contact-us/index.html"
    ]
    desc = "Contact Hosterlo for premium web hosting sales, technical support, billing inquiries, or Gemini Pro AI activation. We offer fast, human WhatsApp support."
    for rel_path in paths:
        abs_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(abs_path):
            continue
        print(f"Fixing description in {rel_path}...")
        content = read_file(abs_path)
        content = set_meta_tag(content, "description", desc)
        # Also set og:description and twitter:description to keep it aligned
        content = set_meta_tag(content, "og:description", desc, is_property=True)
        content = set_meta_tag(content, "twitter:description", desc)
        write_file(abs_path, content)

# 8. Fix service pages descriptions and empty schemas
def fix_service_pages():
    services = {
        "api-development": {
            "name": "API Development & Integration Services",
            "short_name": "API Development",
            "desc": "Professional API development and integration services by Hosterlo. We build secure, scalable, and high-performance APIs for web and mobile applications."
        },
        "backend-development": {
            "name": "Backend Development Services",
            "short_name": "Backend Development",
            "desc": "Robust backend development services by Hosterlo. We build secure, reliable, and scalable server-side systems, databases, and application architectures."
        },
        "frontend-development": {
            "name": "Frontend Development Services",
            "short_name": "Frontend Development",
            "desc": "Sleek, responsive frontend development services by Hosterlo. We build fast, interactive, and visually stunning user interfaces optimized for all devices."
        },
        "mobile-app-development": {
            "name": "Mobile App Development Services",
            "short_name": "Mobile App Development",
            "desc": "Custom mobile app development services by Hosterlo. We build high-performance iOS and Android applications designed for seamless user experiences."
        },
        "saas-development": {
            "name": "SaaS Product Development Company Services",
            "short_name": "SaaS Development",
            "desc": "End-to-end SaaS product development company services by Hosterlo. We design, build, and launch scalable, secure, and multi-tenant software-as-a-service apps."
        },
        "ui-ux-design": {
            "name": "UI/UX Design Services",
            "short_name": "UI/UX Design",
            "desc": "User-centric UI/UX design services by Hosterlo. We create intuitive user journeys, wireframes, prototypes, and visually stunning interfaces that convert."
        },
        "web-development": {
            "name": "Custom Web Development Services",
            "short_name": "Web Development",
            "desc": "Custom web development services by Hosterlo. We build fast, secure, and SEO-optimized custom websites tailored to convert visitors into loyal customers."
        },
        "website-maintenance": {
            "name": "Website Maintenance & Support Plans",
            "short_name": "Website Maintenance",
            "desc": "Comprehensive website maintenance and support plans by Hosterlo. Keep your website fast, secure, updated, and running smoothly with our expert support."
        }
    }
    
    for slug, info in services.items():
        rel_path = f"services/{slug}/index.html"
        abs_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(abs_path):
            continue
        print(f"Fixing service page {rel_path}...")
        content = read_file(abs_path)
        
        # Set description
        content = set_meta_tag(content, "description", info["desc"])
        content = set_meta_tag(content, "og:description", info["desc"], is_property=True)
        content = set_meta_tag(content, "twitter:description", info["desc"])
        
        # Replace empty schema block
        url = f"https://hosterlo.com/services/{slug}/"
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Service",
                    "@id": f"{url}#service",
                    "name": info["name"],
                    "description": info["desc"],
                    "provider": {
                        "@type": "Organization",
                        "name": "Hosterlo",
                        "url": "https://hosterlo.com/"
                    }
                },
                {
                    "@type": "WebPage",
                    "@id": f"{url}#webpage",
                    "url": url,
                    "name": f"{info['name']} | Hosterlo Services",
                    "breadcrumb": {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://hosterlo.com/"},
                            {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://hosterlo.com/services/"},
                            {"@type": "ListItem", "position": 3, "name": info["short_name"], "item": url}
                        ]
                    }
                }
            ]
        }
        
        # Match <script ...application/ld+json...>{}</script> (possibly with whitespace)
        empty_schema_pattern = re.compile(r'<script\b[^>]*type="application/ld\+json"[^>]*>\s*\{\}\s*</script>', re.DOTALL | re.IGNORECASE)
        schema_str = json.dumps(schema, indent=2)
        new_schema_block = f'<script type="application/ld+json">\n{schema_str}\n    </script>'
        
        if empty_schema_pattern.search(content):
            content = empty_schema_pattern.sub(new_schema_block, content)
        else:
            # If not found (or already fixed/replaced), add it
            content = add_schema(content, schema)
            
        write_file(abs_path, content)

# 9. Standardize hreflang localization for the 14 path sets
def fix_hreflangs():
    path_sets = [
        "", # homepage
        "about-hosterlo/",
        "compare/hosterlo-vs-bluehost/",
        "compare/hosterlo-vs-godaddy/",
        "compare/hosterlo-vs-hostinger/",
        "compare/hosterlo-vs-siteground/",
        "contact-us/",
        "domains/",
        "hosting/",
        "hosting/business-email/",
        "hosting/shared-hosting/",
        "hosting/wordpress-hosting/",
        "pricing/",
        "website-migration/"
    ]
    
    # We will search for all files in this list for US (rel_path = PATH + "index.html"), UK ("uk/" + PATH + "index.html"), PK ("pk/" + PATH + "index.html")
    for path_slug in path_sets:
        # Files for this path
        versions = [
            ("", f"{path_slug}index.html", f"https://hosterlo.com/{path_slug}"),
            ("uk", f"uk/{path_slug}index.html", f"https://hosterlo.com/uk/{path_slug}"),
            ("pk", f"pk/{path_slug}index.html", f"https://hosterlo.com/pk/{path_slug}")
        ]
        
        # Build new hreflang blocks
        hreflang_tags = (
            f'    <link rel="alternate" hreflang="en-us" href="https://hosterlo.com/{path_slug}" />\n'
            f'    <link rel="alternate" hreflang="en-gb" href="https://hosterlo.com/uk/{path_slug}" />\n'
            f'    <link rel="alternate" hreflang="en-pk" href="https://hosterlo.com/pk/{path_slug}" />\n'
            f'    <link rel="alternate" hreflang="x-default" href="https://hosterlo.com/{path_slug}" />'
        )
        
        for lang, rel_file, canonical_url in versions:
            abs_file = os.path.join(base_dir, rel_file)
            if not os.path.exists(abs_file):
                # Handle special case where root index.html is just "index.html"
                if rel_file == "index.html":
                    abs_file = os.path.join(base_dir, "index.html")
                else:
                    continue
            
            print(f"Aligning hreflangs and canonical in {rel_file}...")
            content = read_file(abs_file)
            
            # Remove any existing alternate hreflang tags
            content = re.sub(r'\s*<link[^>]*rel="alternate"[^>]*hreflang="[^"]*"[^>]*>', '', content, flags=re.IGNORECASE)
            
            # Update canonical to the correct one
            content = set_link_tag(content, "canonical", canonical_url)
            
            # Insert new hreflang block right before </head>
            content = content.replace('</head>', f'{hreflang_tags}\n</head>')
            
            write_file(abs_file, content)

if __name__ == "__main__":
    fix_404()
    fix_faq()
    fix_gemini_pro()
    fix_business_email()
    fix_legal()
    fix_gemini_pro_terms()
    fix_contact_us()
    fix_service_pages()
    fix_hreflangs()
    print("All fixes completed!")
