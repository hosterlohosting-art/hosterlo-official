import os
import re

services_data = {
    "web-development": {
        "title": "Custom Web Development Services",
        "tagline": "Custom Websites That Convert Visitors Into Customers",
        "description": "We develop high-performance custom websites from scratch, tailored to your brand identity, business workflows, and user expectations. Whether you need a corporate portal, a sales funnel, or a bespoke CMS solution, our expert team writes clean, modular code that loads instantly and ranks on Google.",
        "hero_image": "/assets/web-development.png",
        "starting_price": "$999 flat rate",
        "bullets": [
            "Bespoke Responsive Layouts & Design Systems",
            "Headless CMS Integration (Next.js + Sanity/Strapi)",
            "Custom WordPress Block Themes & Plugin Engineering",
            "SEO-ready Semantics & Schema Markup Included"
        ],
        "benefits": [
            {"title": "LiteSpeed Optimized", "text": "Structured to leverage LiteSpeed server caching algorithms for sub-second speeds."},
            {"title": "Clean Code Quality", "text": "Strict adherence to HTML5/CSS3 and JS standards, eliminating bloated frameworks."}
        ],
        "tech_stack": ["HTML5 / CSS3", "JavaScript (ES6+)", "React.js", "Next.js", "WordPress", "Tailwind CSS"],
        "packages": [
            {"name": "Starter Landing Page", "price": "$999", "desc": "Perfect for single-product launches or campaign funnels.", "items": ["1 Premium Landing Page", "Custom Design Mockup", "Basic Contact Form", "SEO Setup & SSL Integration", "1 Year Shared Hosting Included"]},
            {"name": "Business Website", "price": "$2,499", "desc": "Ideal for service providers and growing companies.", "items": ["Up to 10 Custom Pages", "Bespoke UI/UX Design", "CMS Integration (WordPress/Strapi)", "Custom Lead Capture Forms", "30-Day Post-Launch Support"]},
            {"name": "Custom Portal / E-commerce", "price": "$4,999", "desc": "Complete tailored solutions for transactions and databases.", "items": ["Unlimited Products / Pages", "WooCommerce/Shopify Setup", "Payment Gateway Integration", "Custom Admin Dashboard", "60-Day Premium Maintenance"]}
        ]
    },
    "saas-development": {
        "title": "SaaS Product Development Company",
        "tagline": "Build Your SaaS Product From Idea to Launch",
        "description": "Launch your software-as-a-service application with a scalable, secure, and robust architecture. From wireframing the MVP to scaling a multi-tenant cloud environment, we handle authentication, subscription billing, custom databases, and sleek dashboards so you can focus on user acquisition.",
        "hero_image": "/assets/saas-development.png",
        "starting_price": "$8,000 package",
        "bullets": [
            "Multi-Tenant Database Architectures",
            "Stripe & PayPal Subscription Billing Integrations",
            "Secure Auth0 & Supabase Authentication Layers",
            "Scalable API Integrations & Admin Control Panels"
        ],
        "benefits": [
            {"title": "Rapid MVP Sprints", "text": "Get your core product to market in 6-8 weeks using pre-built modular modules."},
            {"title": "Cloud Scale Ready", "text": "Dockerized deployments optimized for AWS, Google Cloud, or DigitalOcean."}
        ],
        "tech_stack": ["React / Next.js", "Node.js (Express)", "Python (Django)", "PostgreSQL", "AWS / Docker", "Stripe API"],
        "packages": [
            {"name": "Core MVP Package", "price": "$8,000", "desc": "Launch fast and test your product concept in the real market.", "items": ["Complete Figma Prototypes", "Standard User Authentication", "1 Core Dashboard Workflow", "Stripe Billing Integration", "Deployment to AWS/Vercel"]},
            {"name": "Scale-Up SaaS", "price": "$15,000", "desc": "Perfect for established concepts adding advanced features.", "items": ["Multi-Tenant Architecture", "Custom Database Models", "Advanced Analytics Panels", "Multiple Subscription Tiers", "API Documentation & Webhooks"]},
            {"name": "Enterprise Platform", "price": "$25,000+", "desc": "Complete bespoke system with custom cloud configurations.", "items": ["High-Availability Setup", "Custom Integrations (CRM/ERP)", "SLA & Performance Monitoring", "Dedicated Sprint Team", "Ongoing Monthly Maintenance"]}
        ]
    },
    "frontend-development": {
        "title": "Frontend Development Services",
        "tagline": "Pixel-Perfect Frontend Engineering & Interactive UIs",
        "description": "Transform static design mockups into interactive, fast-loading, and responsive web applications. We specialize in building clean, component-based user interfaces in React and Next.js, matching your Figma specifications to the pixel while ensuring accessibility (WCAG) and smooth micro-animations.",
        "hero_image": "/assets/frontend-development.png",
        "starting_price": "$1,499 flat rate",
        "bullets": [
            "Figma / Adobe XD to Pixel-Perfect HTML & React",
            "Responsive & Mobile-First Component Frameworks",
            "Core Web Vitals & Loading Optimization",
            "Smooth Framer Motion & CSS Animations"
        ],
        "benefits": [
            {"title": "WCAG Accessible", "text": "Semantically coded elements ensuring compliance with web accessibility standards."},
            {"title": "Optimized Bundles", "text": "Clean module structure, lazy loading, and tree-shaking for high PageSpeed."}
        ],
        "tech_stack": ["React.js", "Next.js", "Vue.js", "TypeScript", "Tailwind CSS", "Figma integration"],
        "packages": [
            {"name": "Single Page UI", "price": "$1,499", "desc": "Highly interactive page built with React or Next.js.", "items": ["1 Custom Responsive View", "Figma to Code Transition", "Interactive JavaScript Components", "Tailwind CSS Styling", "AOS / Motion Animations"]},
            {"name": "Full App Frontend", "price": "$3,499", "desc": "Ideal for developers needing a ready UI for their backend API.", "items": ["Up to 12 Distinct Pages", "Next.js Framework Routing", "Global State Management", "Component Library Integration", "Form Validation & APIs Connected"]},
            {"name": "Custom UI System", "price": "$6,000+", "desc": "Complete frontend build for complex dashboards and SaaS apps.", "items": ["Interactive Data Visualization", "Complex Admin Layouts", "Dark/Light Mode Systems", "Custom Theme Styling", "Comprehensive Cross-Browser Testing"]}
        ]
    },
    "backend-development": {
        "title": "Backend Development Services",
        "tagline": "Scalable Backend Systems, APIs & Secure Infrastructures",
        "description": "Power your web applications with secure databases, optimized servers, and lightning-fast APIs. We design backend architectures that handle heavy traffic volumes, manage secure user sessions, interface with databases efficiently, and integrate seamlessly with third-party software.",
        "hero_image": "/assets/backend-development.png",
        "starting_price": "$2,499 package",
        "bullets": [
            "RESTful & GraphQL API Architecture",
            "Relational & Document Databases (Postgres, MongoDB)",
            "Secure Session Control & JWT Authentication",
            "Background Workers & Caching (Redis, Celery)"
        ],
        "benefits": [
            {"title": "Database Tuned", "text": "Expert query optimizations, indexing, and connection pools for high load."},
            {"title": "Ironclad Security", "text": "Encrypted credentials, SQL injection blocks, and sanitization protocols."}
        ],
        "tech_stack": ["Node.js / NestJS", "Python (FastAPI)", "PHP (Laravel)", "PostgreSQL / MongoDB", "Redis / Memcached", "Docker / K8s"],
        "packages": [
            {"name": "API Service Node", "price": "$2,499", "desc": "Custom backend server representing isolated APIs.", "items": ["REST API Architecture", "User Authorization System", "Database Integration (1 engine)", "Standard Unit Tests", "Deploy Setup (Render/Docker)"]},
            {"name": "Database & Sync Server", "price": "$4,999", "desc": "Ideal for sync-heavy portals and transactional systems.", "items": ["Complex Relational Models", "Background Worker Queues", "Third-Party Data Syncing", "Caching Layer Integration", "Performance Load Auditing"]},
            {"name": "Scalable Infrastructure", "price": "$9,999+", "desc": "Bespoke backend architecture ready for global scale.", "items": ["Microservices Setup", "Kubernetes Configurations", "High-Availability Clusters", "Advanced Security Hardening", "Documentation & SDK Generation"]}
        ]
    },
    "ui-ux-design": {
        "title": "UI/UX Design Services",
        "tagline": "User-Centered Figma Design Systems That Convert",
        "description": "Unlock better user retention, higher conversions, and premium brand aesthetics. We specialize in researching user journeys, wireframing product layouts, and creating detailed Figma design systems. You get high-fidelity interactive prototypes that show exactly how the site will behave before a single line of code is written.",
        "hero_image": "/assets/ui-ux-design.png",
        "starting_price": "$999 flat rate",
        "bullets": [
            "In-depth User Research & Persona Identification",
            "High-Fidelity Wireframes & Interactive Prototypes",
            "Bespoke Figma Design Systems & Style Guides",
            "UX Audits & Usability Optimizations"
        ],
        "benefits": [
            {"title": "Agile Iterations", "text": "Rapid feedback sprints allowing you to test interactions before coding."},
            {"title": "Developer Hand-off", "text": "Clean spacing specs, components structure, and assets organized for devs."}
        ],
        "tech_stack": ["Figma", "Adobe Creative Suite", "Wireframing", "User Testing", "Interactive Prototypes", "A/B Layout Maps"],
        "packages": [
            {"name": "Bespoke UI Design", "price": "$999", "desc": "Perfect prototype design for simple apps or landing funnels.", "items": ["Figma Style Assets Guide", "Landing Page Layout Design", "Interactive Clickable Prototypes", "2 Iteration Feedback Rounds", "All Assets Handed Over"]},
            {"name": "Standard App Design", "price": "$2,499", "desc": "Complete layouts for mobile apps or core corporate sites.", "items": ["Up to 10 Distinct Layouts", "Comprehensive User Flow Diagrams", "Component Figma Library", "Clickable High-Fidelity Demos", "Full UI Kit Asset Export"]},
            {"name": "Product Design System", "price": "$4,999+", "desc": "Ideal for complex SaaS platforms and enterprise tools.", "items": ["Full Design Audit", "Multi-State Components Kits", "Interactive Micro-Interactions", "Collaboration Sprints", "Design-to-Code Support"]}
        ]
    },
    "mobile-app-development": {
        "title": "Mobile App Development Company",
        "tagline": "Bespoke Hybrid & Native Mobile Apps",
        "description": "Bring your product to the App Store and Google Play. We develop high-performance cross-platform mobile apps using React Native and Flutter, allowing you to run a single codebase on both iOS and Android. We manage the entire lifecycle, from design and API connections to app store review publication.",
        "hero_image": "/assets/mobile-app-development.png",
        "starting_price": "$9,999 package",
        "bullets": [
            "React Native & Flutter Cross-Platform Development",
            "Push Notifications & Deep Linking Configurations",
            "Offline Syncing & SQLite Local Storage",
            "App Store & Google Play Publication Support"
        ],
        "benefits": [
            {"title": "Native Performance", "text": "Optimized rendering layers ensuring smooth 60fps transitions and animations."},
            {"title": "Device Integration", "text": "Bespoke integrations with GPS, cameras, biometric locks, and contacts."}
        ],
        "tech_stack": ["React Native", "Flutter", "TypeScript / Dart", "Swift / Kotlin", "Firebase Services", "App Store Connect"],
        "packages": [
            {"name": "Mobile MVP App", "price": "$9,999", "desc": "Launch your core mobile features quickly and test concepts.", "items": ["iOS & Android Builds (1 codebase)", "User Sign Up & Login", "2 Core Workflow Screens", "Firebase Push Notifications", "App Store Submission Support"]},
            {"name": "Full Custom App", "price": "$17,999", "desc": "Comprehensive application with deep database integrations.", "items": ["Custom Interactive UI/UX", "Offline Data Caching", "Biometric Lock (Face/Touch ID)", "Payment Gateway Connection", "Full Analytics & Event Logs"]},
            {"name": "Enterprise Mobile Platform", "price": "$29,999+", "desc": "Complex enterprise tools with dedicated SLA backups.", "items": ["Native Modules Custom Code", "Real-Time Sync Systems", "Deep Link Integrations", "Security Penetration Auditing", "Ongoing Performance Support"]}
        ]
    },
    "api-development": {
        "title": "API Development & Integration",
        "tagline": "Custom API Integrations & Middleware Sync Tools",
        "description": "Connect your business systems and automate redundant tasks. We write secure web middleware and custom API synchronization tools to integrate CRM, billing, logistics, and sales platforms (like Salesforce, HubSpot, Stripe, Shopify, and Zoho) so your data stays synchronized in real time.",
        "hero_image": "/assets/api-development.png",
        "starting_price": "$1,299 flat rate",
        "bullets": [
            "Third-Party CRM / Payment Gateway Integrations",
            "Custom Middleware & Webhook Receivers",
            "API Authentication Hardening (OAuth2, Key Management)",
            "Automated ETL Sync Pipelines"
        ],
        "benefits": [
            {"title": "Error-Handling", "text": "Robust fallback retry mechanisms preventing sync drops during outages."},
            {"title": "Fully Documented", "text": "Comprehensive interactive Swagger/Postman documentation for simple handoffs."}
        ],
        "tech_stack": ["REST / JSON", "GraphQL", "Node.js", "Python / FastAPI", "OAuth 2.0 / Webhooks", "Swagger / OpenAPI"],
        "packages": [
            {"name": "Single Integration", "price": "$1,299", "desc": "Connect two third-party platforms together safely.", "items": ["Stripe, HubSpot, or Salesforce Connection", "Bespoke Sync Webhooks", "Error Logging Dashboard", "Secure API Key Management", "30-Day Support Guarantee"]},
            {"name": "Custom API Server", "price": "$3,499", "desc": "Custom server hosting API endpoints for your apps.", "items": ["REST or GraphQL Architecture", "OAuth2 Authentication Layer", "PostgreSQL Database Model", "Swagger API Documentation", "Performance Optimization Setup"]},
            {"name": "Enterprise Sync Hub", "price": "$7,999+", "desc": "Ideal for syncing multiple CRM, ERP, and payment databases.", "items": ["Real-Time Event Hub", "Multi-Source ETL Pipeline", "Advanced Queue Management", "Security Log Auditing", "2 Years Active Maintenance"]}
        ]
    },
    "website-maintenance": {
        "title": "Website Maintenance & Support Plans",
        "tagline": "Keep Your Website Secure, Fast, and Updated",
        "description": "Ensure your online presence remains secure, functional, and fully optimized. Our monthly retainer plans cover core updates, performance audits, security patching, cloud backup management, and priority content changes so you never have to worry about downtime or bugs.",
        "hero_image": "/assets/performance-monitoring-ui.webp",
        "starting_price": "$99/mo",
        "bullets": [
            "Weekly WordPress / Plugin / Core System Updates",
            "Automated Daily Cloud Backups (Off-site Restores)",
            "Active Uptime Monitoring (24/7/365 Alerts)",
            "Priority Support Hours for Content Revisions"
        ],
        "benefits": [
            {"title": "Malware Removal", "text": "Immediate isolation and cleanup in the event of security compromise."},
            {"title": "Monthly Reports", "text": "Detailed analytics, updates logs, speed scores, and recommendations."}
        ],
        "tech_stack": ["LiteSpeed Cache", "Security Firewalls", "Automated Backups", "Uptime Monitors", "CDN Configs", "Core updates"],
        "packages": [
            {"name": "Starter Plan", "price": "$99/mo", "desc": "Perfect for simple informational business websites.", "items": ["Weekly Plugin & Core Updates", "Daily Cloud Backups", "24/7 Security Scanning", "1 Hour Support / mo", "Email Support Response < 24h"]},
            {"name": "Professional Plan", "price": "$199/mo", "desc": "Ideal for blogs, directories, and high-traffic sites.", "items": ["Priority Updates & Testing", "Real-Time Security Firewalls", "Uptime Monitoring Alerts", "3 Hours Support / mo", "Priority Response < 12h"]},
            {"name": "Enterprise Retainer", "price": "$499/mo", "desc": "Essential for e-commerce stores and custom web apps.", "items": ["Daily Database Optimization", "Staging Environment Testing", "Core Web Vitals Tuning", "10 Hours Support / mo", "Priority Response < 4h"]}
        ]
    }
}

process_steps = [
    {"num": "1", "name": "Discovery & Scope", "text": "We outline your user personas, database schemas, and integration points to create a comprehensive project blueprint."},
    {"num": "2", "name": "UI/UX Prototyping", "text": "Our designers build clickable Figma wireframes so you can verify interactive elements before coding starts."},
    {"num": "3", "name": "Agile Sprints", "text": "Our engineering team writes clean, component-based code in weekly sprints, providing live demo environments."},
    {"num": "4", "name": "QA, Launch & Handoff", "text": "We run extensive cross-device tests, optimize speed scores, launch on secure hosting, and transfer ownership."}
]

def generate_body_html(data):
    # Overview & Benefits
    bullets_html = "\n".join([f'<div class="flex items-center gap-2.5"><span class="material-symbols-outlined text-primary text-sm font-bold">check_circle</span> <span>{b}</span></div>' for b in data['bullets']])
    benefits_html = ""
    for ben in data['benefits']:
        benefits_html += f"""                    <div class="bg-slate-50 p-6 rounded-3xl border border-slate-100/80 shadow-sm">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">{ben['title']}</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">{ben['text']}</p>
                    </div>\n"""
                    
    # Tech Stack
    tech_stack_badges = "".join([f'<span class="px-4 py-2 bg-[#f2ebfa] text-primary text-xs font-bold rounded-full border border-slate-200/50 hover:scale-105 transition-transform">{tech}</span>' for tech in data['tech_stack']])
    
    # Process steps
    process_html = ""
    for step in process_steps:
        process_html += f"""                <div class="bg-white p-8 rounded-[2rem] border border-slate-100 shadow-sm relative group hover:shadow-lg transition-all duration-300">
                    <div class="w-12 h-12 rounded-xl bg-primary/10 text-primary flex items-center justify-center font-black text-lg mb-6 group-hover:scale-110 transition-transform">{step['num']}</div>
                    <h3 class="text-lg font-bold mb-3">{step['name']}</h3>
                    <p class="text-slate-500 text-xs leading-relaxed">{step['text']}</p>
                </div>\n"""
                
    # Packages
    packages_html = ""
    for idx, pkg in enumerate(data['packages']):
        is_featured = idx == 1
        card_class = "bg-[#111c2d] text-white border-primary shadow-xl scale-105" if is_featured else "bg-white text-slate-800 border-slate-100 shadow-sm"
        badge = '<span class="inline-block px-3 py-1 bg-primary text-white text-[9px] font-black uppercase rounded-full mb-4">RECOMMENDED</span><br>' if is_featured else ''
        title_class = "text-white" if is_featured else "text-[#111c2d]"
        price_class = "text-indigo-400" if is_featured else "text-primary"
        desc_class = "text-slate-300" if is_featured else "text-slate-500"
        item_icon_color = "text-indigo-400" if is_featured else "text-primary"
        item_text_color = "text-slate-200" if is_featured else "text-slate-600"
        btn_class = "bg-primary text-white hover:bg-primary-container" if is_featured else "bg-slate-100 hover:bg-slate-200 text-slate-800"
        
        items_list_html = "".join([f'<li class="flex items-center gap-2.5"><span class="material-symbols-outlined {item_icon_color} text-sm">check</span> <span class="{item_text_color} text-xs">{item}</span></li>' for item in pkg['items']])
        
        packages_html += f"""            <div class="rounded-[2.5rem] border p-8 flex flex-col justify-between {card_class} transition-all duration-500 relative z-10">
                <div>
                    {badge}
                    <h3 class="text-xl font-bold mb-2 {title_class}">{pkg['name']}</h3>
                    <div class="text-3xl font-black mb-3 {price_class}">{pkg['price']}<span class="text-xs font-semibold">{"/mo" if "Maintenance" in data['title'] else " starting"}</span></div>
                    <p class="text-xs leading-relaxed mb-6 {desc_class}">{pkg['desc']}</p>
                    <div class="h-px bg-slate-200/20 my-6"></div>
                    <ul class="space-y-3">
                        {items_list_html}
                    </ul>
                </div>
                <div class="mt-8">
                    <a href="/get-a-quote/" class="block w-full py-4 text-center rounded-xl font-bold text-xs transition-all {btn_class}">Choose plan</a>
                </div>
            </div>\n"""

    body_html = f"""
    <!-- Service Overview & Benefits -->
    <section class="py-24 bg-white relative">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="grid lg:grid-cols-2 gap-16 items-center mb-20">
                <div data-aos="fade-right">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-6 leading-tight">Fast, Responsive &amp; Conversion-Focused</h2>
                    <p class="text-slate-500 text-base mb-8 leading-relaxed">{data['description']}</p>
                    <div class="space-y-4 text-sm font-bold text-slate-700">
                        {bullets_html}
                    </div>
                </div>
                <div class="grid sm:grid-cols-2 gap-6" data-aos="fade-left">
                    {benefits_html}
                </div>
            </div>
        </div>
    </section>

    <!-- Technologies & Tech Stack -->
    <section class="py-16 bg-slate-50 border-y border-slate-200/50">
        <div class="max-w-[1440px] mx-auto px-6 text-center">
            <h3 class="text-xs font-black uppercase tracking-wider text-slate-400 mb-6">Expertise &amp; Technology Stack</h3>
            <div class="flex flex-wrap justify-center gap-3">
                {tech_stack_badges}
            </div>
        </div>
    </section>

    <!-- Interactive Development Process -->
    <section class="py-24 bg-white">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="text-center mb-16" data-aos="fade-up">
                <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-primary/5 text-primary text-xs font-black uppercase rounded-full mb-4">OUR WORKFLOW</span>
                <h2 class="text-3xl md:text-5xl font-black text-[#111c2d] mb-4 font-h2">How We Work</h2>
                <p class="text-slate-500 text-base max-w-xl mx-auto">We follow a structured, collaborative engineering process to deliver code on time and on budget.</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8" data-aos="fade-up">
                {process_html}
            </div>
        </div>
    </section>

    <!-- Pricing Packages -->
    <section class="py-24 bg-slate-50 border-t border-slate-100">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="text-center mb-16" data-aos="fade-up">
                <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-primary/5 text-primary text-xs font-black uppercase rounded-full mb-4">PRICING PLANS</span>
                <h2 class="text-3xl md:text-5xl font-black text-[#111c2d] mb-4 font-h2">Starting Project Packages</h2>
                <p class="text-slate-500 text-base max-w-xl mx-auto">Transparent, flat-rate pricing to fit your phase of business. Choose a plan or request a custom estimate.</p>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto" data-aos="fade-up">
                {packages_html}
            </div>
        </div>
    </section>
"""
    return body_html

def update_file(file_name, data):
    file_path = f"services/{file_name}/index.html"
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} - not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace Hero Content (line-by-line replacement or regex)
    # Let's replace title & subtitle and image in the hero section
    # Title & subtitle:
    title_pattern = r'<h1 class="font-h1 text-4xl sm:text-5xl lg:text-6xl text-white mb-6 leading-tight font-black">.*?</h1>'
    tagline_pattern = r'<p class="font-body-lg text-body-lg text-white/70 max-w-xl mb-12">.*?</p>'
    img_pattern = r'<img src="/assets/secure-enterprise-hosting.webp" alt=".*?" class="rounded-\[40px\] shadow-2xl max-w-md mx-auto" decoding="async" loading="lazy">'
    
    new_title = f'<h1 class="font-h1 text-4xl sm:text-5xl lg:text-6xl text-white mb-6 leading-tight font-black">{data["title"]}</h1>'
    new_tagline = f'<p class="font-body-lg text-body-lg text-white/70 max-w-xl mb-12">{data["tagline"]}. Packages start at {data["starting_price"]}.</p>'
    new_img = f'<img src="{data["hero_image"]}" alt="{data["title"]}" class="rounded-[40px] shadow-2xl max-w-md mx-auto" decoding="async" loading="lazy">'
    
    content = re.sub(title_pattern, new_title, content)
    content = re.sub(tagline_pattern, new_tagline, content)
    content = re.sub(img_pattern, new_img, content)

    # Replace Body Content
    start_marker = "<!-- Service Body Content -->"
    end_marker = "<!-- FAQ Section -->"
    
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)
    
    if start_pos != -1 and end_pos != -1:
        new_body = generate_body_html(data)
        updated_content = content[:start_pos + len(start_marker)] + new_body + "\n        " + content[end_pos:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Enriched content for {file_path}")
    else:
        print(f"Could not find body content markers in {file_path}")

def main():
    for file_name, data in services_data.items():
        update_file(file_name, data)

if __name__ == '__main__':
    main()
