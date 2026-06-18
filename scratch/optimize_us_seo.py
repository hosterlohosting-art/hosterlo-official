import os
import re

ROOT = "d:/Hosterlo Official Site"

optimizations = {
    "hosting/index.html": {
        "title": "Web Hosting Services USA | Free Domain & Email | Hosterlo",
        "desc": "Get fast, NVMe-backed web hosting in the USA for $59/year. Includes a free .com domain, business email, SSL, setup support, and 18 months of Gemini Pro.",
        "h1": "Web Hosting Services USA"
    },
    "hosting/shared-hosting/index.html": {
        "title": "Shared Web Hosting USA | Cheap cPanel Hosting | Hosterlo",
        "desc": "Affordable shared web hosting in the USA with cPanel. Get SSD speed, a free .com domain, SSL, business email, and WhatsApp support for just $59/year.",
        "h1": "Shared Web Hosting USA"
    },
    "hosting/wordpress-hosting/index.html": {
        "title": "Managed WordPress Hosting USA | Fast LiteSpeed WP | Hosterlo",
        "desc": "Fast, managed WordPress hosting in the USA. Optimized for LiteSpeed caching, SSD speed, free .com domain, SSL, business email, and WhatsApp setup support.",
        "h1": "Managed WordPress Hosting USA"
    },
    "domains/index.html": {
        "title": "Domain Name Registration USA | Buy .com Domain | Hosterlo",
        "desc": "Search and register domain names in the USA. Get a free .com domain with Hosterlo's hosting bundle, complete with free WHOIS privacy and DNS tools.",
        "h1": "Domain Name Registration USA"
    },
    "pricing/index.html": {
        "title": "Web Hosting Pricing USA | Flat-Rate $59/Yr Bundle | Hosterlo",
        "desc": "Compare Hosterlo's transparent web hosting pricing. The $59/year Website Launch Bundle features flat renewals, a free domain, email, and setup support.",
        "h1": "Transparent Hosting Pricing"
    },
    "contact-us/index.html": {
        "title": "Contact Hosterlo USA | Sales & Setup Support Chat",
        "desc": "Contact Hosterlo USA support and sales. Connect with our experts via phone, ticketing, or direct WhatsApp chat for website setup, migration, and billing help.",
        "h1": "Contact Hosterlo USA"
    },
    "about-hosterlo/index.html": {
        "title": "About Hosterlo | Reliable Web Hosting Company USA",
        "desc": "Learn about Hosterlo, an honest web hosting company in the USA. We offer transparent $59/year NVMe hosting packages backed by global Digioverse cloud systems.",
        "h1": "About Hosterlo"
    }
}

def optimize_file(file_rel, data):
    file_path = os.path.join(ROOT, file_rel)
    if not os.path.exists(file_path):
        print(f"Skipping missing file: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Title Tag
    content = re.sub(r'<title>.*?</title>', f'<title>{data["title"]}</title>', content)
    content = re.sub(r'<meta\s+property=["\']og:title["\']\s+content="[^"]*"', f'<meta property="og:title" content="{data["title"]}"', content)
    content = re.sub(r'<meta\s+name=["\']twitter:title["\']\s+content="[^"]*"', f'<meta name="twitter:title" content="{data["title"]}"', content)

    # 2. Meta Description
    content = re.sub(r'<meta\s+name=["\']description["\']\s+content="[^"]*"', f'<meta name="description" content="{data["desc"]}"', content)
    content = re.sub(r'<meta\s+property=["\']og:description["\']\s+content="[^"]*"', f'<meta property="og:description" content="{data["desc"]}"', content)
    content = re.sub(r'<meta\s+name=["\']twitter:description["\']\s+content="[^"]*"', f'<meta name="twitter:description" content="{data["desc"]}"', content)

    # 3. Update H1 if matches the pattern
    # Find the first H1 in the file and replace its contents
    h1_match = re.search(r'(<h1[^>]*>).*?(</h1>)', content, re.DOTALL | re.IGNORECASE)
    if h1_match:
        # replace inner HTML of H1
        start_tag = h1_match.group(1)
        end_tag = h1_match.group(2)
        # We only replace if we want to update the headline to be US targeted
        # Let's inspect the original H1 to see if it makes sense to replace
        orig_h1 = h1_match.group(0)
        # Let's replace the whole H1 match with start_tag + data["h1"] + end_tag
        content = content.replace(orig_h1, f'{start_tag}{data["h1"]}{end_tag}')

    # 4. Schema Updates
    # Set areaServed in the first/ Organization schema to United States
    content = content.replace('"areaServed": "Worldwide"', '"areaServed": {"@type": "Country", "name": "United States"}')
    content = content.replace('"areaServed":{"@type":"Country","name":"United States"}', '"areaServed": {"@type": "Country", "name": "United States"}')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Optimized US SEO on page: {file_path}")

def main():
    for file_rel, data in optimizations.items():
        optimize_file(file_rel, data)

if __name__ == '__main__':
    main()
