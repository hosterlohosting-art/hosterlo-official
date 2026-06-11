import os
import json

def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Shared HTML head wrapper
def get_head(title, description, canonical_url, schema_json):
    return f"""<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <link rel="icon" type="image/png" href="/favicon.png">
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="theme-color" content="#4f17ce">
    <meta name="format-detection" content="telephone=yes">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="author" content="Hosterlo">
    <link rel="canonical" href="{canonical_url}">
    <meta property="og:locale" content="en_US">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Hosterlo">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://hosterlo.com/assets/secure-enterprise-hosting.webp">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="https://hosterlo.com/assets/secure-enterprise-hosting.webp">
    
    <script type="application/ld+json">
    {schema_json}
    </script>
    
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script id="tailwind-config">
      tailwind.config = {{
        darkMode: "class",
        theme: {{
          extend: {{
            "colors": {{
                    "secondary-container": "#6860ef",
                    "surface-container-high": "#dee8ff",
                    "surface-dim": "#cfdaf2",
                    "surface-variant": "#d8e3fb",
                    "surface-container-low": "#f0f3ff",
                    "secondary": "#4e45d5",
                    "tertiary-container": "#596267",
                    "on-tertiary-fixed": "#141d21",
                    "surface-tint": "#6439e3",
                    "surface-container-lowest": "#ffffff",
                    "on-tertiary-fixed-variant": "#3f484d",
                    "on-error": "#ffffff",
                    "outline": "#797487",
                    "surface-container-highest": "#d8e3fb",
                    "background": "#f9f9ff",
                    "primary": "#4f17ce",
                    "on-primary": "#ffffff",
                    "on-background": "#111c2d",
                    "tertiary-fixed": "#dbe4ea",
                    "tertiary-fixed-dim": "#bfc8ce",
                    "primary-container": "#673de6",
                    "inverse-on-surface": "#ecf1ff",
                    "inverse-surface": "#263143",
                    "primary-fixed-dim": "#ccbeff",
                    "on-primary-fixed-variant": "#4c10cc",
                    "on-secondary-fixed": "#100069",
                    "error": "#ba1a1a",
                    "inverse-primary": "#ccbeff",
                    "surface-bright": "#f9f9ff",
                    "on-secondary": "#ffffff",
                    "on-primary-container": "#e1d7ff",
                    "on-secondary-fixed-variant": "#372abf",
                    "on-error-container": "#93000a",
                    "on-secondary-container": "#fffbff",
                    "on-primary-fixed": "#1e0060",
                    "tertiary": "#414a4f",
                    "on-surface": "#111c2d",
                    "primary-fixed": "#e7deff",
                    "on-tertiary-container": "#d4dde3",
                    "surface": "#f9f9ff",
                    "secondary-fixed-dim": "#c3c0ff",
                    "surface-container": "#e7eeff",
                    "on-tertiary": "#ffffff",
                    "outline-variant": "#cac3d8",
                    "on-surface-variant": "#484455",
                    "secondary-fixed": "#e3dfff",
                    "error-container": "#ffdad6"
            }},
            "borderRadius": {{
                    "DEFAULT": "0.25rem",
                    "lg": "0.5rem",
                    "xl": "0.75rem",
                    "full": "9999px"
            }},
            "spacing": {{
                    "md": "24px",
                    "xs": "4px",
                    "lg": "48px",
                    "gutter": "24px",
                    "base": "8px",
                    "sm": "12px",
                    "container-max": "1440px",
                    "xl": "80px"
            }},
            "fontFamily": {{
                    "h3": ["Outfit", "sans-serif"],
                    "body-sm": ["Plus Jakarta Sans", "sans-serif"],
                    "body-md": ["Plus Jakarta Sans", "sans-serif"],
                    "h1": ["Outfit", "sans-serif"],
                    "body-lg": ["Plus Jakarta Sans", "sans-serif"],
                    "label-caps": ["Plus Jakarta Sans", "sans-serif"],
                    "h2": ["Outfit", "sans-serif"]
            }},
            "fontSize": {{
                    "h3": ["20px", {{"lineHeight": "1.4", "fontWeight": "700", "letterSpacing": "-0.01em"}}],
                    "body-sm": ["14px", {{"lineHeight": "1.6", "fontWeight": "400"}}],
                    "body-md": ["16px", {{"lineHeight": "1.6", "fontWeight": "400"}}],
                    "h1": ["42px", {{"lineHeight": "1.15", "letterSpacing": "-0.03em", "fontWeight": "800"}}],
                    "body-lg": ["17px", {{"lineHeight": "1.6", "fontWeight": "400"}}],
                    "label-caps": ["11px", {{"lineHeight": "1", "letterSpacing": "0.15em", "fontWeight": "700"}}],
                    "h2": ["32px", {{"lineHeight": "1.2", "letterSpacing": "-0.02em", "fontWeight": "800"}}]
            }}
          }},
        }},
      }}
    </script>

    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
    <style>
        body {{
            font-family: "Plus Jakarta Sans", sans-serif !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-family: "Outfit", sans-serif !important;
        }}
        .button-shine {{
            position: relative;
            overflow: hidden;
        }}
        .button-shine::after {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
            transform: rotate(45deg);
            transition: 0.7s;
            opacity: 0;
        }}
        .button-shine:hover::after {{
            left: 100%;
            top: 100%;
            opacity: 1;
        }}
        .glass-card {{
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(226, 232, 240, 0.6);
        }}
        .progress-bar {{
            height: 4px;
            background: #4f17ce;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 100;
            width: 0%;
            transition: width 0.1s ease-out;
        }}
        .nav-link {{
            position: relative;
            font-weight: 500;
            color: #484455;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
        }}
        .nav-link:hover {{
            color: #4f17ce;
        }}
    </style>
</head>
<body class="bg-[#f9f9ff] text-[#111c2d] font-body-md overflow-x-hidden">
    <div class="progress-bar" id="progress-bar"></div>
    
    <!-- TopNavBar -->
    <header class="sticky top-4 w-full z-50 px-4 sm:px-6 lg:px-8">
        <!-- Placeholder: Synchronized by sync_branding.py -->
    </header>

    <!-- Mobile Menu Overlay -->
    <div id="mobile-menu-overlay" class="hidden">
        <!-- Placeholder: Synchronized by sync_branding.py -->
    </div>
"""

def get_foot():
    return """
    <!-- Footer -->
    <footer class="w-full bg-[#f8f6fc] border-t border-slate-200/50 pt-24 pb-16 text-slate-900 relative overflow-hidden">
        <!-- Placeholder: Synchronized by sync_branding.py -->
    </footer>

    <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            AOS.init({
                duration: 800,
                once: true
            });
            
            // Progress Bar
            window.addEventListener("scroll", function () {
                const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                document.getElementById("progress-bar").style.width = scrolled + "%";
            });
        });
    </script>
</body>
</html>
"""

# ----------------- SERVICES HUB PAGE -----------------
def generate_services_hub():
    schema = """{
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Organization",
          "@id": "https://hosterlo.com/#organization",
          "name": "Hosterlo",
          "url": "https://hosterlo.com/",
          "logo": {
            "@type": "ImageObject",
            "url": "https://hosterlo.com/assets/logo.png"
          }
        },
        {
          "@type": "WebSite",
          "@id": "https://hosterlo.com/#website",
          "url": "https://hosterlo.com/",
          "name": "Hosterlo"
        },
        {
          "@type": "WebPage",
          "@id": "https://hosterlo.com/services/#webpage",
          "url": "https://hosterlo.com/services/",
          "name": "Web Development & Digital Agency Services | Hosterlo",
          "isPartOf": {
            "@id": "https://hosterlo.com/#website"
          }
        }
      ]
    }"""
    
    body = """
    <main>
        <!-- Hero Section -->
        <section class="relative min-h-[75vh] flex items-center overflow-hidden bg-gradient-to-br from-[#0f0a1e] via-[#1a1145] to-[#2d1b69] text-white -mt-[96px] pt-32 pb-20">
            <div class="absolute inset-0">
                <div class="hero-grid-pattern absolute inset-0 opacity-[0.2]"></div>
            </div>
            <div class="max-w-[1440px] mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center w-full relative z-10">
                <div class="text-left" data-aos="fade-right">
                    <span class="inline-block font-label-caps text-indigo-400 px-4 py-1.5 bg-white/5 rounded-full mb-6 uppercase">From Hosting to Full-Stack Development</span>
                    <h1 class="font-h1 text-4xl sm:text-5xl lg:text-6xl text-white mb-6 leading-tight font-black">Launch, Build & Scale Your Digital Presence</h1>
                    <p class="font-body-lg text-body-lg text-white/70 max-w-xl mb-12">Launch with our reliable high-speed web hosting. Scale with our world-class custom development and design agency team. One trusted partner for your entire software journey.</p>
                    <div class="flex flex-wrap gap-4">
                        <a href="/get-a-quote/" class="button-shine inline-block px-8 py-4 bg-primary text-white rounded-2xl font-bold shadow-lg shadow-primary/20 hover:scale-105 transition-all text-center">Get a Free Project Quote</a>
                        <a href="#services-grid" class="px-8 py-4 bg-white/10 text-white hover:bg-white/20 rounded-2xl font-bold transition-all text-center">Explore Our Services</a>
                    </div>
                </div>
                <div class="hidden lg:block relative" data-aos="fade-left">
                    <img src="/assets/secure-enterprise-hosting.webp" alt="Hosterlo Digital Agency Team" class="rounded-[40px] shadow-2xl max-w-md mx-auto" decoding="async" loading="lazy">
                </div>
            </div>
        </section>

        <!-- Services Grid Section -->
        <section id="services-grid" class="py-24 bg-white relative">
            <div class="max-w-[1440px] mx-auto px-6">
                <div class="text-center mb-20" data-aos="fade-up">
                    <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-primary/5 text-primary text-xs font-black uppercase rounded-full mb-4">WHAT WE BUILD</span>
                    <h2 class="text-3xl md:text-5xl font-black text-slate-900 mb-4 font-h2">Our Agency Capabilities</h2>
                    <p class="text-slate-500 text-base max-w-2xl mx-auto">We engineer high-performance web products, scalable backend systems, custom APIs, and stunning user interfaces.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                    <!-- Service 1: Web Development -->
                    <div class="bg-slate-50 border border-slate-100 rounded-3xl p-8 hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col h-full" data-aos="fade-up">
                        <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-6">
                            <span class="material-symbols-outlined text-2xl">web</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3">Web Development</h3>
                        <p class="text-slate-500 text-sm leading-relaxed mb-6">Custom web development, bespoke WordPress themes, corporate portals, and e-commerce stores optimized for speed and SEO.</p>
                        <div class="mt-auto">
                            <span class="text-xs text-primary font-bold block mb-4">Starting at $999</span>
                            <a href="/services/web-development/" class="text-primary font-bold text-sm flex items-center gap-1 hover:underline">Learn More <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a>
                        </div>
                    </div>

                    <!-- Service 2: SaaS Development -->
                    <div class="bg-slate-50 border border-slate-100 rounded-3xl p-8 hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col h-full" data-aos="fade-up" data-aos-delay="100">
                        <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-6">
                            <span class="material-symbols-outlined text-2xl">layers</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3">SaaS Development</h3>
                        <p class="text-slate-500 text-sm leading-relaxed mb-6">Full-scale multi-tenant SaaS products, MVPs, admin dashboards, and custom subscription systems wired to Stripe.</p>
                        <div class="mt-auto">
                            <span class="text-xs text-primary font-bold block mb-4">Starting at $9,999</span>
                            <a href="/services/saas-development/" class="text-primary font-bold text-sm flex items-center gap-1 hover:underline">Learn More <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a>
                        </div>
                    </div>

                    <!-- Service 3: Frontend Development -->
                    <div class="bg-slate-50 border border-slate-100 rounded-3xl p-8 hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col h-full" data-aos="fade-up" data-aos-delay="200">
                        <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-6">
                            <span class="material-symbols-outlined text-2xl">code</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3">Frontend Engineering</h3>
                        <p class="text-slate-500 text-sm leading-relaxed mb-6">Pixel-perfect, interactive frontend applications built in React.js, Next.js, and Vue.js with absolute responsiveness.</p>
                        <div class="mt-auto">
                            <span class="text-xs text-primary font-bold block mb-4">Hourly / Fixed Pricing</span>
                            <a href="/services/frontend-development/" class="text-primary font-bold text-sm flex items-center gap-1 hover:underline">Learn More <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a>
                        </div>
                    </div>

                    <!-- Service 4: Backend Development -->
                    <div class="bg-slate-50 border border-slate-100 rounded-3xl p-8 hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col h-full" data-aos="fade-up" data-aos-delay="300">
                        <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-6">
                            <span class="material-symbols-outlined text-2xl">terminal</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3">Backend Engineering</h3>
                        <p class="text-slate-500 text-sm leading-relaxed mb-6">Secure, scalable server architectures, database modeling, authentication systems, and cloud infrastructure management.</p>
                        <div class="mt-auto">
                            <span class="text-xs text-primary font-bold block mb-4">Hourly / Fixed Pricing</span>
                            <a href="/services/backend-development/" class="text-primary font-bold text-sm flex items-center gap-1 hover:underline">Learn More <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a>
                        </div>
                    </div>

                    <!-- Service 5: UI/UX Design -->
                    <div class="bg-slate-50 border border-slate-100 rounded-3xl p-8 hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col h-full" data-aos="fade-up">
                        <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-6">
                            <span class="material-symbols-outlined text-2xl">design_services</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3">UI/UX Design</h3>
                        <p class="text-slate-500 text-sm leading-relaxed mb-6">User research, wireframing, high-fidelity UI design in Figma, and complete usability audits for existing apps.</p>
                        <div class="mt-auto">
                            <span class="text-xs text-primary font-bold block mb-4">Starting at $1,499</span>
                            <a href="/services/ui-ux-design/" class="text-primary font-bold text-sm flex items-center gap-1 hover:underline">Learn More <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a>
                        </div>
                    </div>

                    <!-- Service 6: Mobile Apps -->
                    <div class="bg-slate-50 border border-slate-100 rounded-3xl p-8 hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col h-full" data-aos="fade-up" data-aos-delay="100">
                        <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-6">
                            <span class="material-symbols-outlined text-2xl">phone_iphone</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3">Mobile App Dev</h3>
                        <p class="text-slate-500 text-sm leading-relaxed mb-6">Cross-platform native mobile applications for iOS and Android built on React Native and Flutter frameworks.</p>
                        <div class="mt-auto">
                            <span class="text-xs text-primary font-bold block mb-4">Starting at $14,999</span>
                            <a href="/services/mobile-app-development/" class="text-primary font-bold text-sm flex items-center gap-1 hover:underline">Learn More <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a>
                        </div>
                    </div>

                    <!-- Service 7: API Development -->
                    <div class="bg-slate-50 border border-slate-100 rounded-3xl p-8 hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col h-full" data-aos="fade-up" data-aos-delay="200">
                        <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-6">
                            <span class="material-symbols-outlined text-2xl">api</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3">API Integrations</h3>
                        <p class="text-slate-500 text-sm leading-relaxed mb-6">Bespoke REST and GraphQL API engineering, database synchronizations, CRM/ERP hooks, and payment gateway systems.</p>
                        <div class="mt-auto">
                            <span class="text-xs text-primary font-bold block mb-4">Starting at $1,499</span>
                            <a href="/services/api-development/" class="text-primary font-bold text-sm flex items-center gap-1 hover:underline">Learn More <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a>
                        </div>
                    </div>

                    <!-- Service 8: Website Maintenance -->
                    <div class="bg-slate-50 border border-slate-100 rounded-3xl p-8 hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col h-full" data-aos="fade-up" data-aos-delay="300">
                        <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-6">
                            <span class="material-symbols-outlined text-2xl">build</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3">Website Maintenance</h3>
                        <p class="text-slate-500 text-sm leading-relaxed mb-6">Monthly retainer plans covering security updates, server backups, plugin audits, speed optimization, and support.</p>
                        <div class="mt-auto">
                            <span class="text-xs text-primary font-bold block mb-4">Starting at $99/mo</span>
                            <a href="/services/website-maintenance/" class="text-primary font-bold text-sm flex items-center gap-1 hover:underline">Learn More <span class="material-symbols-outlined text-[16px]">arrow_forward</span></a>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Our Process Section -->
        <section class="py-24 bg-slate-50 border-t border-slate-100 relative overflow-hidden">
            <div class="max-w-[1440px] mx-auto px-6 relative z-10">
                <div class="text-center mb-20" data-aos="fade-up">
                    <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-primary/5 text-primary text-xs font-black uppercase rounded-full mb-4">HOW WE WORK</span>
                    <h2 class="text-3xl md:text-5xl font-black text-slate-900 mb-4 font-h2">The Hosterlo Process</h2>
                    <p class="text-slate-500 text-base max-w-2xl mx-auto">We follow a rigorous, agile process to take your software requirements from initial whiteboard doodles to a live, scalable production build.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8" data-aos="fade-up">
                    <!-- Step 1 -->
                    <div class="relative bg-white border border-slate-200 p-8 rounded-3xl shadow-sm">
                        <div class="absolute -top-6 left-8 w-12 h-12 rounded-full bg-primary text-white font-black flex items-center justify-center shadow-lg">1</div>
                        <h3 class="text-lg font-extrabold text-[#111c2d] mt-2 mb-3">Discovery & Strategy</h3>
                        <p class="text-slate-500 text-sm leading-relaxed">We hold collaborative calls to understand your business objectives, target audience, budget boundaries, and technology stack choices.</p>
                    </div>

                    <!-- Step 2 -->
                    <div class="relative bg-white border border-slate-200 p-8 rounded-3xl shadow-sm">
                        <div class="absolute -top-6 left-8 w-12 h-12 rounded-full bg-primary text-white font-black flex items-center justify-center shadow-lg">2</div>
                        <h3 class="text-lg font-extrabold text-[#111c2d] mt-2 mb-3">UX/UI Prototyping</h3>
                        <p class="text-slate-500 text-sm leading-relaxed">We map user journeys, outline wireframes, and design interactive Figma prototypes so you can experience the product flow before coding begins.</p>
                    </div>

                    <!-- Step 3 -->
                    <div class="relative bg-white border border-slate-200 p-8 rounded-3xl shadow-sm">
                        <div class="absolute -top-6 left-8 w-12 h-12 rounded-full bg-primary text-white font-black flex items-center justify-center shadow-lg">3</div>
                        <h3 class="text-lg font-extrabold text-[#111c2d] mt-2 mb-3">Agile Development</h3>
                        <p class="text-slate-500 text-sm leading-relaxed">Our backend and frontend developers build the product in bi-weekly sprints, offering sandbox demo links to keep you aligned every step.</p>
                    </div>

                    <!-- Step 4 -->
                    <div class="relative bg-white border border-slate-200 p-8 rounded-3xl shadow-sm">
                        <div class="absolute -top-6 left-8 w-12 h-12 rounded-full bg-primary text-white font-black flex items-center justify-center shadow-lg">4</div>
                        <h3 class="text-lg font-extrabold text-[#111c2d] mt-2 mb-3">Launch & Retain</h3>
                        <p class="text-slate-500 text-sm leading-relaxed">We perform security scans and launch your product onto secure, optimized hosting, providing 30 days of free support and optional retainers.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Trust Section -->
        <section class="py-24 bg-white relative overflow-hidden">
            <div class="max-w-[1440px] mx-auto px-6 relative z-10">
                <div class="grid lg:grid-cols-2 gap-16 items-center">
                    <div data-aos="fade-right">
                        <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-primary/5 text-primary text-xs font-black uppercase rounded-full mb-4">BUILT ON TRUST</span>
                        <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-6 leading-tight font-h2">Why Partner with Hosterlo?</h2>
                        <p class="text-slate-500 text-base mb-8 leading-relaxed">Unlike anonymous freelancers or offshore white-label factories, Hosterlo operates through registered corporate entities to guarantee compliant legal support, clear milestones, and absolute security.</p>
                        
                        <div class="space-y-4 text-xs font-bold text-slate-700">
                            <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">verified_user</span> 100% Source Code Ownership Guaranteed</div>
                            <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">verified_user</span> Dedicated Local Project Managers</div>
                            <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">verified_user</span> Fully Insured & Registered Corporate Entities (US LLC, UK Ltd, PK FBR)</div>
                        </div>
                    </div>
                    <div class="grid sm:grid-cols-2 gap-6" data-aos="fade-left">
                        <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                            <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">No Vendor Lock-In</h4>
                            <p class="text-slate-500 text-xs leading-relaxed">All code is pushed to your private GitHub repository, using standard modern frameworks so any developer can manage it in the future.</p>
                        </div>
                        <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                            <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">Ongoing Infrastructure</h4>
                            <p class="text-slate-500 text-xs leading-relaxed">Since we own and operate premium server arrays, we can deploy, cache, and host your apps faster and cheaper than standard development shops.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Final CTA Section -->
        <section class="py-24 bg-white border-t border-slate-100">
            <div class="max-w-[1440px] mx-auto px-6" data-aos="fade-up">
                <div class="relative bg-gradient-to-r from-primary to-indigo-700 rounded-[36px] p-10 md:p-14 text-center text-white overflow-hidden shadow-2xl" style="background: linear-gradient(135deg, #4f17ce 0%, #31108c 100%);">
                    <div class="absolute -right-20 -top-20 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
                    <div class="relative z-10 max-w-2xl mx-auto">
                        <h2 class="text-3xl md:text-4xl font-black mb-4 font-h2">Have a Custom Project in Mind?</h2>
                        <p class="text-white/80 text-sm md:text-base mb-8">Discuss your goals with our lead systems architect. We will provide a complete project roadmap and flat-rate estimate within 24 hours.</p>
                        <div class="flex flex-col sm:flex-row gap-4 justify-center">
                            <a href="/get-a-quote/" class="px-8 py-3.5 bg-white text-primary font-bold rounded-full hover:bg-slate-50 transition-all text-sm text-center">Request a Quote</a>
                            <a href="https://wa.me/923394437730" target="_blank" rel="noopener noreferrer" class="px-8 py-3.5 border border-white/30 text-white font-semibold rounded-full hover:bg-white/10 transition-all text-sm text-center">Chat via WhatsApp</a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
    """
    
    html = get_head("Web Development & Digital Agency Services | Hosterlo", 
                    "Custom web development, SaaS product development, frontend & backend engineering, UI/UX design, and mobile apps. Get a free project quote from Hosterlo.",
                    "https://hosterlo.com/services/", schema) + body + get_foot()
    
    create_dir_if_not_exists("services")
    with open("services/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated services/index.html")


# ----------------- SERVICE DETAIL GENERATOR -----------------
def generate_service_detail_page(folder, title, subtitle, h1, body_content, faqs, starting_price, canonical, schema_str):
    faq_html = ""
    for idx, (q, a) in enumerate(faqs):
        faq_html += f"""
        <details class="group bg-white rounded-2xl border border-slate-150 shadow-sm overflow-hidden transition-all duration-300 open:border-primary/30 open:shadow-md hover:border-slate-200">
            <summary class="flex items-center justify-between p-6 cursor-pointer font-black text-[#111c2d] hover:text-primary transition-colors select-none">
                {q}
                <span class="material-symbols-outlined text-slate-400 group-open:text-primary group-open:rotate-180 transition-transform duration-300">expand_more</span>
            </summary>
            <div class="px-6 pb-6 text-slate-500 text-sm leading-relaxed border-t border-slate-50 pt-4">
                {a}
            </div>
        </details>
        """

    body = f"""
    <main>
        <!-- Hero Section -->
        <section class="relative min-h-[60vh] flex items-center overflow-hidden bg-gradient-to-br from-[#0f0a1e] via-[#1a1145] to-[#2d1b69] text-white -mt-[96px] pt-32 pb-20">
            <div class="absolute inset-0">
                <div class="hero-grid-pattern absolute inset-0 opacity-[0.2]"></div>
            </div>
            <div class="max-w-[1440px] mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center w-full relative z-10">
                <div class="text-left" data-aos="fade-right">
                    <span class="inline-block font-label-caps text-indigo-400 px-4 py-1.5 bg-white/5 rounded-full mb-6 uppercase">{subtitle}</span>
                    <h1 class="font-h1 text-4xl sm:text-5xl lg:text-6xl text-white mb-6 leading-tight font-black">{h1}</h1>
                    <p class="font-body-lg text-body-lg text-white/70 max-w-xl mb-12">{starting_price}</p>
                    <div class="flex flex-wrap gap-4">
                        <a href="/get-a-quote/" class="button-shine inline-block px-8 py-4 bg-primary text-white rounded-2xl font-bold shadow-lg shadow-primary/20 hover:scale-105 transition-all text-center">Get a Free Quote</a>
                        <a href="/services/" class="px-8 py-4 bg-white/10 text-white hover:bg-white/20 rounded-2xl font-bold transition-all text-center">Back to Services</a>
                    </div>
                </div>
                <div class="hidden lg:block relative" data-aos="fade-left">
                    <img src="/assets/secure-enterprise-hosting.webp" alt="{title}" class="rounded-[40px] shadow-2xl max-w-md mx-auto" decoding="async" loading="lazy">
                </div>
            </div>
        </section>

        <!-- Service Body Content -->
        {body_content}

        <!-- FAQ Section -->
        <section class="py-24 bg-white border-t border-slate-100 relative overflow-hidden">
            <div class="max-w-3xl mx-auto px-6 relative z-10">
                <div class="text-center mb-16" data-aos="fade-up">
                    <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-primary/5 text-primary text-xs font-black uppercase rounded-full mb-4">SERVICE FAQ</span>
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">Frequently Asked Questions</h2>
                    <p class="text-slate-500 text-sm">Everything you need to know about our {title.lower()} workflow, deliverables, and billing model.</p>
                </div>
                
                <div class="space-y-4" data-aos="fade-up">
                    {faq_html}
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="py-24 bg-slate-50 border-t border-slate-100">
            <div class="max-w-[1440px] mx-auto px-6" data-aos="fade-up">
                <div class="relative bg-gradient-to-r from-primary to-indigo-700 rounded-[36px] p-10 md:p-14 text-center text-white overflow-hidden shadow-2xl" style="background: linear-gradient(135deg, #4f17ce 0%, #31108c 100%);">
                    <div class="absolute -right-20 -top-20 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
                    <div class="relative z-10 max-w-2xl mx-auto">
                        <h2 class="text-3xl md:text-4xl font-black mb-4 font-h2">Start Your Project Today</h2>
                        <p class="text-white/80 text-sm md:text-base mb-8">Ready to bring your ideas to life? Fill out our simple quote request form and our senior project leads will schedule a free 30-minute scope consultation with you.</p>
                        <div class="flex flex-col sm:flex-row gap-4 justify-center">
                            <a href="/get-a-quote/" class="px-8 py-3.5 bg-white text-primary font-bold rounded-full hover:bg-slate-50 transition-all text-sm text-center">Request a Free Quote</a>
                            <a href="https://wa.me/923394437730" target="_blank" rel="noopener noreferrer" class="px-8 py-3.5 border border-white/30 text-white font-semibold rounded-full hover:bg-white/10 transition-all text-sm text-center">Chat with Support</a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
    """
    
    html = get_head(f"{title} | Hosterlo Services", f"{h1}. High-performance custom digital services by Hosterlo.", canonical, schema_str) + body + get_foot()
    create_dir_if_not_exists(f"services/{folder}")
    with open(f"services/{folder}/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated services/{folder}/index.html")


# ----------------- INDIVIDUAL SERVICE DETAILS CONTENT -----------------

def build_web_development():
    body = """
    <section class="py-24 bg-white relative">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="grid lg:grid-cols-2 gap-16 items-center">
                <div data-aos="fade-right">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-6 leading-tight">Fast, Responsive & Conversion-Focused Websites</h2>
                    <p class="text-slate-500 text-base mb-8 leading-relaxed">We develop custom websites from scratch, tailored to your brand identity, business workflows, and user expectations. Whether you need a corporate website, a marketing landing page, or a full-scale e-commerce store, we deliver hand-coded HTML/CSS/JS or optimized WordPress structures built to perform.</p>
                    <div class="space-y-4 text-xs font-bold text-slate-700">
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Custom WordPress Theme & Plugin Engineering</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Shopify & WooCommerce Bespoke Checkout Configurations</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Landing Page and Conversion Funnel Development</div>
                    </div>
                </div>
                <div class="grid sm:grid-cols-2 gap-6" data-aos="fade-left">
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">LiteSpeed Caching Opt</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">Every site is structured to utilize LiteSpeed caching algorithms, resulting in sub-second load times and better SEO.</p>
                    </div>
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">100% PageSpeed Score</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We write clean HTML, clean JS scripts, and use compressed modern layouts (WebP) to guarantee high Core Web Vitals.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    faqs = [
        ("How long does it take to build a custom website?", "A basic landing page or small business website takes 2-3 weeks. A complex e-commerce store or corporate portal with multiple databases takes 4-8 weeks depending on the specifications."),
        ("Will my website be mobile-friendly and optimized for Google?", "Yes, 100% of our code is mobile-first, highly responsive across all tablets and phones, and strictly adheres to modern SEO best practices for structured schema markup and fast loading speeds."),
        ("Do I own the source code and design files?", "Absolutely. Once the project invoice is cleared, we hand over 100% ownership of design assets, Figma mockups, and codebase files. We push the final files to your private GitHub repository.")
    ]
    generate_service_detail_page("web-development", "Custom Web Development Services", "Build Your Web Brand", "Custom Websites That Convert Visitors Into Customers", body, faqs, "Project packages start at $999 flat rate.", "https://hosterlo.com/services/web-development/", "{}")

def build_saas_development():
    body = """
    <section class="py-24 bg-white relative">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="grid lg:grid-cols-2 gap-16 items-center">
                <div data-aos="fade-right">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-6 leading-tight">Turn Your App Idea Into a Scaleable SaaS Business</h2>
                    <p class="text-slate-500 text-base mb-8 leading-relaxed">We architect, design, and program custom Software-as-a-Service (SaaS) products from initial MVP to production scale. Our specialized team integrates secure user auth, database models, Stripe multi-tier subscription billing, and real-time dashboard analytics.</p>
                    <div class="space-y-4 text-xs font-bold text-slate-700">
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Multi-tenant Database Architectures (PostgreSQL, MongoDB)</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Stripe, PayPal, and BrainTree Subscription Billing Hooks</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Real-time Admin Dashboards & User Analytics Charts</div>
                    </div>
                </div>
                <div class="grid sm:grid-cols-2 gap-6" data-aos="fade-left">
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">Scaleable Cloud Setup</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We deploy your SaaS on AWS or GCP, with dockerized microservices and autoscale triggers to manage spikes in traffic.</p>
                    </div>
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">High Security Defaults</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We implement JWT security headers, rate limiting, and database encryptions to protect sensitive customer data.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    faqs = [
        ("What is the cost of building a SaaS MVP?", "SaaS MVP (Minimum Viable Product) development costs between $9,999 to $25,000 depending on complexity, database size, and billing models. We supply a clear breakdown of milestones."),
        ("How long does it take to launch a SaaS MVP?", "Most SaaS MVPs are successfully completed and launched in 8 to 12 weeks. We work in bi-weekly sprints to ensure you can test intermediate builds along the way."),
        ("Can you help with post-launch maintenance and upgrades?", "Yes. We include 30 days of free post-launch bug support. After that, we offer monthly retainer maintenance plans starting at $199/month to manage server updates, security scans, and feature additions.")
    ]
    generate_service_detail_page("saas-development", "SaaS Product Development Company", "Launch Your Product", "Build Your SaaS Product From Idea to Launch", body, faqs, "MVP packages start at $9,999.", "https://hosterlo.com/services/saas-development/", "{}")

def build_frontend_development():
    body = """
    <section class="py-24 bg-white relative">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="grid lg:grid-cols-2 gap-16 items-center">
                <div data-aos="fade-right">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-6 leading-tight">Pixel-Perfect, Highly Interactive Frontends</h2>
                    <p class="text-slate-500 text-base mb-8 leading-relaxed">We translate static designs (Figma, Adobe XD) into interactive, performant frontend code. Specializing in modern JavaScript frameworks, we construct responsive web applications with micro-interactions, smooth animations, and clean modular states.</p>
                    <div class="space-y-4 text-xs font-bold text-slate-700">
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> React.js, Next.js, and Vue.js Single Page Applications</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Modern State Management (Redux Toolkit, Zustand, Pinia)</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Responsive CSS Frame (Tailwind CSS, CSS Modules)</div>
                    </div>
                </div>
                <div class="grid sm:grid-cols-2 gap-6" data-aos="fade-left">
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">Modern Frameworks</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We leverage Next.js to provide Server-Side Rendering (SSR) and Static Site Generation (SSG) for faster speeds.</p>
                    </div>
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">AOS Animations</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We build scroll-triggered layouts and clean CSS animations that feel alive and keep visitors engaged.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    faqs = [
        ("Which frontend framework should I choose?", "Next.js (React) is highly recommended for search-visible websites and marketing-centric portals. For complex dashboard apps, React.js or Vue.js is ideal."),
        ("Do you build frontends for existing backend APIs?", "Yes, we frequently build frontends that consume pre-existing REST or GraphQL backend APIs, ensuring perfect synchronization and data validation.")
    ]
    generate_service_detail_page("frontend-development", "Frontend Development Services", "Pixel-Perfect UI", "Pixel-Perfect Frontend Development", body, faqs, "Hourly starting at $55/hr or flat-rate per project.", "https://hosterlo.com/services/frontend-development/", "{}")

def build_backend_development():
    body = """
    <section class="py-24 bg-white relative">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="grid lg:grid-cols-2 gap-16 items-center">
                <div data-aos="fade-right">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-6 leading-tight">Scalable Server-Side Logic and Databases</h2>
                    <p class="text-slate-500 text-base mb-8 leading-relaxed">We build the core engine of your web application. From secure user registration and role-based permissions to massive database schemas and automated workflows, we write clean, robust backend code that scales with your business traffic.</p>
                    <div class="space-y-4 text-xs font-bold text-slate-700">
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Node.js (Express, NestJS), Python (Django, FastAPI), & PHP (Laravel)</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Relational & NoSQL Databases (PostgreSQL, MySQL, MongoDB, Redis)</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Secure RESTful and GraphQL API Design</div>
                    </div>
                </div>
                <div class="grid sm:grid-cols-2 gap-6" data-aos="fade-left">
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">Cloud Operations</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">Docker containerized environments, Kubernetes clusters, and serverless architectures deployed on AWS and Google Cloud.</p>
                    </div>
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">Caching & Queuing</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">Redis query caching and RabbitMQ/Celery background queue managers to keep the application quick under heavy load.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    faqs = [
        ("What backend technology is best for my app?", "Node.js is excellent for real-time applications and rapid scalability. Python (FastAPI/Django) is perfect for data manipulation and AI workflows. Laravel (PHP) is great for classic business portals."),
        ("How do you secure server endpoints?", "We implement strict authentication protocols (JWT or OAuth2), rate limiting to prevent spam, HTTPS encryption, parameter sanitation to prevent SQL injection, and regular dependency updates.")
    ]
    generate_service_detail_page("backend-development", "Backend Development Services", "Scalable Engines", "Scalable Backend Development and Database Modeling", body, faqs, "Hourly starting at $60/hr or flat-rate per project.", "https://hosterlo.com/services/backend-development/", "{}")

def build_ui_ux_design():
    body = """
    <section class="py-24 bg-white relative">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="grid lg:grid-cols-2 gap-16 items-center">
                <div data-aos="fade-right">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-6 leading-tight">User-Centered Designs That Enhance Engagement</h2>
                    <p class="text-slate-500 text-base mb-8 leading-relaxed">We design digital products that users love to interact with. By combining deep user research with high-fidelity wireframing and interactive prototypes, we build gorgeous UI designs in Figma that resolve complex navigation and convert visitors into loyal clients.</p>
                    <div class="space-y-4 text-xs font-bold text-slate-700">
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Interactive Figma Wireframes & High-Fidelity Prototypes</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Complete UX Audits and Conversion Optimization Analysis</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Custom Logo, Vector Graphics, and Brand Styling Systems</div>
                    </div>
                </div>
                <div class="grid sm:grid-cols-2 gap-6" data-aos="fade-left">
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">Figma Design Systems</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We design modular design tokens and components in Figma, making it simple for developers to write structured code.</p>
                    </div>
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">User Persona Audits</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We map target customer personas to streamline menu navigation, minimizing bounce rates and shopping cart drops.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    faqs = [
        ("What is the difference between UI and UX?", "UI (User Interface) refers to the visual appearance of the screens—colors, fonts, images, and alignment. UX (User Experience) refers to the logical flow, speed, structure, and how easily a user achieves their goals on the page."),
        ("What assets do I receive at the end of the design phase?", "You will receive full access to our collaborative Figma design space containing styled UI screens, vector illustration layers, custom icons, typography rules, and exportable branding guidelines.")
    ]
    generate_service_detail_page("ui-ux-design", "UI/UX Design Services", "Gorgeous Prototypes", "User-Centered Design That Drives Results and Conversions", body, faqs, "Design packages start at $1,499.", "https://hosterlo.com/services/ui-ux-design/", "{}")

def build_mobile_app_development():
    body = """
    <section class="py-24 bg-white relative">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="grid lg:grid-cols-2 gap-16 items-center">
                <div data-aos="fade-right">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-6 leading-tight">High-Performance Mobile Apps for iOS and Android</h2>
                    <p class="text-slate-500 text-base mb-8 leading-relaxed">We engineer native-feel cross-platform mobile applications that bring your service directly to your users' fingertips. Specializing in React Native and Flutter, we implement push notifications, location tracking, camera interfaces, and secure local databases.</p>
                    <div class="space-y-4 text-xs font-bold text-slate-700">
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Cross-Platform App Development (React Native & Flutter)</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Apple App Store & Google Play Store Submission Support</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Push Notification Systems & Local Location Tracking APIs</div>
                    </div>
                </div>
                <div class="grid sm:grid-cols-2 gap-6" data-aos="fade-left">
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">Native Integration</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We write custom platform bridges to hook into phone hardware components (camera, biometrics, Bluetooth) safely.</p>
                    </div>
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">Offline First Support</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We develop offline caching rules using SQLite or WatermelonDB to keep the app working when signals are weak.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    faqs = [
        ("Should I build a native or cross-platform app?", "For 90% of business applications, cross-platform (React Native or Flutter) is the best choice. It allows you to maintain one single codebase that runs on both iOS and Android, cutting development and maintenance costs in half."),
        ("Do you handle store submission and approval?", "Yes, we handle the entire process of compiling release builds, preparing metadata, setting up developer accounts, and submitting the apps to the Apple App Store and Google Play Store until they are approved.")
    ]
    generate_service_detail_page("mobile-app-development", "Mobile App Development Services", "iOS & Android", "High-Performance Mobile Apps for iOS and Android", body, faqs, "Mobile projects start at $14,999.", "https://hosterlo.com/services/mobile-app-development/", "{}")

def build_api_development():
    body = """
    <section class="py-24 bg-white relative">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="grid lg:grid-cols-2 gap-16 items-center">
                <div data-aos="fade-right">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-6 leading-tight">Secure & Scalable Custom APIs to Connect Your Software</h2>
                    <p class="text-slate-500 text-base mb-8 leading-relaxed">We design and construct clean API architectures that allow your website, mobile apps, database pools, and third-party SaaS tools to communicate seamlessly. Specializing in high-throughput REST and GraphQL design, we provide thorough documentation and secure tokens.</p>
                    <div class="space-y-4 text-xs font-bold text-slate-700">
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Custom RESTful and GraphQL API Architectures</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> CRM, ERP, Payment Gateway, and Logistics Custom Integrations</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Full Swagger/OpenAPI Documentation and API Testing Sandboxes</div>
                    </div>
                </div>
                <div class="grid sm:grid-cols-2 gap-6" data-aos="fade-left">
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">OAuth2 Authentication</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We deploy secure API key management systems, OAuth2 protocols, and token expiration structures to protect endpoints.</p>
                    </div>
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">High Rate Limits</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We integrate Redis caching layers and rate-limiting scripts to protect your servers from DDoS spikes.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    faqs = [
        ("What is the difference between REST and GraphQL?", "REST APIs use traditional standard endpoints (like /api/users) which return full structures. GraphQL allows the frontend client to request only the specific fields it needs in a single request, which speeds up mobile applications."),
        ("Do you provide documentation for internal teams?", "Yes. We configure automated interactive documentation systems (such as Swagger/OpenAPI or Postman Workspace collections) so your internal developers can integrate the API easily.")
    ]
    generate_service_detail_page("api-development", "API Development & Integration Services", "Connect Your Apps", "Custom APIs That Power Your Digital Ecosystem", body, faqs, "API development starts at $1,499.", "https://hosterlo.com/services/api-development/", "{}")

def build_website_maintenance():
    body = """
    <section class="py-24 bg-white relative">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="grid lg:grid-cols-2 gap-16 items-center">
                <div data-aos="fade-right">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-6 leading-tight">Proactive Support and Website Care retainers</h2>
                    <p class="text-slate-500 text-base mb-8 leading-relaxed">Keep your website secure, fast, and optimized without hire costs. Our professional developers perform weekly plugin reviews, system updates, secure off-site cloud backups, uptime monitoring, and prioritize support tickets to keep your site online 24/7.</p>
                    <div class="space-y-4 text-xs font-bold text-slate-700">
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Weekly Plugin, Core Theme, and PHP Audits</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Daily Off-site Cloud Backups and Instant Restore Support</div>
                        <div class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-sm">check_circle</span> Proactive Malware Scans and Firewalls Integration</div>
                    </div>
                </div>
                <div class="grid sm:grid-cols-2 gap-6" data-aos="fade-left">
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">24/7 Uptime Check</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We monitor your website every 60 seconds. If a crash happens, our team is notified automatically to fix it.</p>
                    </div>
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 class="font-extrabold text-sm text-[#111c2d] mb-2">Monthly Optimization</h4>
                        <p class="text-slate-500 text-xs leading-relaxed">We analyze load speeds and purge database overhead monthly to maintain a high PageSpeed score.</p>
                    </div>
                </div>
            </div>

            <!-- Pricing Table -->
            <div class="mt-20">
                <div class="text-center mb-12">
                    <h3 class="text-2xl font-extrabold text-slate-900">Choose Your Maintenance Plan</h3>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <!-- Basic -->
                    <div class="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm hover:shadow-md transition-all flex flex-col">
                        <h4 class="text-lg font-bold text-slate-800">Starter Plan</h4>
                        <span class="text-3xl font-black text-slate-900 mt-4">$99<span class="text-sm font-normal text-slate-500">/month</span></span>
                        <p class="text-slate-500 text-xs mt-2 mb-6">Perfect for small business sites & blogs.</p>
                        <ul class="space-y-3 text-xs text-slate-600 mb-8 mt-4">
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> Weekly WordPress/Plugin updates</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> Monthly off-site backups</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> 24/7 Uptime monitoring</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> 1 Hour included dev edits/mo</li>
                        </ul>
                        <a href="/get-a-quote/" class="mt-auto block w-full py-3 text-center bg-slate-100 text-slate-800 font-bold rounded-xl hover:bg-slate-200 transition-all text-xs">Choose Starter</a>
                    </div>
                    <!-- Pro -->
                    <div class="bg-white border-2 border-primary rounded-3xl p-8 shadow-md hover:shadow-lg transition-all flex flex-col relative">
                        <div class="absolute -top-4 right-8 px-3 py-1 bg-primary text-white text-[10px] uppercase font-black rounded-full">RECOMMENDED</div>
                        <h4 class="text-lg font-bold text-slate-800">Professional Plan</h4>
                        <span class="text-3xl font-black text-slate-900 mt-4">$199<span class="text-sm font-normal text-slate-500">/month</span></span>
                        <p class="text-slate-500 text-xs mt-2 mb-6">Ideal for busy e-commerce & corporate sites.</p>
                        <ul class="space-y-3 text-xs text-slate-600 mb-8 mt-4">
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> Weekly updates & security scans</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> Daily off-site backups</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> Speed & database optimization</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> 3 Hours included dev edits/mo</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> Priority email & chat support</li>
                        </ul>
                        <a href="/get-a-quote/" class="mt-auto block w-full py-3 text-center bg-primary text-white font-bold rounded-xl hover:bg-primary-container transition-all text-xs shadow-md shadow-primary/10">Choose Professional</a>
                    </div>
                    <!-- Enterprise -->
                    <div class="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm hover:shadow-md transition-all flex flex-col">
                        <h4 class="text-lg font-bold text-slate-800">Enterprise Plan</h4>
                        <span class="text-3xl font-black text-slate-900 mt-4">$499<span class="text-sm font-normal text-slate-500">/month</span></span>
                        <p class="text-slate-500 text-xs mt-2 mb-6">For complex portals and custom web applications.</p>
                        <ul class="space-y-3 text-xs text-slate-600 mb-8 mt-4">
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> Core code, server & plugin management</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> Real-time continuous backups</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> Dedicated staging setup for tests</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> 8 Hours included dev edits/mo</li>
                            <li class="flex items-center gap-2"><span class="material-symbols-outlined text-emerald-500 text-[16px]">check</span> 24/7 Priority support hotline</li>
                        </ul>
                        <a href="/get-a-quote/" class="mt-auto block w-full py-3 text-center bg-slate-100 text-slate-800 font-bold rounded-xl hover:bg-slate-200 transition-all text-xs">Choose Enterprise</a>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    faqs = [
        ("What constitutes a 'dev edit' in the plans?", "Dev edits cover content additions, changing copy or image files, correcting layout misalignments, setting up redirects, and minor code refinements. They exclude building new multi-page features from scratch."),
        ("Is there a lock-in contract on maintenance plans?", "No. All website care plans are billed on a month-to-month basis. You can cancel or upgrade your care tier at any time with a 15-day notice before your next invoice cycle.")
    ]
    generate_service_detail_page("website-maintenance", "Website Maintenance & Support Plans", "Worry-Free Website Support", "Keep Your Website Secure, Fast, and Updated", body, faqs, "Retainers starting at $99/mo.", "https://hosterlo.com/services/website-maintenance/", "{}")


# ----------------- PORTFOLIO / CASE STUDIES PAGE -----------------
def generate_portfolio():
    schema = """{
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Organization",
          "@id": "https://hosterlo.com/#organization",
          "name": "Hosterlo",
          "url": "https://hosterlo.com/"
        },
        {
          "@type": "WebSite",
          "@id": "https://hosterlo.com/#website",
          "url": "https://hosterlo.com/"
        },
        {
          "@type": "WebPage",
          "@id": "https://hosterlo.com/portfolio/#webpage",
          "url": "https://hosterlo.com/portfolio/",
          "name": "Our Work Portfolio & Case Studies | Hosterlo",
          "isPartOf": {
            "@id": "https://hosterlo.com/#website"
          }
        }
      ]
    }"""
    
    body = """
    <main>
        <!-- Hero Section -->
        <section class="relative min-h-[50vh] flex items-center overflow-hidden bg-gradient-to-br from-[#0f0a1e] via-[#1a1145] to-[#2d1b69] text-white -mt-[96px] pt-32 pb-20">
            <div class="absolute inset-0">
                <div class="hero-grid-pattern absolute inset-0 opacity-[0.2]"></div>
            </div>
            <div class="max-w-[1440px] mx-auto px-6 text-center w-full relative z-10">
                <span class="inline-block font-label-caps text-indigo-400 px-4 py-1.5 bg-white/5 rounded-full mb-6 uppercase">OUR CASE STUDIES</span>
                <h1 class="font-h1 text-4xl sm:text-5xl lg:text-6xl text-white mb-6 leading-tight font-black">Proof of Our Execution</h1>
                <p class="font-body-lg text-body-lg text-white/70 max-w-2xl mx-auto mb-12">We help clients solve complex software problems, streamline UI workflows, and build high-performance products that convert visitors into revenue.</p>
                <div class="flex justify-center gap-4 flex-wrap text-sm font-bold">
                    <button onclick="filterProjects('all')" class="filter-btn px-6 py-2.5 bg-primary text-white rounded-full transition-all">All Projects</button>
                    <button onclick="filterProjects('web')" class="filter-btn px-6 py-2.5 bg-white/10 text-white hover:bg-white/20 rounded-full transition-all">Web Dev</button>
                    <button onclick="filterProjects('saas')" class="filter-btn px-6 py-2.5 bg-white/10 text-white hover:bg-white/20 rounded-full transition-all">SaaS Products</button>
                    <button onclick="filterProjects('mobile')" class="filter-btn px-6 py-2.5 bg-white/10 text-white hover:bg-white/20 rounded-full transition-all">Mobile Apps</button>
                </div>
            </div>
        </section>

        <!-- Project Grid Section -->
        <section class="py-24 bg-white relative">
            <div class="max-w-[1440px] mx-auto px-6">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <!-- Project 1: SaaS MVP -->
                    <div class="project-card bg-slate-50 border border-slate-100 rounded-3xl overflow-hidden hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col" data-category="saas" data-aos="fade-up">
                        <div class="h-[240px] bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-6 relative">
                            <span class="text-white font-extrabold text-2xl font-h1">FinTech Dashboard</span>
                        </div>
                        <div class="p-8 flex flex-col flex-grow">
                            <span class="text-primary font-black text-[10px] uppercase tracking-widest block mb-2">SaaS MVP</span>
                            <h3 class="text-xl font-bold text-slate-900 mb-3">FinTech Analytics Dashboard</h3>
                            <p class="text-slate-500 text-sm mb-6 leading-relaxed">Built in 8 weeks for a financial advisory startup, this platform features secure JWT user authentication, MongoDB schema arrays, Stripe billing pipelines, and interactive Chart.js modules.</p>
                            <div class="flex flex-wrap gap-2 mb-6">
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">React.js</span>
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">Node.js</span>
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">MongoDB</span>
                            </div>
                            <div class="mt-auto border-t border-slate-200/60 pt-4 flex justify-between items-center text-xs">
                                <span class="font-extrabold text-slate-900">Result: Launched in 8 Weeks</span>
                                <a href="/get-a-quote/" class="text-primary font-extrabold flex items-center gap-1 hover:underline">Discuss Similar <span class="material-symbols-outlined text-[14px]">arrow_forward</span></a>
                            </div>
                        </div>
                    </div>

                    <!-- Project 2: Web Dev -->
                    <div class="project-card bg-slate-50 border border-slate-100 rounded-3xl overflow-hidden hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col" data-category="web" data-aos="fade-up" data-aos-delay="100">
                        <div class="h-[240px] bg-gradient-to-br from-blue-500 to-emerald-600 flex items-center justify-center p-6 relative">
                            <span class="text-white font-extrabold text-2xl font-h1">Solar Energy Corp</span>
                        </div>
                        <div class="p-8 flex flex-col flex-grow">
                            <span class="text-primary font-black text-[10px] uppercase tracking-widest block mb-2">Web Development</span>
                            <h3 class="text-xl font-bold text-slate-900 mb-3">Solar Energy Corporate Portal</h3>
                            <p class="text-slate-500 text-sm mb-6 leading-relaxed">A custom-designed corporate website for a leading green energy provider, utilizing optimized WordPress setups, custom contact forms, and custom Gutenberg blocks.</p>
                            <div class="flex flex-wrap gap-2 mb-6">
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">WordPress</span>
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">PHP</span>
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">Tailwind CSS</span>
                            </div>
                            <div class="mt-auto border-t border-slate-200/60 pt-4 flex justify-between items-center text-xs">
                                <span class="font-extrabold text-slate-900">Result: +150% Leads Increase</span>
                                <a href="/get-a-quote/" class="text-primary font-extrabold flex items-center gap-1 hover:underline">Discuss Similar <span class="material-symbols-outlined text-[14px]">arrow_forward</span></a>
                            </div>
                        </div>
                    </div>

                    <!-- Project 3: Ecommerce Web Dev -->
                    <div class="project-card bg-slate-50 border border-slate-100 rounded-3xl overflow-hidden hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col" data-category="web" data-aos="fade-up" data-aos-delay="200">
                        <div class="h-[240px] bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center p-6 relative">
                            <span class="text-white font-extrabold text-2xl font-h1">Skincare Shopify</span>
                        </div>
                        <div class="p-8 flex flex-col flex-grow">
                            <span class="text-primary font-black text-[10px] uppercase tracking-widest block mb-2">Web Development</span>
                            <h3 class="text-xl font-bold text-slate-900 mb-3">Organic Skincare Shopify Store</h3>
                            <p class="text-slate-500 text-sm mb-6 leading-relaxed">Bespoke Shopify Liquid development, setting up custom product configurators, high-performance checkout optimizations, and CRM hooks for shipping alerts.</p>
                            <div class="flex flex-wrap gap-2 mb-6">
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">Shopify</span>
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">Liquid</span>
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">Figma</span>
                            </div>
                            <div class="mt-auto border-t border-slate-200/60 pt-4 flex justify-between items-center text-xs">
                                <span class="font-extrabold text-slate-900">Result: 4.2% Conv. Rate</span>
                                <a href="/get-a-quote/" class="text-primary font-extrabold flex items-center gap-1 hover:underline">Discuss Similar <span class="material-symbols-outlined text-[14px]">arrow_forward</span></a>
                            </div>
                        </div>
                    </div>

                    <!-- Project 4: Mobile App -->
                    <div class="project-card bg-slate-50 border border-slate-100 rounded-3xl overflow-hidden hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col" data-category="mobile" data-aos="fade-up">
                        <div class="h-[240px] bg-gradient-to-br from-violet-500 to-fuchsia-600 flex items-center justify-center p-6 relative">
                            <span class="text-white font-extrabold text-2xl font-h1">Ride-Sharing App</span>
                        </div>
                        <div class="p-8 flex flex-col flex-grow">
                            <span class="text-primary font-black text-[10px] uppercase tracking-widest block mb-2">Mobile Application</span>
                            <h3 class="text-xl font-bold text-slate-900 mb-3">City Ride-Sharing Application</h3>
                            <p class="text-slate-500 text-sm mb-6 leading-relaxed">Engineered using React Native for cross-platform iOS and Android performance, integrated with real-time Google Maps API directions and push notification triggers.</p>
                            <div class="flex flex-wrap gap-2 mb-6">
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">React Native</span>
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">Firebase</span>
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">Google Maps API</span>
                            </div>
                            <div class="mt-auto border-t border-slate-200/60 pt-4 flex justify-between items-center text-xs">
                                <span class="font-extrabold text-slate-900">Result: 50K+ Installs</span>
                                <a href="/get-a-quote/" class="text-primary font-extrabold flex items-center gap-1 hover:underline">Discuss Similar <span class="material-symbols-outlined text-[14px]">arrow_forward</span></a>
                            </div>
                        </div>
                    </div>

                    <!-- Project 5: API Dev -->
                    <div class="project-card bg-slate-50 border border-slate-100 rounded-3xl overflow-hidden hover:shadow-xl hover:border-primary/20 transition-all duration-300 flex flex-col" data-category="saas" data-aos="fade-up" data-aos-delay="100">
                        <div class="h-[240px] bg-gradient-to-br from-teal-500 to-cyan-600 flex items-center justify-center p-6 relative">
                            <span class="text-white font-extrabold text-2xl font-h1">Shipping Hub</span>
                        </div>
                        <div class="p-8 flex flex-col flex-grow">
                            <span class="text-primary font-black text-[10px] uppercase tracking-widest block mb-2">API Development</span>
                            <h3 class="text-xl font-bold text-slate-900 mb-3">Custom Logistics API Hub</h3>
                            <p class="text-slate-500 text-sm mb-6 leading-relaxed">Built a custom Python/FastAPI integration middleware to connect a manufacturer's CRM database to international shipping lines and invoice APIs.</p>
                            <div class="flex flex-wrap gap-2 mb-6">
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">FastAPI</span>
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">Python</span>
                                <span class="px-3 py-1 bg-slate-200/60 text-slate-700 text-[10px] font-bold rounded-full">PostgreSQL</span>
                            </div>
                            <div class="mt-auto border-t border-slate-200/60 pt-4 flex justify-between items-center text-xs">
                                <span class="font-extrabold text-slate-900">Result: 99.9% Sync Accuracy</span>
                                <a href="/get-a-quote/" class="text-primary font-extrabold flex items-center gap-1 hover:underline">Discuss Similar <span class="material-symbols-outlined text-[14px]">arrow_forward</span></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <script>
        function filterProjects(category) {
            // Update button styles
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(btn => {
                btn.classList.remove('bg-primary', 'text-white');
                btn.classList.add('bg-white/10', 'text-white', 'hover:bg-white/20');
            });
            
            // Add active styles to clicked button
            const eventTarget = window.event ? window.event.target : null;
            if (eventTarget && eventTarget.tagName === 'BUTTON') {
                eventTarget.classList.remove('bg-white/10', 'text-white', 'hover:bg-white/20');
                eventTarget.classList.add('bg-primary', 'text-white');
            }

            // Filter cards
            const cards = document.querySelectorAll('.project-card');
            cards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-category') === category) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
    """
    
    html = get_head("Our Work Portfolio & Case Studies | Hosterlo", 
                    "Explore our development case studies. Custom web development, SaaS product MVPs, and mobile app projects delivered by Hosterlo.",
                    "https://hosterlo.com/portfolio/", schema) + body + get_foot()
    
    create_dir_if_not_exists("portfolio")
    with open("portfolio/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated portfolio/index.html")


# ----------------- GET A QUOTE FORM PAGE -----------------
def generate_get_a_quote():
    schema = """{
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Organization",
          "@id": "https://hosterlo.com/#organization",
          "name": "Hosterlo",
          "url": "https://hosterlo.com/"
        },
        {
          "@type": "WebSite",
          "@id": "https://hosterlo.com/#website",
          "url": "https://hosterlo.com/"
        },
        {
          "@type": "WebPage",
          "@id": "https://hosterlo.com/get-a-quote/#webpage",
          "url": "https://hosterlo.com/get-a-quote/",
          "name": "Request a Free Project Quote | Hosterlo",
          "isPartOf": {
            "@id": "https://hosterlo.com/#website"
          }
        }
      ]
    }"""
    
    body = """
    <main>
        <!-- Hero Section -->
        <section class="relative min-h-[40vh] flex items-center overflow-hidden bg-gradient-to-br from-[#0f0a1e] via-[#1a1145] to-[#2d1b69] text-white -mt-[96px] pt-32 pb-20">
            <div class="absolute inset-0">
                <div class="hero-grid-pattern absolute inset-0 opacity-[0.2]"></div>
            </div>
            <div class="max-w-[1440px] mx-auto px-6 text-center w-full relative z-10">
                <span class="inline-block font-label-caps text-indigo-400 px-4 py-1.5 bg-white/5 rounded-full mb-6 uppercase">FREE CONSULTATION</span>
                <h1 class="font-h1 text-4xl sm:text-5xl lg:text-6xl text-white mb-4 leading-tight font-black">Request a Free Project Quote</h1>
                <p class="font-body-lg text-body-lg text-white/70 max-w-xl mx-auto">Share your project ideas and software goals. We will reply within 24 hours with a scope outline and price range.</p>
            </div>
        </section>

        <!-- Form Section -->
        <section class="py-24 bg-white relative">
            <div class="max-w-[1440px] mx-auto px-6 grid lg:grid-cols-12 gap-16">
                <!-- Left: Form -->
                <div class="lg:col-span-7 bg-slate-50 border border-slate-200/60 rounded-[36px] p-8 md:p-12 shadow-sm" data-aos="fade-right">
                    <form id="quote-request-form" class="space-y-6" onsubmit="handleQuoteSubmit(event)">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                            <div>
                                <label for="client_name" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Full Name</label>
                                <input required type="text" id="client_name" name="client_name" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:border-primary focus:ring-primary text-sm transition-all" placeholder="Sarah Jenkins">
                            </div>
                            <div>
                                <label for="client_email" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Email Address</label>
                                <input required type="email" id="client_email" name="client_email" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:border-primary focus:ring-primary text-sm transition-all" placeholder="sarah@company.com">
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                            <div>
                                <label for="client_company" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Company / Organization</label>
                                <input type="text" id="client_company" name="client_company" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:border-primary focus:ring-primary text-sm transition-all" placeholder="Acme Corp">
                            </div>
                            <div>
                                <label for="project_category" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Project Category</label>
                                <select required id="project_category" name="project_category" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:border-primary focus:ring-primary text-sm transition-all">
                                    <option value="" disabled selected>Select category...</option>
                                    <option value="web-dev">Web Development</option>
                                    <option value="saas">SaaS Application</option>
                                    <option value="frontend">Frontend Engineering</option>
                                    <option value="backend">Backend Engineering</option>
                                    <option value="uiux">UI/UX Design</option>
                                    <option value="mobile">Mobile Application</option>
                                    <option value="api">API / Integration</option>
                                    <option value="maintenance">Website Maintenance Plan</option>
                                </select>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                            <div>
                                <label for="budget_range" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Budget Range</label>
                                <select required id="budget_range" name="budget_range" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:border-primary focus:ring-primary text-sm transition-all">
                                    <option value="" disabled selected>Select budget...</option>
                                    <option value="under-1k">Under $1,000</option>
                                    <option value="1k-5k">$1,000 - $5,000</option>
                                    <option value="5k-15k">$5,000 - $15,000</option>
                                    <option value="15k-50k">$15,000 - $50,000</option>
                                    <option value="above-50k">Above $50,000</option>
                                </select>
                            </div>
                            <div>
                                <label for="project_timeline" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Expected Timeline</label>
                                <select required id="project_timeline" name="project_timeline" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:border-primary focus:ring-primary text-sm transition-all">
                                    <option value="" disabled selected>Select timeline...</option>
                                    <option value="urgent">Urgent (Less than 1 month)</option>
                                    <option value="1-2-mo">1 to 2 months</option>
                                    <option value="3-6-mo">3 to 6 months</option>
                                    <option value="no-hurry">No rush / flexible</option>
                                </select>
                            </div>
                        </div>

                        <div>
                            <label for="project_description" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Project Scope & Details</label>
                            <textarea required id="project_description" name="project_description" rows="5" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:border-primary focus:ring-primary text-sm transition-all" placeholder="Describe your database requirements, integration endpoints, page count, or desired user features..."></textarea>
                        </div>

                        <button type="submit" class="button-shine w-full py-4 bg-primary text-white font-extrabold rounded-2xl transition-all shadow-lg shadow-primary/20 text-center hover:scale-[1.02]">Submit Quote Request</button>
                    </form>

                    <!-- Success State Dialog (Hidden by Default) -->
                    <div id="form-success-state" class="hidden text-center py-12 space-y-6">
                        <div class="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto shadow-inner">
                            <span class="material-symbols-outlined text-3xl">task_alt</span>
                        </div>
                        <h3 class="text-2xl font-black text-slate-900">Request Sent Successfully!</h3>
                        <p class="text-slate-500 text-sm max-w-sm mx-auto">Thank you for sharing your project scope. Our lead software architect has received your details and will get back to you with a free scope outline in 24 hours.</p>
                        <button onclick="resetQuoteForm()" class="px-6 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold rounded-xl transition-all">Send Another Request</button>
                    </div>
                </div>

                <!-- Right: Trust Signals -->
                <div class="lg:col-span-5 space-y-8" data-aos="fade-left">
                    <div class="bg-slate-50 border border-slate-200/60 rounded-[30px] p-8 space-y-6">
                        <h3 class="text-lg font-extrabold text-[#111c2d]">The Hosterlo Guarantee</h3>
                        <div class="space-y-4 text-xs font-bold text-slate-700">
                            <div class="flex items-start gap-3">
                                <span class="material-symbols-outlined text-emerald-500 text-sm shrink-0">check_circle</span>
                                <div>
                                    <h4 class="font-extrabold text-[#111c2d] text-sm">24-Hour Response Promise</h4>
                                    <p class="text-slate-500 text-xs font-normal mt-1 leading-relaxed">We respect your timelines. You will receive an initial structured review or meeting invitation from our leads in under 24 hours.</p>
                                </div>
                            </div>
                            <div class="flex items-start gap-3">
                                <span class="material-symbols-outlined text-emerald-500 text-sm shrink-0">check_circle</span>
                                <div>
                                    <h4 class="font-extrabold text-[#111c2d] text-sm">100% IP & Source Code Security</h4>
                                    <p class="text-slate-500 text-xs font-normal mt-1 leading-relaxed">All project discussions are strictly confidential. Upon launch, full repository source code and intellectual property are handed to you.</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="p-4 bg-[#f8f6fc] rounded-2xl border border-indigo-100 flex items-center gap-4">
                        <div class="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center shrink-0">
                            <span class="material-symbols-outlined text-xl">contact_support</span>
                        </div>
                        <div>
                            <h4 class="text-xs font-bold text-slate-900">Prefer direct messaging?</h4>
                            <p class="text-[11px] text-slate-500 mt-0.5">Chat with our systems architect on WhatsApp: <a href="https://wa.me/923394437730" target="_blank" rel="noopener" class="text-primary hover:underline font-bold">+92 (339) 443-7730</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <script>
        function handleQuoteSubmit(event) {
            event.preventDefault();
            
            // Collect form data (Mockup API trigger)
            const formData = {
                name: document.getElementById('client_name').value,
                email: document.getElementById('client_email').value,
                company: document.getElementById('client_company').value,
                category: document.getElementById('project_category').value,
                budget: document.getElementById('budget_range').value,
                timeline: document.getElementById('project_timeline').value,
                description: document.getElementById('project_description').value
            };
            
            console.log('Sending project quote request:', formData);
            
            // Switch form to success state dialog
            document.getElementById('quote-request-form').classList.add('hidden');
            document.getElementById('form-success-state').classList.remove('hidden');
        }
        
        function resetQuoteForm() {
            document.getElementById('quote-request-form').reset();
            document.getElementById('form-success-state').classList.add('hidden');
            document.getElementById('quote-request-form').classList.remove('hidden');
        }
    </script>
    """
    
    html = get_head("Request a Free Project Quote | Hosterlo Digital Agency", 
                    "Request a free software or website development quote from Hosterlo. We respond with a roadmap and budget estimate in 24 hours.",
                    "https://hosterlo.com/get-a-quote/", schema) + body + get_foot()
    
    create_dir_if_not_exists("get-a-quote")
    with open("get-a-quote/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated get-a-quote/index.html")


# ----------------- MAIN PIPELINE RUNNER -----------------
if __name__ == "__main__":
    generate_services_hub()
    build_web_development()
    build_saas_development()
    build_frontend_development()
    build_backend_development()
    build_ui_ux_design()
    build_mobile_app_development()
    build_api_development()
    build_website_maintenance()
    generate_portfolio()
    generate_get_a_quote()
    print("All 11 digital service agency pages generated successfully!")
