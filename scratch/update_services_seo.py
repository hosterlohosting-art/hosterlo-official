import os
import re

seo_mapping = {
    "services/index.html": {
        "old_title": "Web Development & Digital Agency Services | Hosterlo",
        "new_title": "Web Development &amp; Digital Agency Services USA | Hosterlo",
        "old_desc": "Custom web development, SaaS product development, frontend & backend engineering, UI/UX design, and mobile apps. Get a free project quote from Hosterlo.",
        "new_desc": "Custom web development, SaaS MVP development, frontend &amp; backend engineering, UI/UX design, and mobile apps in the USA. Get a free project quote from Hosterlo.",
        "schema_name": "Web Development &amp; Digital Agency Services USA | Hosterlo",
        "schema_desc": "Custom web development, SaaS MVP development, frontend &amp; backend engineering, UI/UX design, and mobile apps in the USA. Get a free project quote from Hosterlo."
    },
    "services/web-development/index.html": {
        "old_title": "Custom Web Development Services | Hosterlo Services",
        "new_title": "Web Development Company USA | Custom Web Design | Hosterlo",
        "old_desc": "Custom web development services by Hosterlo. We build fast, secure, and SEO-optimized custom websites tailored to convert visitors into loyal customers.",
        "new_desc": "Top custom web development company in the USA. We build fast, secure, and SEO-optimized custom websites tailored to convert visitors into loyal customers.",
        "schema_name": "Web Development Company USA",
        "schema_desc": "Top custom web development company in the USA. We build fast, secure, and SEO-optimized custom websites tailored to convert visitors into loyal customers."
    },
    "services/saas-development/index.html": {
        "old_title": "SaaS Product Development Company | Hosterlo Services",
        "new_title": "SaaS Product Development Company USA | Build SaaS MVP",
        "old_desc": "End-to-end SaaS product development company services by Hosterlo. We design, build, and launch scalable, secure, and multi-tenant software-as-a-service apps.",
        "new_desc": "Expert SaaS product development company in the USA. We design, build, and launch scalable, secure, and multi-tenant software-as-a-service (SaaS) apps.",
        "schema_name": "SaaS Product Development Company USA",
        "schema_desc": "Expert SaaS product development company in the USA. We design, build, and launch scalable, secure, and multi-tenant software-as-a-service (SaaS) apps."
    },
    "services/frontend-development/index.html": {
        "old_title": "Frontend Development Services | Hosterlo Services",
        "new_title": "Frontend Development Company USA | React & Next.js Developers",
        "old_desc": "Sleek, responsive frontend development services by Hosterlo. We build fast, interactive, and visually stunning user interfaces optimized for all devices.",
        "new_desc": "Professional frontend development company in the USA. We build fast, responsive, and visually stunning user interfaces optimized for all devices.",
        "schema_name": "Frontend Development Company USA",
        "schema_desc": "Professional frontend development company in the USA. We build fast, responsive, and visually stunning user interfaces optimized for all devices."
    },
    "services/backend-development/index.html": {
        "old_title": "Backend Development Services | Hosterlo Services",
        "new_title": "Backend Development Services USA | Node.js & Python APIs",
        "old_desc": "Robust backend development services by Hosterlo. We build secure, reliable, and scalable server-side systems, databases, and application architectures.",
        "new_desc": "Robust backend development services in the USA. We build secure, reliable, and scalable server-side systems, databases, and application architectures.",
        "schema_name": "Backend Development Services USA",
        "schema_desc": "Robust backend development services in the USA. We build secure, reliable, and scalable server-side systems, databases, and application architectures."
    },
    "services/ui-ux-design/index.html": {
        "old_title": "UI/UX Design Services | Hosterlo Services",
        "new_title": "UI/UX Design Services USA | Figma Wireframes & Prototypes",
        "old_desc": "User-centric UI/UX design services by Hosterlo. We create intuitive user journeys, wireframes, prototypes, and visually stunning interfaces that convert.",
        "new_desc": "User-centric UI/UX design services in the USA. We create intuitive user journeys, Figma wireframes, interactive prototypes, and visually stunning interfaces.",
        "schema_name": "UI/UX Design Services USA",
        "schema_desc": "User-centric UI/UX design services in the USA. We create intuitive user journeys, Figma wireframes, interactive prototypes, and visually stunning interfaces."
    },
    "services/mobile-app-development/index.html": {
        "old_title": "Mobile App Development Services | Hosterlo Services",
        "new_title": "Mobile App Development Company USA | iOS & Android Apps",
        "old_desc": "Custom mobile app development services by Hosterlo. We build high-performance iOS and Android applications designed for seamless user experiences.",
        "new_desc": "Custom mobile app development company in the USA. We build high-performance, native and cross-platform iOS and Android applications designed for seamless user experience.",
        "schema_name": "Mobile App Development Company USA",
        "schema_desc": "Custom mobile app development company in the USA. We build high-performance, native and cross-platform iOS and Android applications designed for seamless user experience."
    },
    "services/api-development/index.html": {
        "old_title": "API Development & Integration Services | Hosterlo Services",
        "new_title": "API Development & Integration Services USA | Hosterlo",
        "old_desc": "Professional API development and integration services by Hosterlo. We build secure, scalable, and high-performance APIs for web and mobile applications.",
        "new_desc": "Professional API development and integration services in the USA. We build secure, scalable, and high-performance REST and GraphQL APIs.",
        "schema_name": "API Development & Integration Services USA",
        "schema_desc": "Professional API development and integration services in the USA. We build secure, scalable, and high-performance REST and GraphQL APIs."
    },
    "services/website-maintenance/index.html": {
        "old_title": "Website Maintenance & Support Plans | Hosterlo Services",
        "new_title": "Website Maintenance & Support Plans USA | Hosterlo",
        "old_desc": "Comprehensive website maintenance and support plans by Hosterlo. Keep your website fast, secure, updated, and running smoothly with our expert support.",
        "new_desc": "Comprehensive website maintenance and support plans in the USA. Keep your website fast, secure, updated, and running smoothly with our expert support.",
        "schema_name": "Website Maintenance & Support Plans USA",
        "schema_desc": "Comprehensive website maintenance and support plans in the USA. Keep your website fast, secure, updated, and running smoothly with our expert support."
    }
}

def update_file(rel_path, data):
    file_path = os.path.join(os.getcwd(), rel_path)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    print(f"Updating: {rel_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Standard Title Tag replacement
    old_title_tag = f"<title>{data['old_title']}</title>"
    new_title_tag = f"<title>{data['new_title']}</title>"
    content = content.replace(old_title_tag, new_title_tag)
    
    # Meta description replacements (handles both closing slash variations)
    desc_patterns = [
        f'<meta name="description" content="{data["old_desc"]}" />',
        f'<meta name="description" content="{data["old_desc"]}">',
        f'<meta name="description" content="{data["old_desc"]}"  />'
    ]
    for desc_pattern in desc_patterns:
        content = content.replace(desc_pattern, f'<meta name="description" content="{data["new_desc"]}">')
        
    # Open Graph Title replacement
    content = content.replace(f'property="og:title" content="{data["old_title"]}"', f'property="og:title" content="{data["new_title"]}"')
    content = content.replace(f'property="og:title" content="{data["old_title"]}">', f'property="og:title" content="{data["new_title"]}">')
    
    # Open Graph Description replacement
    content = content.replace(f'property="og:description" content="{data["old_desc"]}" />', f'property="og:description" content="{data["new_desc"]}">')
    content = content.replace(f'property="og:description" content="{data["old_desc"]}">', f'property="og:description" content="{data["new_desc"]}">')
    
    # Twitter Title replacement
    content = content.replace(f'name="twitter:title" content="{data["old_title"]}"', f'name="twitter:title" content="{data["new_title"]}"')
    content = content.replace(f'name="twitter:title" content="{data["old_title"]}">', f'name="twitter:title" content="{data["new_title"]}">')
    
    # Twitter Description replacement
    content = content.replace(f'name="twitter:description" content="{data["old_desc"]}" />', f'name="twitter:description" content="{data["new_desc"]}">')
    content = content.replace(f'name="twitter:description" content="{data["old_desc"]}">', f'name="twitter:description" content="{data["new_desc"]}">')
    
    # JSON-LD Schemas replacement
    content = content.replace(f'"name": "{data["old_title"]}"', f'"name": "{data["schema_name"]}"')
    content = content.replace(f'"name": "{data["old_title"][:-len(" | Hosterlo Services")] if " | Hosterlo Services" in data["old_title"] else data["old_title"]}"', f'"name": "{data["schema_name"]}"')
    content = content.replace(f'"description": "{data["old_desc"]}"', f'"description": "{data["schema_desc"]}"')
    
    # Body heading H1 optimization (if any)
    old_h1_text = data["old_title"].split(" | ")[0]
    new_h1_text = data["new_title"].split(" | ")[0]
    # Example: "SaaS Product Development Company" -> "SaaS Product Development Company USA"
    content = content.replace(f'>{old_h1_text}</h1>', f'>{new_h1_text}</h1>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Finished: {rel_path}")

def main():
    for rel_path, data in seo_mapping.items():
        update_file(rel_path, data)
        
if __name__ == '__main__':
    main()
