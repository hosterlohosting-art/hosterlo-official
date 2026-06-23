import os
import re
import json

ROOT = r"d:\Hosterlo Official Site"

def find_tag_bounds(content, tag_name, start_search=0):
    start_pos = content.find(f'<{tag_name}', start_search)
    if start_pos == -1:
        return -1, -1
    
    end_pos = content.find(f'</{tag_name}>', start_pos)
    if end_pos == -1:
        return -1, -1
    end_pos += len(f'</{tag_name}>')
    return start_pos, end_pos

def find_div_bounds(content, identifier, start_search=0):
    id_pos = content.find(identifier, start_search)
    if id_pos == -1:
        return -1, -1
    
    start_pos = content.rfind('<div', 0, id_pos)
    if start_pos == -1:
        return -1, -1
        
    depth = 0
    pattern = re.compile(r'<div\b|</div>', re.IGNORECASE)
    for match in pattern.finditer(content, start_pos):
        tag = match.group(0).lower()
        if tag.startswith('<div'):
            depth += 1
        elif tag == '</div>':
            depth -= 1
            if depth == 0:
                return start_pos, match.end()
                
    return -1, -1

def extract_premium_blocks_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    h_start, h_end = find_tag_bounds(content, 'header')
    if h_start == -1 or h_end == -1:
        raise ValueError(f"Could not find <header> in {file_path}")
        
    o_start, o_end = find_div_bounds(content, 'id="mobile-menu-overlay"')
    
    zone_start = min(h_start, o_start) if o_start != -1 else h_start
    zone_end = max(h_end, o_end) if o_end != -1 else h_end
    
    comment_pos = content.rfind('<!-- TopNavBar -->', 0, zone_start)
    if comment_pos != -1 and zone_start - comment_pos < 100:
        zone_start = comment_pos
        
    header_block = content[zone_start:zone_end].strip()
    
    f_start, f_end = find_tag_bounds(content, 'footer')
    if f_start == -1 or f_end == -1:
        raise ValueError(f"Could not find <footer> in {file_path}")
        
    comment_pos = content.rfind('<!-- Footer', 0, f_start)
    if comment_pos != -1 and f_start - comment_pos < 150:
        f_start = comment_pos
        
    footer_block = content[f_start:f_end].strip()
    
    return header_block, footer_block

# HTML Head details template
def get_head_html(title, desc, canonical, lang, hreflangs_str):
    styles_url = "/styles.css" if lang != "es" else "/es/styles.css"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <link rel="icon" type="image/png" href="/favicon.png">
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <link rel="canonical" href="{canonical}" />
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta property="og:locale" content="{"es_ES" if lang == "es" else "en_US"}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Hosterlo">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="https://hosterlo.com/assets/logo.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="https://hosterlo.com/assets/logo.png">
{hreflangs_str}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="{styles_url}"/>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script id="tailwind-config">
      tailwind.config = {{
        darkMode: "class",
        theme: {{
          extend: {{
            "colors": {{
                    "primary": "#4f17ce",
                    "on-primary": "#ffffff",
                    "background": "#f9f9ff",
                    "on-background": "#111c2d"
            }},
            "fontFamily": {{
                    "h1": ["Outfit", "sans-serif"],
                    "h2": ["Outfit", "sans-serif"],
                    "body-lg": ["Plus Jakarta Sans", "sans-serif"]
            }}
          }}
        }}
      }}
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet"/>
    <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
</head>
<body class="bg-[#f9f9ff] text-[#111c2d]">
"""

# JSON-LD FAQ schema generator
def build_schema_json(faqs, url, lang, breadcrumbs_list):
    faq_entities = []
    for q, a in faqs:
        faq_entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
        
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": "Knowledge Base & Support | Hosterlo",
                "isPartOf": {"@type": "WebSite", "@id": "https://hosterlo.com/#website"},
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": i+1, "name": name, "item": link}
                        for i, (name, link) in enumerate(breadcrumbs_list)
                    ]
                }
            },
            {
                "@type": "FAQPage",
                "@id": f"{url}#faqpage",
                "mainEntity": faq_entities
            }
        ]
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n</script>'

# Knowledge Base Content definitions
kb_data_en = {
    "title": "Knowledge Base & Help Center — Domain, Email, cPanel & Hosting | Hosterlo",
    "desc": "Search Hosterlo's Knowledge Base to find answers about setting up nameservers, configuring custom emails, installing WordPress, cPanel guides, and billing.",
    "heading": "Knowledge Base",
    "subheading": "Search our help articles or browse categories below to find step-by-step guides for cPanel, domains, email setup, and security.",
    "search_placeholder": "Search for answers (e.g. nameservers, email configuration...)",
    "search_popular": "Popular searches:",
    "status_suffix": " articles found for ",
    "contact_title": "Still Need Help?",
    "contact_desc": "If you couldn't find the answer to your question, our support team is available 24/7.",
    "contact_whatsapp": "Chat via WhatsApp",
    "contact_ticket": "Submit Support Ticket",
    "categories": [
        {
            "id": "getting-started",
            "icon": "rocket_launch",
            "title": "Getting Started",
            "articles": [
                (
                    "What is Hosterlo's Website Launch Bundle?",
                    "It is an all-in-one package designed to help beginners and businesses launch their websites. Instead of buying hosting, domain names, SSL, business email, and setup support separately, Hosterlo bundles them into one transparent plan for $59/year."
                ),
                (
                    "How do I get started after purchasing my plan?",
                    "After your purchase is complete, our support team will contact you via WhatsApp or email within a few hours. We will guide you through domain setup, cPanel login, email setup, and one-click WordPress installation so your site can go live smoothly."
                ),
                (
                    "How do I install WordPress on my Hosterlo hosting account?",
                    "You can install WordPress in less than a minute. Log into your cPanel, scroll down to the 'Software' section, and click on 'Softaculous Apps Installer' or 'WordPress Manager by Softaculous'. Click 'Install Now', enter your website details, admin username, and password, and click submit. WordPress is now installed!"
                )
            ]
        },
        {
            "id": "hosting",
            "icon": "dns",
            "title": "cPanel & Hosting",
            "articles": [
                (
                    "How do I log into my cPanel control panel?",
                    "You can log into cPanel using the credentials sent to your welcome email. Alternatively, navigate to yourdomain.com/cpanel or yourdomain.com:2083 in your browser and enter your cPanel username and password. You can also log in directly from your Hosterlo Client Area under 'Services'."
                ),
                (
                    "How do I access cPanel File Manager to upload files?",
                    "Log into your cPanel. Under the 'Files' section, click on 'File Manager'. In the left sidebar, click on the 'public_html' directory. This is the root folder of your website. You can use the 'Upload' button at the top toolbar to upload your website files, scripts, or ZIP archives."
                ),
                (
                    "How do I check server resource usage (CPU, RAM, SSD)?",
                    "Log into cPanel. On the right sidebar under the 'Statistics' section, you will see real-time graphs showing your current CPU usage, Physical Memory usage (RAM), Entry Processes, I/O usage, and Disk Space usage (SSD)."
                )
            ]
        },
        {
            "id": "domains",
            "icon": "language",
            "title": "Domains & DNS",
            "articles": [
                (
                    "What are Hosterlo's nameservers and how do I point my domain?",
                    "If you purchased your domain through Hosterlo, it is already configured. If your domain is registered elsewhere (e.g. GoDaddy, Namecheap), log into your registrar, go to DNS management, and update your nameservers to: ns1.digioverse.com and ns2.digioverse.com. DNS propagation normally takes 1 to 24 hours."
                ),
                (
                    "How do I transfer my domain registration to Hosterlo?",
                    "To transfer your domain: 1. Unlock your domain at your current registrar. 2. Request an authorization code (EPP code). 3. Go to Hosterlo's Domain Transfer Portal, enter your domain name, paste the EPP code, and complete the purchase. 4. Approve the transfer via the verification email sent to you."
                ),
                (
                    "How do I configure DNS records (A, CNAME, MX)?",
                    "Log into cPanel, scroll down to the 'Domains' section, and click on 'Zone Editor'. Click 'Manage' next to your domain. From here, you can add, edit, or delete A records, CNAME records, MX records, and TXT records."
                )
            ]
        },
        {
            "id": "email",
            "icon": "mail",
            "title": "Email Setup",
            "articles": [
                (
                    "How do I create a custom business email address in cPanel?",
                    "Log into cPanel. Under the 'Email' section, click on 'Email Accounts'. Click the '+ Create' button on the right side. Select your domain, enter your desired username (e.g., info or support), set a secure password, assign storage limits, and click 'Create'. Your email address is now ready to use."
                ),
                (
                    "How do I configure my email client (Outlook, Gmail, iPhone)?",
                    "In cPanel → Email Accounts, click 'Connect Devices' next to your email address. You will see the manual configuration details. Use the Secure SSL/TLS settings: Incoming Server: mail.yourdomain.com (Port 993 for IMAP, Port 995 for POP3). Outgoing Server: mail.yourdomain.com (Port 465). Use your full email address and password to log in."
                ),
                (
                    "What is the difference between IMAP and POP3?",
                    "IMAP keeps your emails on the server, syncing changes across all devices (recommended if you read email on phone and computer). POP3 downloads the emails to your device and deletes them from the server (good for saving mail server space, but you won't see sent emails on other devices)."
                )
            ]
        },
        {
            "id": "security",
            "icon": "shield",
            "title": "SSL & Security",
            "articles": [
                (
                    "How do I activate the free Let's Encrypt SSL certificate?",
                    "Hosterlo hosting accounts run AutoSSL. The server automatically checks and installs a Let's Encrypt SSL certificate within a few hours of pointing your domain to our nameservers. It renews automatically every 90 days. To force a check, go to cPanel → SSL/TLS Status and click 'Run AutoSSL'."
                ),
                (
                    "How do I set up SPF and DMARC records to prevent spam?",
                    "Log into cPanel and click 'Email Deliverability' under the 'Email' section. cPanel automatically configures proper SPF, DKIM, and reverse DNS records. For DMARC, you can use our free lookup tools or add a TXT record named '_dmarc.yourdomain.com' in the cPanel Zone Editor with value: 'v=DMARC1; p=quarantine; pct=100'."
                ),
                (
                    "Are daily backups included and how do I restore them?",
                    "Yes. We perform daily automated backups of your files, databases, and emails. You can view, download, and restore backups at any time. Log into cPanel, go to the 'Files' section, and click on 'JetBackup 5' to select individual directories or databases to restore."
                )
            ]
        },
        {
            "id": "billing",
            "icon": "payments",
            "title": "Billing & Account",
            "articles": [
                (
                    "How does the 30-day money-back guarantee work?",
                    "If you are not satisfied with our hosting service, contact our support team within 30 days of your first purchase. We will issue a full refund of your hosting fee, no questions asked. Please note that domain registration fees are non-refundable as the domain remains yours."
                ),
                (
                    "How do I renew my hosting subscription or domain?",
                    "We send renewal notifications 14 days before your invoice is due. Log into your Hosterlo Client Area (billing.hosterlo.com), click on 'Invoices', select the unpaid invoice, choose your preferred payment method, and complete the transaction to renew your service."
                ),
                (
                    "What payment methods are supported?",
                    "We support all major credit/debit cards (Visa, Mastercard), PayPal, and Stripe. For customers in Pakistan, we also support bank transfers, EasyPaisa, and JazzCash payments through our local billing channels."
                )
            ]
        }
    ]
}

# Localized Spanish text
kb_data_es = {
    "title": "Centro de Ayuda y Base de Conocimientos — Dominio, Correo, cPanel y Hosting | Hosterlo",
    "desc": "Busque en la Base de Conocimientos de Hosterlo para encontrar respuestas sobre la configuración de servidores de nombres, correos corporativos, cPanel y facturación.",
    "heading": "Base de Conocimientos",
    "subheading": "Busque en nuestros artículos de ayuda o navegue por las categorías a continuación para encontrar guías detalladas paso a paso para cPanel, dominios, correos y seguridad.",
    "search_placeholder": "Buscar respuestas (ej. servidores de nombres, configuración de correo...)",
    "search_popular": "Búsquedas populares:",
    "status_suffix": " artículos encontrados para ",
    "contact_title": "¿Aún Necesita Ayuda?",
    "contact_desc": "Si no pudo encontrar la respuesta a su pregunta, nuestro equipo de soporte está disponible 24/7.",
    "contact_whatsapp": "Chat de WhatsApp",
    "contact_ticket": "Enviar Ticket de Soporte",
    "categories": [
        {
            "id": "getting-started",
            "icon": "rocket_launch",
            "title": "Primeros Pasos",
            "articles": [
                (
                    "¿Qué es el Paquete de Lanzamiento Web de Hosterlo?",
                    "Es un paquete todo en uno diseñado para ayudar a principiantes y empresas a lanzar sus sitios web de forma rápida. En lugar de comprar hosting, dominio, SSL, correos profesionales y soporte por separado, Hosterlo lo agrupa todo en un plan por $59/año."
                ),
                (
                    "¿Cómo empiezo después de comprar mi plan?",
                    "Una vez completada la compra, nuestro equipo de soporte se pondrá en contacto con usted por WhatsApp o correo electrónico en unas horas. Le ayudaremos a configurar su dominio, iniciar sesión en cPanel, crear sus correos e instalar WordPress con un solo clic."
                ),
                (
                    "¿Cómo instalo WordPress en mi cuenta de hosting Hosterlo?",
                    "Puede instalar WordPress en menos de un minuto. Inicie sesión en cPanel, vaya a la sección 'Software' y haga clic en 'Softaculous Apps Installer' o 'WordPress Manager by Softaculous'. Haga clic en 'Instalar ahora', ingrese los detalles del sitio, el usuario y la contraseña del administrador, y haga clic en enviar."
                )
            ]
        },
        {
            "id": "hosting",
            "icon": "dns",
            "title": "cPanel y Hosting",
            "articles": [
                (
                    "¿Cómo inicio sesión en mi panel de control cPanel?",
                    "Puede iniciar sesión en cPanel utilizando las credenciales enviadas a su correo de bienvenida. Navegue a sudominio.com/cpanel o sudominio.com:2083 en su navegador e introduzca su usuario y contraseña. También puede ingresar desde su Área de Clientes de Hosterlo en 'Servicios'."
                ),
                (
                    "¿Cómo accedo al Administrador de Archivos de cPanel para subir archivos?",
                    "Inicie sesión en cPanel. En la sección 'Archivos', haga clic en 'Administrador de archivos'. En la barra lateral izquierda, haga clic en el directorio 'public_html'. Esta es la carpeta raíz de su sitio. Puede utilizar el botón 'Cargar' en la barra de herramientas superior para subir archivos de su sitio."
                ),
                (
                    "¿Cómo verifico el uso de recursos del servidor (CPU, RAM, SSD)?",
                    "Inicie sesión en cPanel. En la barra lateral derecha, bajo la sección 'Estadísticas', verá gráficos en tiempo real con su consumo de CPU, memoria física (RAM), procesos entrantes, uso de E/S y espacio en disco (SSD)."
                )
            ]
        },
        {
            "id": "domains",
            "icon": "language",
            "title": "Dominios y DNS",
            "articles": [
                (
                    "¿Cuáles son los servidores de nombres de Hosterlo?",
                    "Si compró su dominio a través de Hosterlo, ya está configurado. Si está registrado en otro proveedor (GoDaddy, Namecheap), inicie sesión allí y actualice sus servidores de nombres a: ns1.digioverse.com y ns2.digioverse.com. La propagación DNS tarda de 1 a 24 horas."
                ),
                (
                    "¿Cómo transfiero mi dominio existente a Hosterlo?",
                    "Para transferir su dominio: 1. Desbloquee el dominio en su registrador actual. 2. Obtenga el código de autorización (código EPP). 3. Vaya al Portal de Transferencia de Hosterlo, introduzca su dominio, pegue el código EPP y complete la compra. 4. Confirme la transferencia en el correo que recibirá."
                ),
                (
                    "¿Cómo configuro registros DNS (A, CNAME, MX) en cPanel?",
                    "Inicie sesión en cPanel, baje a la sección 'Dominios' y haga clic en 'Zone Editor'. Haga clic en 'Administrar' junto a su dominio. Desde aquí, puede añadir, editar o eliminar registros DNS como registros A, CNAME, MX y TXT."
                )
            ]
        },
        {
            "id": "email",
            "icon": "mail",
            "title": "Cuentas de Correo",
            "articles": [
                (
                    "¿Cómo creo una dirección de correo corporativa en cPanel?",
                    "Inicie sesión en cPanel. En la sección 'Correo electrónico', haga clic en 'Cuentas de correo electrónico'. Haga clic en el botón '+ Crear' a la derecha. Seleccione su dominio, introduzca el usuario (ej. info o soporte), establezca una contraseña segura y haga clic en 'Crear'."
                ),
                (
                    "¿Cómo configuro mi cliente de correo (Outlook, Gmail, iPhone)?",
                    "En cPanel → Cuentas de correo electrónico, haga clic en 'Connect Devices' junto a su cuenta. Use los siguientes parámetros con SSL/TLS: Servidor entrante/saliente: mail.sudominio.com. Puerto IMAP: 993, Puerto POP3: 995, Puerto SMTP: 465. Use su correo completo y contraseña para iniciar sesión."
                ),
                (
                    "¿Cuál es la diferencia entre IMAP y POP3?",
                    "IMAP guarda los correos en el servidor y los sincroniza en todos los dispositivos. POP3 descarga los correos a su dispositivo y los borra del servidor. Se recomienda utilizar IMAP para poder acceder a sus correos desde múltiples dispositivos."
                )
            ]
        },
        {
            "id": "security",
            "icon": "shield",
            "title": "SSL y Seguridad",
            "articles": [
                (
                    "¿Cómo activo mi certificado SSL gratuito?",
                    "Hosterlo ejecuta AutoSSL en todos sus servidores. El sistema instala de forma automática un certificado Let's Encrypt SSL en un plazo de unas horas tras apuntar su dominio a nuestros servidores de nombres. Para forzar una comprobación, vaya a cPanel → SSL/TLS Status y haga clic en 'Run AutoSSL'."
                ),
                (
                    "¿Cómo configuro registros SPF y DMARC contra el spam?",
                    "Inicie sesión en cPanel y haga clic en 'Email Deliverability' en la sección de correo. cPanel configura automáticamente los registros SPF, DKIM y DNS inverso. Para DMARC, añada un registro TXT con nombre '_dmarc.sudominio.com' y el valor: 'v=DMARC1; p=quarantine; pct=100' en el Zone Editor."
                ),
                (
                    "¿Están incluidas las copias de seguridad y cómo las restauro?",
                    "Sí. Realizamos copias de seguridad automáticas diarias. Puede acceder a ellas en cualquier momento. Inicie sesión en cPanel, vaya a la sección 'Archivos' y haga clic en 'JetBackup 5' para seleccionar las carpetas o bases de datos que desea restaurar."
                )
            ]
        },
        {
            "id": "billing",
            "icon": "payments",
            "title": "Facturación",
            "articles": [
                (
                    "¿Cómo funciona la garantía de devolución de 30 días?",
                    "Si no está satisfecho con el hosting, póngase en contacto con nuestro equipo de soporte dentro de los primeros 30 días de la compra. Le devolveremos el 100% de la tarifa de hosting. Tenga en cuenta que las tasas de registro de dominio no son reembolsables."
                ),
                (
                    "¿Cómo renuevo mi servicio de hosting o dominio?",
                    "Enviamos notificaciones de renovación 14 días antes del vencimiento. Inicie sesión en su Área de Clientes de Hosterlo (billing.hosterlo.com), haga clic en 'Facturas', seleccione la factura correspondiente y proceda al pago."
                ),
                (
                    "¿Qué métodos de pago son aceptados?",
                    "Aceptamos tarjetas de crédito/débito (Visa, Mastercard), PayPal y Stripe. Para clientes en Pakistán, también admitimos EasyPaisa, JazzCash y transferencias bancarias locales."
                )
            ]
        }
    ]
}

def generate_body_html(data, lang, phone_number, whatsapp_url, whmcs_url):
    categories_html = ""
    articles_html = ""
    
    # 1. Categories grid cards
    for cat in data["categories"]:
        categories_html += f"""
                <a href="#category-{cat["id"]}" class="bg-white p-6 rounded-2xl border border-slate-200/60 text-center shadow-sm hover:shadow-md hover:border-primary/20 transition-all group">
                    <span class="material-symbols-outlined text-primary text-3xl mb-3 block group-hover:scale-110 transition-transform">{cat["icon"]}</span>
                    <span class="font-extrabold text-slate-900 text-xs sm:text-sm block">{cat["title"]}</span>
                </a>"""

    # 2. Articles sections with accordions
    for cat in data["categories"]:
        articles_html += f"""
            <div id="category-{cat["id"]}" class="kb-category-section pt-12 pb-4">
                <h3 class="text-xl font-black text-primary border-b border-slate-200 pb-3 flex items-center gap-3">
                    <span class="material-symbols-outlined">{cat["icon"]}</span>
                    {cat["title"]}
                </h3>
                <div class="space-y-4 mt-6">"""
                
        for q, a in cat["articles"]:
            articles_html += f"""
                    <details class="kb-article group bg-white rounded-2xl border border-slate-150 shadow-sm overflow-hidden transition-all duration-300 open:border-primary/30 open:shadow-md hover:border-slate-200">
                        <summary class="flex items-center justify-between p-6 cursor-pointer font-black text-[#111c2d] hover:text-primary transition-colors select-none text-sm sm:text-base">
                            {q}
                            <span class="material-symbols-outlined text-slate-400 group-open:text-primary group-open:rotate-180 transition-transform duration-300">expand_more</span>
                        </summary>
                        <div class="px-6 pb-6 text-slate-500 text-sm leading-relaxed border-t border-slate-50 pt-4">
                            {a}
                        </div>
                    </details>"""
        articles_html += """
                </div>
            </div>"""

    # 3. Assemble main body html
    return f"""
<main class="pt-24">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-[#0f0a1e] via-[#1a1145] to-[#2d1b69] text-white py-20 relative overflow-hidden">
        <div class="absolute inset-0 opacity-20"><div class="hero-grid-pattern absolute inset-0"></div></div>
        <div class="max-w-[1440px] mx-auto px-6 text-center relative z-10">
            <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-white/10 rounded-full text-xs font-black text-indigo-300 uppercase mb-4">{"CENTRO DE AYUDA" if lang == "es" else "HELP CENTER"}</span>
            <h1 class="font-h1 text-4xl md:text-5xl font-black mb-6">{data["heading"]}</h1>
            <p class="text-white/70 max-w-xl mx-auto mb-8 text-sm md:text-base leading-relaxed">{data["subheading"]}</p>
            <div class="max-w-xl mx-auto relative mb-4">
                <span class="material-symbols-outlined absolute left-5 top-1/2 -translate-y-1/2 text-slate-400">search</span>
                <input type="text" id="kb-search-input" placeholder="{data["search_placeholder"]}" class="w-full pl-14 pr-6 py-4 rounded-2xl bg-white text-slate-900 border border-transparent shadow-xl focus:outline-none focus:ring-2 focus:ring-primary/20 text-sm font-semibold">
            </div>
            <div class="flex flex-wrap gap-2 justify-center text-xs text-white/50">
                <span class="font-bold">{data["search_popular"]}</span>
                <a href="#category-domains" class="underline hover:text-white transition-colors">nameservers</a>,
                <a href="#category-getting-started" class="underline hover:text-white transition-colors">wordpress</a>,
                <a href="#category-email" class="underline hover:text-white transition-colors">email configuration</a>
            </div>
        </div>
    </section>

    <!-- Categories Grid -->
    <section class="py-16 bg-slate-50 border-b border-slate-100">
        <div class="max-w-[1440px] mx-auto px-6">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
                {categories_html}
            </div>
        </div>
    </section>

    <!-- KB Articles List -->
    <section class="py-24 bg-white">
        <div class="max-w-[900px] mx-auto px-6">
            <!-- Search status message -->
            <div id="search-status" class="hidden mb-6 p-4 bg-primary/5 border border-primary/10 rounded-xl text-primary font-bold text-sm"></div>
            
            <div class="space-y-4">
                {articles_html}
            </div>
        </div>
    </section>

    <!-- Contact CTA -->
    <section class="py-20 bg-slate-50 border-t border-slate-100 relative overflow-hidden">
        <div class="max-w-[1440px] mx-auto px-6 text-center relative z-10">
            <h2 class="text-2xl md:text-3xl font-black text-[#111c2d] mb-4">{data["contact_title"]}</h2>
            <p class="text-slate-500 text-sm max-w-md mx-auto mb-8 leading-relaxed">{data["contact_desc"]}</p>
            <div class="flex flex-wrap gap-4 justify-center">
                <a href="{whatsapp_url}" target="_blank" rel="noopener noreferrer" class="px-8 py-4 bg-[#25D366] text-white hover:bg-[#1da851] rounded-xl font-bold transition-all text-center shadow-md flex items-center justify-center gap-2">
                    <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.246 2.248 3.484 5.237 3.483 8.42-.003 6.557-5.338 11.892-11.893 11.892-1.997-.001-3.951-.5-5.688-1.448l-6.308 1.648zm6.757-4.041c1.574.933 3.109 1.423 4.919 1.424 5.456 0 9.897-4.437 9.9-9.899 0-2.646-1.03-5.132-2.903-7.003-1.871-1.871-4.358-2.901-7.001-2.902-5.463 0-9.897 4.437-9.9 9.902-.001 1.933.535 3.551 1.558 5.178l-.999 3.644 3.742-.979zm11.287-5.125c-.3-.15-1.771-.874-2.046-.975-.276-.101-.476-.15-.676.15-.199.3-.776.975-.951 1.176-.175.199-.349.225-.649.075-.3-.15-1.266-.467-2.411-1.487-.893-.797-1.495-1.782-1.67-2.083-.175-.3-.019-.462.13-.611.135-.134.3-.349.449-.525.151-.176.199-.3.3-.499.1-.199.05-.375-.025-.525-.075-.15-.676-1.631-.926-2.231-.242-.583-.491-.504-.676-.513-.174-.009-.375-.011-.575-.011-.2 0-.525.075-.8.375-.276.3-1.051 1.026-1.051 2.502 0 1.475 1.074 2.901 1.224 3.102.15.199 2.115 3.227 5.123 4.525.714.308 1.272.492 1.707.631.717.227 1.369.195 1.884.118.574-.085 1.771-.724 2.021-1.424.25-.699.25-1.299.175-1.424-.075-.125-.275-.199-.575-.349z"/></svg>
                    {data["contact_whatsapp"]}
                </a>
                <a href="{whmcs_url}" class="px-8 py-4 bg-primary text-white hover:bg-primary-container rounded-xl font-bold transition-all text-center shadow-md">
                    {data["contact_ticket"]}
                </a>
            </div>
        </div>
    </section>
</main>

<script>
document.addEventListener("DOMContentLoaded", function() {{
    const searchInput = document.getElementById('kb-search-input');
    const articles = document.querySelectorAll('details.kb-article');
    const categories = document.querySelectorAll('.kb-category-section');
    const status = document.getElementById('search-status');
    const statusSuffix = "{data["status_suffix"]}";
    
    if (searchInput) {{
        searchInput.addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase().trim();
            let matchedCount = 0;
            
            if (query === "") {{
                articles.forEach(item => {{
                    item.classList.remove('hidden');
                }});
                categories.forEach(cat => {{
                    cat.classList.remove('hidden');
                }});
                status.classList.add('hidden');
                return;
            }}
            
            articles.forEach(item => {{
                const text = item.innerText.toLowerCase();
                if (text.includes(query)) {{
                    item.classList.remove('hidden');
                    item.setAttribute('open', 'true');
                    matchedCount++;
                }} else {{
                    item.classList.add('hidden');
                    item.removeAttribute('open');
                }}
            }});
            
            categories.forEach(cat => {{
                const visible = cat.querySelectorAll('details.kb-article:not(.hidden)');
                if (visible.length === 0) {{
                    cat.classList.add('hidden');
                }} else {{
                    cat.classList.remove('hidden');
                }}
            }});
            
            status.classList.remove('hidden');
            status.innerText = matchedCount + statusSuffix + "'" + e.target.value + "'";
        }});
    }}
}});
</script>
"""

# Dynamic page compiler
def build_kb_page(rel_path, lang, title, desc, canonical, whatsapp_url, whmcs_url, hreflangs_str, breadcrumbs, source_homepage):
    # Extract original header/footer
    h_block, f_block = extract_premium_blocks_from_file(source_homepage)
    
    # Select content dictionary
    data = kb_data_es if lang == "es" else kb_data_en
    
    # 1. Compile FAQS list for JSON-LD schema
    all_faqs = []
    for cat in data["categories"]:
        for q, a in cat["articles"]:
            all_faqs.append((q, a))
            
    # 2. Get head, body, schema, footer
    head_content = get_head_html(title, desc, canonical, lang, hreflangs_str)
    schema_script = build_schema_json(all_faqs, canonical, lang, breadcrumbs)
    body_content = generate_body_html(data, lang, "+1 (618) 356-1311", whatsapp_url, whmcs_url)
    
    # Replace </head> with schema in head_content
    head_content = head_content.replace('</head>', f'{schema_script}\n</head>')
    
    # Combine page
    page_html = head_content + h_block + body_content + f_block + "\n</body>\n</html>"
    
    # Write page
    dir_path = os.path.dirname(os.path.join(ROOT, rel_path.replace('/', os.sep)))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    with open(os.path.join(ROOT, rel_path.replace('/', os.sep)), 'w', encoding='utf-8') as f:
        f.write(page_html)
    print(f"Created searchable Knowledge Base at: {rel_path}")

def main():
    import json
    # Define pages details
    hreflangs_str = (
        '    <link rel="alternate" hreflang="en-us" href="https://hosterlo.com/support/" />\n'
        '    <link rel="alternate" hreflang="en-gb" href="https://hosterlo.com/uk/support/" />\n'
        '    <link rel="alternate" hreflang="en-pk" href="https://hosterlo.com/pk/support/" />\n'
        '    <link rel="alternate" hreflang="es" href="https://hosterlo.com/es/support/" />\n'
        '    <link rel="alternate" hreflang="x-default" href="https://hosterlo.com/support/" />'
    )
    
    # 1. US support page
    build_kb_page(
        rel_path="support/index.html",
        lang="en",
        title="Knowledge Base & Help Center — cPanel, Domain, Email & Hosting | Hosterlo",
        desc="Search Hosterlo's Knowledge Base to find answers about setting up nameservers, configuring business emails, installing WordPress, cPanel, and billing.",
        canonical="https://hosterlo.com/support/",
        whatsapp_url="https://wa.me/16183561311",
        whmcs_url="https://billing.hosterlo.com/index.php?rp=/store/lightspeed-hosting/business-hosting",
        hreflangs_str=hreflangs_str,
        breadcrumbs=[
            ("Home", "https://hosterlo.com/"),
            ("Support & Knowledge Base", "https://hosterlo.com/support/")
        ],
        source_homepage=os.path.join(ROOT, "index.html")
    )
    
    # 2. ES support page
    build_kb_page(
        rel_path="es/support/index.html",
        lang="es",
        title="Centro de Ayuda y Base de Conocimientos — cPanel, Dominio & Hosting | Hosterlo",
        desc="Busque en la Base de Conocimientos de Hosterlo para encontrar guías sobre servidores de nombres, configuración de correo corporativo, cPanel y facturación.",
        canonical="https://hosterlo.com/es/support/",
        whatsapp_url="https://wa.me/16183561311",
        whmcs_url="https://billing.hosterlo.com/index.php?rp=/store/lightspeed-hosting/business-hosting",
        hreflangs_str=hreflangs_str,
        breadcrumbs=[
            ("Inicio", "https://hosterlo.com/es/"),
            ("Soporte y Base de Conocimientos", "https://hosterlo.com/es/support/")
        ],
        source_homepage=os.path.join(ROOT, "es/index.html")
    )
    
    # 3. UK support page
    build_kb_page(
        rel_path="uk/support/index.html",
        lang="en",
        title="Knowledge Base & Help Center — cPanel, Domain, Email & Hosting | Hosterlo UK",
        desc="Search Hosterlo's UK Knowledge Base to find answers about setting up nameservers, configuring business emails, installing WordPress, cPanel, and billing.",
        canonical="https://hosterlo.com/uk/support/",
        whatsapp_url="https://wa.me/16183561311",
        whmcs_url="https://billing.hosterlo.com/index.php?rp=/store/lightspeed-hosting/business-hosting",
        hreflangs_str=hreflangs_str,
        breadcrumbs=[
            ("Home", "https://hosterlo.com/uk/"),
            ("Support & Knowledge Base", "https://hosterlo.com/uk/support/")
        ],
        source_homepage=os.path.join(ROOT, "uk/index.html")
    )
    
    # 4. PK support page
    build_kb_page(
        rel_path="pk/support/index.html",
        lang="en",
        title="Knowledge Base & Help Center — cPanel, Domain, Email & Hosting | Hosterlo PK",
        desc="Search Hosterlo's PK Knowledge Base to find answers about setting up nameservers, configuring business emails, installing WordPress, cPanel, and billing.",
        canonical="https://hosterlo.com/pk/support/",
        whatsapp_url="https://wa.me/923394437730",
        whmcs_url="https://billing.hosterlo.com/index.php?rp=/store/lightspeed-hosting/business-hosting",
        hreflangs_str=hreflangs_str,
        breadcrumbs=[
            ("Home", "https://hosterlo.com/pk/"),
            ("Support & Knowledge Base", "https://hosterlo.com/pk/support/")
        ],
        source_homepage=os.path.join(ROOT, "pk/index.html")
    )

if __name__ == "__main__":
    import json
    main()
