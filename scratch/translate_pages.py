import os
import re

ROOT = "d:/Hosterlo Official Site"

def make_dirs(file_path):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def translate_page(rel_path, title, desc, replacements, schema_replacement=None):
    src_path = os.path.join(ROOT, rel_path)
    if not os.path.exists(src_path):
        print(f"Source file not found: {src_path}")
        return

    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update HTML lang
    content = content.replace('<html class="light" lang="en">', '<html class="light" lang="es">')
    content = content.replace('<html lang="en">', '<html lang="es">')

    # 2. Update canonical and OpenGraph url
    slug = rel_path
    if slug == "index.html":
        slug = ""
    elif slug.endswith("/index.html"):
        slug = slug[:-10]
    slug = slug.replace("\\", "/")
    
    # Update canonical
    content = re.sub(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']https://hosterlo.com/([^"\']*)["\']', 
        rf'<link rel="canonical" href="https://hosterlo.com/es/\1"', 
        content
    )
    # Update og:url
    content = re.sub(
        r'<meta\s+property=["\']og:url["\']\s+content=["\']https://hosterlo.com/([^"\']*)["\']', 
        rf'<meta property="og:url" content="https://hosterlo.com/es/\1"', 
        content
    )

    # 3. Update Title & Meta Description
    # We find existing title and replace it
    content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content)
    content = re.sub(r'<meta\s+property=["\']og:title["\']\s+content="[^"]*"', f'<meta property="og:title" content="{title}"', content)
    content = re.sub(r'<meta\s+name=["\']twitter:title["\']\s+content="[^"]*"', f'<meta name="twitter:title" content="{title}"', content)

    # replace description
    content = re.sub(r'<meta\s+name=["\']description["\']\s+content="[^"]*"', f'<meta name="description" content="{desc}"', content)
    content = re.sub(r'<meta\s+property=["\']og:description["\']\s+content="[^"]*"', f'<meta property="og:description" content="{desc}"', content)
    content = re.sub(r'<meta\s+name=["\']twitter:description["\']\s+content="[^"]*"', f'<meta name="twitter:description" content="{desc}"', content)

    # 4. Global replacements (Header & Footer)
    # Header Nav menu
    content = content.replace('Hosting <span', 'Hosting <span')
    content = content.replace('Services <span', 'Servicios <span')
    content = content.replace('Resources <span', 'Recursos <span')
    content = content.replace('Free Website Tools', 'Herramientas Gratis')
    content = content.replace('Contact Us</a>', 'Contacto</a>')
    content = content.replace('Client Login', 'Portal de Clientes')
    content = content.replace('Get the $59 Bundle', 'Obtener Paquete $59')
    
    # Mobile menu specific translations
    content = content.replace(' WordPress Hosting\n</a>', ' Hosting WordPress\n</a>')
    content = content.replace(' Pricing\n</a>', ' Precios\n</a>')
    content = content.replace(' Domains\n</a>', ' Dominios\n</a>')
    content = content.replace(' Services\n</a>', ' Servicios\n</a>')
    content = content.replace(' Free Tools\n</a>', ' Herramientas Gratis\n</a>')
    content = content.replace(' About Hosterlo\n</a>', ' Sobre Hosterlo\n</a>')
    content = content.replace(' Contact Us\n</a>', ' Contacto\n</a>')
    content = content.replace(' Client Login\n</a>', ' Portal de Clientes\n</a>')

    content = content.replace('Hosting</a>', 'Hosting</a>')
    content = content.replace('Cloud Hosting', 'Hosting Cloud')
    content = content.replace('Shared Hosting', 'Hosting Compartido')
    content = content.replace('WordPress Hosting', 'Hosting WordPress')
    content = content.replace('Domains</a>', 'Dominios</a>')
    content = content.replace('Services</a>', 'Servicios</a>')
    content = content.replace('All Services', 'Todos los Servicios')
    content = content.replace('Web Development', 'Desarrollo Web')
    content = content.replace('SaaS Development', 'Desarrollo SaaS')
    content = content.replace('Frontend Development', 'Desarrollo Frontend')
    content = content.replace('Backend Development', 'Desarrollo Backend')
    content = content.replace('UI/UX Design', 'Diseño UI/UX')
    content = content.replace('Mobile App Development', 'Desarrollo de Apps')
    content = content.replace('API Development', 'Desarrollo de APIs')
    content = content.replace('Website Maintenance', 'Mantenimiento Web')
    content = content.replace('Pricing</a>', 'Precios</a>')
    content = content.replace('Resources</a>', 'Recursos</a>')
    content = content.replace('Blog</a>', 'Blog</a>')
    content = content.replace('Free Tools', 'Herramientas Gratis')
    content = content.replace('About Hosterlo', 'Sobre Hosterlo')
    content = content.replace('Client Portal', 'Portal de Clientes')
    content = content.replace('Start Launching', 'Comenzar')

    # Footer section
    content = content.replace('Quick Links', 'Enlaces Rápidos')
    content = content.replace('Legal', 'Legal')
    content = content.replace('Terms of Service', 'Términos de Servicio')
    content = content.replace('Privacy Policy', 'Política de Privacidad')
    content = content.replace('Refund Policy', 'Política de Reembolso')
    content = content.replace('Hosterlo provides fast NVMe-backed web hosting, WordPress hosting, domain registration, SSL support, business email tools, DNS/email security tools, and customer support for website owners.', 
                              'Hosterlo ofrece hosting web NVMe rápido, hosting WordPress, registro de dominios, SSL y soporte para creadores y empresas.')
    content = content.replace('All rights reserved.', 'Todos los derechos reservados.')
    content = content.replace('Chat with Support', 'Chatear con Soporte')

    # Cookie Banner
    content = content.replace('We use cookies to improve your experience. By continuing to visit this site you agree to our use of cookies.', 
                              'Utilizamos cookies para mejorar su experiencia. Al continuar visitando este sitio, acepta nuestro uso de cookies.')
    content = content.replace('Accept</button>', 'Aceptar</button>')
    content = content.replace('Decline</button>', 'Rechazar</button>')

    # Floating contact widgets
    content = content.replace('Call Support', 'Llamar a Soporte')
    content = content.replace('Chat on WhatsApp', 'Soporte por WhatsApp')

    # 5. Schema replacement
    if schema_replacement:
        content = re.sub(
            r'<script type="application/ld\+json">(.*?)</script>', 
            f'<script type="application/ld+json">{schema_replacement}</script>', 
            content, 
            flags=re.DOTALL
        )

    # 6. Page-specific replacements
    for orig, rep in replacements:
        content = content.replace(orig, rep)

    # 7. Localized Link prefixing (e.g. href="/hosting/" -> href="/es/hosting/")
    # Avoid prefixing assets, billing, external link domains, or anchors
    def replace_href(match):
        prefix = "/es/"
        url = match.group(1)
        if url.startswith("/") and not url.startswith("//") and not url.startswith("/assets") and not url.startswith("/favicon"):
            if not url.startswith("/es/"):
                if url == "/":
                    return f'href="{prefix}"'
                return f'href="{prefix}{url[1:]}"'
        return match.group(0)

    content = re.sub(r'href="([^"]+)"', replace_href, content)

    # 8. Write file to /es/
    dest_path = os.path.join(ROOT, "es", rel_path)
    make_dirs(dest_path)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully created Spanish page: {dest_path}")

def main():
    # Helper to load organization schema
    es_org_schema = """{
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Organization",
          "@id": "https://hosterlo.com/es/#organization",
          "name": "Hosterlo LLC",
          "url": "https://hosterlo.com/es/",
          "logo": {
            "@type": "ImageObject",
            "url": "https://hosterlo.com/assets/logo.png"
          },
          "description": "Hosterlo ofrece hosting web NVMe rápido y planes de hosting WordPress administrados en español.",
          "address": {
            "@type": "PostalAddress",
            "streetAddress": "16192 Coastal Highway",
            "addressLocality": "Lewes",
            "addressRegion": "DE",
            "postalCode": "19958",
            "addressCountry": "US"
          },
          "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+1-302-203-9118",
            "contactType": "customer support",
            "availableLanguage": ["English", "Spanish"],
            "areaServed": [
              {"@type": "Country", "name": "Spain"},
              {"@type": "Country", "name": "Mexico"},
              {"@type": "Country", "name": "Colombia"},
              {"@type": "Country", "name": "Argentina"}
            ]
          }
        }
      ]
    }"""

    # ---------------- 1. HOMEPAGE ----------------
    homepage_replacements = [
        ("One Flat Price. Everything Included.", "Un Solo Precio Plano. Todo Incluido."),
        ("Get fast web hosting, free .com domain, SSL, business email, and Gemini Pro — all in one simple flat-rate package with flat renewal fees.", 
         "Obtén hosting web rápido, dominio .com gratis, SSL, correo corporativo y Gemini Pro — todo en un paquete simple de tarifa plana sin sorpresas en la renovación."),
        ("Switch to Hosterlo", "Cambiar a Hosterlo"),
        ("Launch Your Website", "Lanzar Mi Web"),
        ("30-Day Money-Back Guarantee", "Garantía de Reembolso de 30 Días"),
        ("No credit card required for setup support", "No se requiere tarjeta para el soporte de configuración"),
        ("All-In-One Website Launch Bundle", "Paquete Todo Incluido para Lanzar Tu Web"),
        ("Everything you need to launch your site in under 5 minutes. No hidden fees, no renewal price hikes.", 
         "Todo lo que necesitas para lanzar tu sitio en menos de 5 minutos. Sin tarifas ocultas ni aumentos de precio al renovar."),
        ("Fast NVMe SSD Storage", "Almacenamiento NVMe SSD Rápido"),
        ("Your site loads instantly on NVMe SSDs.", "Tu sitio carga al instante con discos NVMe SSD."),
        ("LiteSpeed Web Server", "Servidor Web LiteSpeed"),
        ("Up to 5x faster speeds than traditional Apache hosting.", "Velocidades hasta 5 veces mayores que el hosting tradicional."),
        ("Free .com Domain", "Dominio .com Gratis"),
        ("Included free for the first year with annual plans.", "Incluido gratis durante el primer año en planes anuales."),
        ("Business Email Accounts", "Cuentas de Correo Corporativo"),
        ("Create professional addresses using your domain.", "Crea correos profesionales con tu propio dominio."),
        ("Free SSL Certificate", "Certificado SSL Gratis"),
        ("Keep customer data secure and boost your SEO.", "Protege los datos de tus clientes y mejora tu SEO."),
        ("Gemini Pro AI (18 Months)", "Gemini Pro IA (18 Meses)"),
        ("Premium AI model included to assist with writing.", "Modelo de IA premium incluido para ayudarte a redactar."),
        ("Reliable Uptime", "Uptime Confiable"),
        ("Tested stability to keep your business online.", "Estabilidad probada para mantener tu negocio en línea."),
        ("WhatsApp Support", "Soporte por WhatsApp"),
        ("Real human experts available via text when you need help.", "Expertos humanos reales disponibles por chat cuando lo necesites."),
        
        ("How It Works", "Cómo Funciona"),
        ("Get online in three easy steps", "Pon tu sitio en línea en tres simples pasos"),
        ("1. Choose Your Domain", "1. Elige tu Dominio"),
        ("Search and select your free .com domain or connect an existing one.", "Busca tu dominio .com gratis o conecta uno que ya tengas."),
        ("2. Complete Your Purchase", "2. Completa tu Compra"),
        ("Get instant access to your cPanel hosting account and billing portal.", "Obtén acceso instantáneo a tu hosting cPanel y portal de facturación."),
        ("3. Start Launching", "3. Comienza a Crear"),
        ("Our support team will contact you via WhatsApp to assist with WordPress installation, email setup, and migrations.", 
         "Nuestro equipo te contactará por WhatsApp para ayudarte con la instalación de WordPress, correos y migraciones."),
         
        ("Why Choose Hosterlo?", "¿Por Qué Elegir Hosterlo?"),
        ("We believe in honest hosting with zero upselling, transparent pricing, and real human support.", 
         "Creemos en un hosting honesto, sin ventas adicionales agresivas, con precios transparentes y soporte humano real."),
        ("No Renewal Price Hikes", "Sin Aumentos al Renovar"),
        ("Unlike GoDaddy or Hostinger, we don't lure you in with low promo rates and double the price on renewal. You pay $59/year now, and $59/year when you renew.", 
         "A diferencia de GoDaddy o Hostinger, no te atraemos con precios promocionales bajos para luego duplicar el precio al renovar. Pagas $59/año hoy y $59/año en tus renovaciones."),
        ("LiteSpeed Speed Caching", "Velocidad LiteSpeed"),
        ("Your website loads up to 5x faster thanks to LiteSpeed Web Server caching and NVMe SSD drives.", 
         "Tu sitio web cargará hasta 5 veces más rápido gracias a la caché de LiteSpeed Web Server y unidades SSD NVMe."),
        ("Real WhatsApp Support", "Soporte Real por WhatsApp"),
        ("Skip the AI chatbots. Talk to real developers and hosting experts directly on WhatsApp whenever you need help.", 
         "Olvídate de los chatbots de IA. Habla con desarrolladores reales y expertos en hosting directamente por WhatsApp cuando lo necesites."),
        ("Free Website Migration", "Migración Web Gratuita"),
        ("Moving from another host? Our team transfers your files, databases, and emails with zero downtime — completely free of charge.", 
         "¿Te cambias de otro proveedor? Nuestro equipo transfiere tus archivos, bases de datos y correos sin tiempo de inactividad — completamente gratis."),

        ("The Website Launch Bundle", "Paquete de Lanzamiento Web"),
        ("Everything you need to launch a fast, professional website.", "Todo lo que necesitas para lanzar un sitio web rápido y profesional."),
        ("Popular", "Popular"),
        ("Launch Bundle", "Paquete Lanzamiento"),
        ("year", "año"),
        ("Order Now", "Comprar Ahora"),
        ("Free .com Domain (First Year)", "Dominio .com Gratis (Primer Año)"),
        ("Unlimited Bandwidth", "Ancho de Banda Ilimitado"),
        ("18 Months Gemini Pro AI", "18 Meses de Gemini Pro IA"),
        ("WhatsApp & Ticket Support", "Soporte por WhatsApp y Ticket"),
        ("30-day money-back guarantee", "Garantía de reembolso de 30 días"),

        ("What Our Customers Say", "Lo Que Dicen Nuestros Clientes"),
        ("Trusted by creators, bloggers, and small business owners worldwide.", "La confianza de creadores, bloggers y dueños de negocios en todo el mundo."),
        ("Founder, Apex Media Agency", "Fundador, Apex Media Agency"),
        ("Store Owner, Ellie's Boutique", "Dueña, Ellie's Boutique"),
        ("Creator, Ben's Travels Blog", "Creador, Ben's Travels Blog"),

        ("Frequently Asked Questions", "Preguntas Frecuentes"),
        ("Everything you need to know about the Website Launch Bundle.", "Todo lo que necesitas saber sobre el Paquete de Lanzamiento Web."),
        ("View FAQ Page", "Ver Todas las Preguntas"),

        ("Ready to Launch Your Website?", "¿Listo para Lanzar tu Sitio Web?"),
        ("Join Hosterlo today and get web hosting, a free domain, business email, SSL, and Gemini Pro — all for just $59/year.", 
         "Únete a Hosterlo hoy y obtén hosting web, dominio gratis, correo corporativo, SSL y Gemini Pro — todo por solo $59/año."),
        ("Get Started Today", "Comenzar Hoy Mismo")
    ]

    translate_page("index.html", 
                   "Hosting Web Barato con Dominio y Correo Gratis | Hosterlo", 
                   "Hosting web barato en España y Latinoamérica por $59/año. Incluye almacenamiento NVMe rápido, dominio .com gratis, correo corporativo, SSL y Gemini Pro.",
                   homepage_replacements, es_org_schema)

    # ---------------- 2. HOSTING OVERVIEW ----------------
    hosting_replacements = [
        ("Simple, Powerful Web Hosting", "Hosting Web Simple y Potente"),
        ("Fast NVMe storage, LiteSpeed performance, free .com domain, and business email — all in one simple plan.", 
         "Almacenamiento NVMe rápido, rendimiento LiteSpeed, dominio .com gratis y correo corporativo — todo en un solo plan."),
        ("View Pricing Plans", "Ver Planes de Precios"),
        ("Hosting Features Built for Speed and Security", "Características de Hosting Diseñadas para Velocidad y Seguridad"),
        ("We combine premium hardware with optimized software to ensure your website loads instantly and stays online.", 
         "Combinamos hardware premium con software optimizado para garantizar que tu sitio web cargue al instante y permanezca en línea."),
        ("Pure NVMe SSD Storage", "Almacenamiento Puro NVMe SSD"),
        ("Your files load up to 10x faster than traditional hard drives.", "Tus archivos cargan hasta 10 veces más rápido que con los discos tradicionales."),
        ("LiteSpeed Web Server", "Servidor Web LiteSpeed"),
        ("The fastest web server technology, fully compatible with WordPress.", "La tecnología de servidor web más rápida, totalmente compatible con WordPress."),
        ("One-Click WordPress Install", "Instalación de WordPress en 1 Clic"),
        ("Launch your WordPress site in seconds with our simple installer.", "Lanza tu sitio WordPress en segundos con nuestro instalador simple."),
        ("Automated Daily Backups", "Copias de Seguridad Diarias"),
        ("Your data is backed up daily so you never lose your work.", "Tus datos se respaldan diariamente para que nunca pierdas tu trabajo."),
        ("Free SSL Certificate", "Certificado SSL Gratis"),
        ("Automatic Let's Encrypt SSL for all your domains.", "Certificado SSL automático de Let's Encrypt para todos tus dominios."),
        ("Advanced Security Shield", "Escudo de Seguridad Avanzado"),
        ("Firewall and DDoS protection built into our global infrastructure.", "Protección contra DDoS y cortafuegos integrados en nuestra infraestructura global."),

        ("Hosting Technology Specifications", "Especificaciones de Nuestra Tecnología"),
        ("Stack Spec", "Especificación"),
        ("Details / Performance Benefit", "Detalles / Beneficios de Rendimiento"),
        ("Web Server", "Servidor Web"),
        ("LiteSpeed Enterprise (compatible with WordPress caching)", "LiteSpeed Enterprise (compatible con caché de WordPress)"),
        ("Storage Drive", "Unidades de Disco"),
        ("Pure Enterprise NVMe SSD in RAID 10 configuration", "NVMe SSD empresarial puro en configuración RAID 10"),
        ("PHP Selector", "Selector de PHP"),
        ("Supports PHP 7.4, 8.0, 8.1, 8.2, and 8.3", "Compatible con PHP 7.4, 8.0, 8.1, 8.2 y 8.3"),
        ("Database", "Base de Datos"),
        ("MariaDB (optimized drop-in MySQL alternative)", "MariaDB (alternativa MySQL optimizada)"),
        ("Control Panel", "Panel de Control"),
        ("cPanel-style management interface for easy setup", "Interfaz de control estilo cPanel para configuración fácil"),

        ("Pricing Plans & Resource Allocation", "Planes de Precios y Recursos"),
        ("Our pricing is simple and transparent. No hidden fees, flat renewal pricing.", 
         "Nuestros precios son simples y transparentes. Sin tarifas ocultas, renovación a precio plano."),
        ("Plan Feature", "Características"),
        ("Website Launch Bundle", "Paquete Lanzamiento"),
        ("Disk Storage", "Almacenamiento"),
        ("15 GB NVMe SSD", "15 GB NVMe SSD"),
        ("Bandwidth Limit", "Límite de Ancho de Banda"),
        ("Unmetered / Unlimited", "No Medido / Ilimitado"),
        ("Free Domain", "Dominio Gratis"),
        ("Yes (free .com for first year)", "Sí (dominio .com gratis el primer año)"),
        ("Business Email", "Cuentas de Correo"),
        ("Unlimited accounts included", "Cuentas ilimitadas incluidas"),
        ("Setup Guidance", "Guía de Configuración"),
        ("Included (via WhatsApp support)", "Incluido (por WhatsApp)"),
        ("Yearly Price", "Precio Anual"),
        ("flat renewal rate", "tarifa de renovación plana"),

        ("Ready to Launch Your Site?", "¿Listo para Lanzar tu Sitio?"),
        ("Get started with our $59/year bundle. Web hosting, free domain, SSL, email, and support included.", 
         "Comienza con nuestro paquete de $59/año. Hosting web, dominio gratis, SSL, correo y soporte incluidos.")
    ]

    translate_page("hosting/index.html", 
                   "Planes de Hosting Web NVMe Rápido y Confiable | Hosterlo", 
                   "Elige el mejor plan de hosting web. Servidores ultra rápidos con tecnología LiteSpeed, SSL gratis, copias de seguridad diarias y soporte por WhatsApp.",
                   hosting_replacements, es_org_schema)

    # ---------------- 3. SHARED HOSTING ----------------
    shared_replacements = [
        ("Affordable Shared Web Hosting", "Hosting Web Compartido Económico"),
        ("Get fast, secure, and reliable web hosting for your website. No complex setups, no hidden pricing hikes.", 
         "Obtén hosting web rápido, seguro y confiable para tu sitio. Sin configuraciones complejas ni aumentos de precio ocultos."),
        ("Choose Shared Hosting", "Elegir Hosting Compartido"),
        ("Why Hosterlo Shared Hosting?", "¿Por Qué el Hosting Compartido de Hosterlo?"),
        ("We offer a simpler shared hosting environment designed for speed and reliability at an honest price.", 
         "Ofrecemos un entorno de hosting compartido más simple diseñado para velocidad y confiabilidad a un precio honesto."),
        ("LiteSpeed Performance", "Rendimiento LiteSpeed"),
        ("Your website is powered by LiteSpeed, delivering faster response times than standard Apache web hosting.", 
         "Tu sitio web funciona con LiteSpeed, ofreciendo tiempos de respuesta más rápidos que el hosting Apache estándar."),
        ("cPanel Interface", "Interfaz cPanel"),
        ("Easily manage your files, databases, email accounts, and backups with our intuitive hosting dashboard.", 
         "Administra fácilmente tus archivos, bases de datos, correos y copias de seguridad con nuestro panel intuitivo."),
        ("Free Site Migration", "Migración de Sitio Gratis"),
        ("Our support team will handle the migration of your website from your old host to Hosterlo at no extra cost.", 
         "Nuestro equipo se encargará de la migración de tu sitio web desde tu proveedor anterior a Hosterlo sin costo extra."),

        ("Everything Included in Our Shared Plan", "Todo Incluido en Nuestro Plan Compartido"),
        ("We pack our shared hosting with features to make launching and managing your website a breeze.", 
         "Equipamos nuestro hosting compartido con características que facilitan el lanzamiento y la administración de tu sitio."),
        ("Start Your Shared Hosting Now", "Iniciar Hosting Compartido Ahora"),
        ("30-Day Money-Back Guarantee Included", "Garantía de Reembolso de 30 Días Incluida")
    ]

    translate_page("hosting/shared-hosting/index.html", 
                   "Hosting Compartido NVMe Barato con cPanel | Hosterlo", 
                   "Hosting compartido de alta velocidad con cPanel. Ideal para blogs y pequeños negocios. Soporte en español, SSL gratis y dominio .com incluido.",
                   shared_replacements, es_org_schema)

    # ---------------- 4. WORDPRESS HOSTING ----------------
    wordpress_replacements = [
        ("Optimized WordPress Hosting", "Hosting WordPress Optimizado"),
        ("Fast, secure, and fully managed WordPress hosting. Build and launch your WordPress site with LiteSpeed caching.", 
         "Hosting WordPress rápido, seguro y totalmente administrado. Construye y lanza tu sitio WordPress con caché LiteSpeed."),
        ("Get WordPress Hosting", "Elegir Hosting WordPress"),
        ("WordPress Hosting Built for Speed", "Hosting WordPress Diseñado para la Velocidad"),
        ("Our servers are tuned specifically for WordPress performance, helping you achieve better page speeds.", 
         "Nuestros servidores están optimizados específicamente para WordPress, ayudándote a mejorar la velocidad de carga."),
        ("LiteSpeed Cache (LSCache)", "Caché de LiteSpeed (LSCache)"),
        ("Get blazing-fast page load times thanks to built-in WordPress page caching at the server level.", 
         "Obtén tiempos de carga ultrarrápidos gracias a la caché de páginas de WordPress integrada a nivel de servidor."),
        ("One-Click WordPress Installer", "Instalador de WordPress en 1 Clic"),
        ("Install WordPress in seconds. Our installer sets up database and configuration automatically.", 
         "Instala WordPress en segundos. Nuestro instalador configura la base de datos de forma automática."),
        ("Automatic Updates", "Actualizaciones Automáticas"),
        ("Keep your WordPress core, themes, and plugins updated automatically to secure your website.", 
         "Mantén el núcleo, temas y plugins de WordPress actualizados automáticamente para mayor seguridad."),

        ("Launch Your WordPress Website Today", "Lanza Tu Web WordPress Hoy Mismo"),
        ("Experience the speed of NVMe drives and LiteSpeed caching. All setup support included.", 
         "Experimenta la velocidad de los discos NVMe y la caché LiteSpeed. Soporte de configuración incluido.")
    ]

    translate_page("hosting/wordpress-hosting/index.html", 
                   "Hosting WordPress Administrado Rápido y Seguro | Hosterlo", 
                   "Hosting WordPress de alto rendimiento con instalación en un clic, almacenamiento NVMe, caché LiteSpeed integrada, seguridad avanzada y soporte.",
                   wordpress_replacements, es_org_schema)

    # ---------------- 5. BUSINESS EMAIL ----------------
    email_replacements = [
        ("Professional Business Email Hosting", "Hosting de Correo Corporativo Profesional"),
        ("Build trust with customer-focused email addresses using your own custom domain name.", 
         "Genera confianza con correos personalizados con tu propio nombre de dominio."),
        ("Get Business Email", "Obtener Correo Corporativo"),
        ("Professional Email Built for Business", "Correos Profesionales Diseñados para Negocios"),
        ("A custom email address shows customers you run a legitimate, established business.", 
         "Una dirección de correo personalizada demuestra a los clientes que eres un negocio establecido."),
        ("Custom Domains", "Dominios Personalizados"),
        ("Create email accounts like name@yourdomain.com for your team.", 
         "Crea cuentas de correo como nombre@tudominio.com para tu equipo."),
        ("Secure Webmail Access", "Acceso Seguro a Webmail"),
        ("Access your email from any browser on any device securely.", 
         "Accede a tu correo de forma segura desde cualquier navegador y dispositivo."),
        ("Spam & Malware Protection", "Protección contra Spam y Virus"),
        ("Filters block unwanted emails and viruses before they hit your inbox.", 
         "Filtros avanzados bloquean correos no deseados y virus antes de que lleguen."),

        ("Everything You Need to Connect", "Todo lo Que Necesitas para Conectarte"),
        ("Our business email hosting is reliable, secure, and easy to connect to Outlook or mobile devices.", 
         "Nuestro hosting de correo es confiable, seguro y fácil de configurar en Outlook o dispositivos móviles."),
        ("Setup Your Business Email", "Configura Tu Correo Corporativo")
    ]

    translate_page("hosting/business-email/index.html", 
                   "Correo Corporativo Profesional con Tu Dominio | Hosterlo", 
                   "Crea cuentas de correo corporativo profesional para tu negocio. Funcionalidades empresariales, antispam y soporte las 24 horas.",
                   email_replacements, es_org_schema)

    # ---------------- 6. DOMAINS OVERVIEW ----------------
    domains_replacements = [
        ("Find the Perfect Domain Name", "Encuentra el Nombre de Dominio Perfecto"),
        ("Register your domain name and start building your brand online today.", 
         "Registra tu nombre de dominio y comienza a construir tu marca en Internet hoy mismo."),
        ("Search Domain", "Buscar Dominio"),
        ("Register Domain", "Registrar Dominio"),
        ("Register Your Domain with Hosterlo", "Registra tu Dominio con Hosterlo"),
        ("We make search, registration, and setup simple with no hidden domain transfer costs.", 
         "Hacemos que la búsqueda, registro y configuración sean simples, sin tarifas ocultas de transferencia."),
        ("Privacy Protection", "Protección de Privacidad"),
        ("We hide your personal details on WHOIS database to prevent spam (where supported).", 
         "Ocultamos tus datos personales en la base de datos WHOIS para evitar spam (donde sea compatible)."),
        ("Easy DNS Management", "Gestión de DNS Fácil"),
        ("Connect your domain to hosting, emails, or third party platforms with ease.", 
         "Conecta tu dominio a hosting, correos o plataformas externas con total facilidad."),
        ("Transparent Pricing", "Precios Transparentes"),
        ("Clear renewal rates so you know exactly what you pay year after year.", 
         "Tarifas de renovación claras para que sepas exactamente cuánto pagas año tras año."),

        ("Popular Domain Extensions", "Extensiones de Dominio Populares"),
        ("The standard extension for global brands and websites.", "La extensión estándar para marcas y sitios web globales."),
        ("The perfect fit for organizations and non-profits.", "La opción perfecta para organizaciones y entidades sin fines de lucro."),
        ("Ideal for technology, SaaS, startups, and websites.", "Ideal para tecnología, empresas SaaS y startups."),

        ("Register Your Domain Today", "Registra Tu Dominio Hoy"),
        ("Find your name, check availability, and secure your domain name instantly.", 
         "Busca tu nombre, comprueba la disponibilidad y asegura tu dominio al instante.")
    ]

    translate_page("domains/index.html", 
                   "Registrar Dominios Baratos | Compra Tu Dominio .com | Hosterlo", 
                   "Busca, registra y compra dominios al mejor precio. Protección WHOIS incluida, redirección de correo y configuración DNS fácil.",
                   domains_replacements, es_org_schema)

    # ---------------- 7. ABOUT HOSTERLO ----------------
    about_replacements = [
        ("About Hosterlo", "Sobre Hosterlo"),
        ("We provide fast, secure, and honest web hosting bundles to help business owners get online.", 
         "Ofrecemos paquetes de hosting web rápidos, seguros y honestos para ayudar a los negocios a estar en línea."),
        ("Learn About Hosterlo", "Conoce Hosterlo"),
        ("Our Core Values", "Nuestros Valores Fundamentales"),
        ("We build hosting services around transparency, reliable speed, and customer service.", 
         "Construimos servicios de hosting basados en la transparencia, velocidad confiable y servicio al cliente."),
        ("Absolute Honesty", "Honestidad Absoluta"),
        ("No renewal shocks, no sneaky addon upsales, no hidden contract commitments.", 
         "Sin sorpresas en la renovación, sin ventas adicionales engañosas ni compromisos de contrato ocultos."),
        ("Simple Launching", "Lanzamiento Simple"),
        ("We bundle domain, email, hosting, SSL, and AI assistance so you start instantly.", 
         "Unimos dominio, correo, hosting, SSL y soporte de IA para que comiences de inmediato."),
        ("Human Support", "Soporte Humano"),
        ("Direct support from human server administrators, avoiding long waiting queues.", 
         "Soporte directo de administradores humanos reales, evitando largas filas de espera."),

        ("Backed by Digioverse Global Infrastructure", "Respaldado por la Infraestructura Global de Digioverse"),
        ("Hosterlo is proud to partner with the Digioverse network, providing enterprise-grade security and speed.", 
         "Hosterlo se enorgullece de asociarse con la red Digioverse, ofreciendo seguridad y velocidad de nivel empresarial."),
        ("Learn more about our partner network.", "Obtén más información sobre nuestra red de socios."),

        ("Our Global Structure", "Nuestra Estructura Global"),
        ("Hosterlo operates globally through localized legal entities to provide localized billing and support:", 
         "Hosterlo opera a nivel mundial a través de entidades legales localizadas para facturación y soporte:"),
        ("Primary market: United States, Canada, Americas", "Mercado principal: Estados Unidos, Canadá y América Latina"),
        ("Primary market: United Kingdom, Europe", "Mercado principal: Reino Unido y Europa"),
        ("Primary market: Pakistan, South Asia", "Mercado principal: Pakistán y Asia del Sur"),
        ("Registered FBR Business", "Negocio Registrado en FBR"),
        ("Company Registration:", "Registro de la Empresa:"),

        ("Join Hosterlo Today", "Únete a Hosterlo Hoy"),
        ("Launch your website on fast NVMe SSD storage with flat-rate annual renewals.", 
         "Lanza tu sitio web en almacenamiento NVMe SSD rápido con renovaciones anuales a tarifa plana.")
    ]

    translate_page("about-hosterlo/index.html", 
                   "Sobre Hosterlo | Hosting Confiable y Transparente | Hosterlo", 
                   "Conoce Hosterlo. Proveedor de hosting web enfocado en la transparencia, velocidad, infraestructura en la nube global y soporte humano.",
                   about_replacements, es_org_schema)

    # ---------------- 8. CONTACT US ----------------
    contact_replacements = [
        ("Contact Hosterlo", "Contactar con Hosterlo"),
        ("Have questions about our hosting bundle, domain setups, or migrations? We are here to help.", 
         "¿Tienes preguntas sobre nuestro paquete de hosting, dominios o migraciones? Estamos aquí para ayudarte."),
        ("Contact Us Now", "Contáctanos Ahora"),
        ("Get in Touch", "Ponte en Contacto"),
        ("Speak to our sales or support team via phone, ticket, or WhatsApp chat.", 
         "Habla con nuestro equipo de ventas o soporte por teléfono, ticket o WhatsApp."),
        ("Send a Message", "Enviar un Mensaje"),
        ("Please fill out the form below and our team will get back to you within a few hours.", 
         "Completa el formulario a continuación y nuestro equipo te responderá en unas pocas horas."),
        ("Your Name", "Tu Nombre"),
        ("Your Email", "Tu Correo"),
        ("How can we help?", "¿Cómo podemos ayudarte?"),
        ("Send Message", "Enviar Mensaje"),

        ("General Support", "Soporte General"),
        ("For setup support, domains, billing, or site migrations.", "Para soporte de configuración, dominios, facturación o migraciones."),
        ("WhatsApp Chat", "Chat de WhatsApp"),
        ("Our fastest support option.", "Nuestra opción de soporte más rápida."),
        ("Email Ticket", "Ticket de Soporte"),
        ("Typical response in 1-2 hours.", "Respuesta típica en 1 a 2 horas."),

        ("Delaware Registered Office", "Oficina Registrada en Delaware"),
        ("Hosterlo LLC registration location for corporate compliance.", "Ubicación de registro de Hosterlo LLC para cumplimiento corporativo.")
    ]

    translate_page("contact-us/index.html", 
                   "Contacto | Soporte y Ventas de Hosting Web | Hosterlo", 
                   "Ponte en contacto con Hosterlo. Soporte técnico de hosting, ayuda con migraciones y consultas comerciales por WhatsApp y ticket.",
                   contact_replacements, es_org_schema)

    # ---------------- 9. PRICING ----------------
    pricing_replacements = [
        ("Transparent Hosting Pricing", "Precios Transparentes de Hosting"),
        ("Simple yearly billing with no unexpected price increases. Everything you need in one bundle.", 
         "Facturación anual simple sin aumentos inesperados de precios. Todo lo que necesitas en un solo paquete."),
        ("View Hosting Bundle", "Ver Paquete de Hosting"),
        ("The Website Launch Bundle Details", "Detalles del Paquete de Lanzamiento Web"),
        ("One simple package containing hosting, domain, email, security, and AI tools.", 
         "Un paquete simple que contiene hosting, dominio, correo, seguridad y herramientas de IA."),
        ("WhatsApp Setup Support", "Soporte de Configuración por WhatsApp"),
        ("30-Day Money-Back Shield", "Garantía de Reembolso de 30 Días"),
        ("Order Launch Bundle", "Comprar Paquete Lanzamiento"),
        ("What makes our pricing different?", "¿Qué hace que nuestro precio sea diferente?"),
        ("No Promotional Traps", "Sin Trampas Promocionales"),
        ("Most hosts show a cheap price like $2/mo but charge $12/mo when you renew. Hosterlo renewal price is exactly the same as you pay now.", 
         "La mayoría de los servidores muestran un precio promocional bajo como $2/mes pero cobran $12/mes al renovar. El precio de renovación de Hosterlo es exactamente el mismo que pagas hoy."),
        ("Email Included Free", "Correo Incluido Gratis"),
        ("Competitors charge extra for email addresses. We include unlimited business email accounts in your plan.", 
         "La competencia cobra extra por las direcciones de correo. Nosotros incluimos cuentas ilimitadas de correo corporativo."),
        ("AI Tool Bonus", "Bono de Herramienta de IA"),
        ("We include 18 months of Gemini Pro to help you write content and build your site faster.", 
         "Incluimos 18 meses de Gemini Pro para ayudarte a escribir contenidos y crear tu sitio más rápido.")
    ]

    translate_page("pricing/index.html", 
                   "Planes y Precios de Hosting Web Todo Incluido | Hosterlo", 
                   "Precios transparentes de hosting web. Paquete de lanzamiento por $59/año con todo lo que necesitas para iniciar tu sitio web.",
                   pricing_replacements, es_org_schema)

    # ---------------- 10. FAQ ----------------
    faq_replacements = [
        ("Frequently Asked Questions", "Preguntas Frecuentes"),
        ("Got questions about Hosterlo hosting, domains, or setups? Find your answers here.", 
         "¿Tienes preguntas sobre el hosting, dominios o configuraciones de Hosterlo? Encuentra las respuestas aquí."),
        ("Search FAQ", "Buscar Preguntas"),
        ("General Questions", "Preguntas Generales"),
        ("Hosting & Technical", "Hosting y Aspectos Técnicos"),
        ("Domains & Billing", "Dominios y Facturación"),
        ("What is included in the $59/year Website Launch Bundle?", "¿Qué está incluido en el Paquete de Lanzamiento Web de $59/año?"),
        ("The bundle includes web hosting, a free .com domain, business email, SSL, setup guidance, support, and Gemini Pro for 18 months.", 
         "El paquete incluye hosting web, dominio .com gratis, correo corporativo, SSL, guía de configuración, soporte y Gemini Pro por 18 meses."),
        ("Is the .com domain really included?", "¿El dominio .com realmente está incluido?"),
        ("Yes. The $59/year bundle includes a free .com domain for your website.", 
         "Sí. El paquete de $59/año incluye un dominio .com gratuito para tu sitio web."),
        ("Can I use WordPress with this hosting?", "¿Puedo usar WordPress con este hosting?"),
        ("Yes. Hosterlo supports WordPress and provides one-click setup options to help you launch faster.", 
         "Sí. Hosterlo es totalmente compatible con WordPress y proporciona opciones de instalación en un clic para ayudarte a lanzar rápido."),
        ("Is this good for beginners?", "¿Es adecuado para principiantes?"),
        ("Yes. Hosterlo is made for beginners, small businesses, creators, and website owners who want a simple way to start online.", 
         "Sí. Hosterlo está diseñado para principiantes, creadores, emprendedores y dueños de negocios que buscan una forma sencilla de empezar en Internet."),
        ("Do I get business email?", "¿Obtengo cuentas de correo corporativo?"),
        ("Yes. Business email is included so you can create a professional email address using your domain name.", 
         "Sí. El correo corporativo está incluido para que puedas crear direcciones profesionales con tu nombre de dominio."),
        ("What is the Gemini Pro bonus?", "¿Qué es el bono de Gemini Pro?"),
        ("Gemini Pro is included for 18 months as a bonus with the Website Launch Bundle. It helps with writing, planning, content ideas, and productivity.", 
         "Gemini Pro se incluye durante 18 meses como bono con el paquete de lanzamiento. Te ayuda a redactar, planificar y crear contenido de forma más productiva."),
        ("How does the 30-day money-back guarantee work?", "¿Cómo funciona la garantía de reembolso de 30 días?"),
        ("If you are not satisfied within the first 30 days of your purchase, contact our support team and we will issue a full refund of your hosting fee. Domain registration fees are non-refundable.", 
         "Si no estás satisfecho dentro de los primeros 30 días, ponte en contacto con soporte y te reembolsaremos la tarifa de hosting. El registro de dominio no es reembolsable."),
        ("Can I migrate my existing website to Hosterlo?", "¿Puedo migrar mi sitio web actual a Hosterlo?"),
        ("Yes. Our team provides free website migration assistance. We will transfer your files, databases, and emails from your current host to Hosterlo with zero downtime.", 
         "Sí. Nuestro equipo te ofrece asistencia gratuita para migrar tu sitio. Transferimos tus archivos, bases de datos y correos sin tiempo de inactividad."),
        ("What payment methods does Hosterlo accept?", "¿Qué métodos de pago acepta Hosterlo?"),
        ("We accept all major credit cards (Visa, Mastercard), PayPal, and Stripe. For Pakistan customers, we also support JazzCash, EasyPaisa, and bank transfer.", 
         "Aceptamos las principales tarjetas de crédito (Visa, Mastercard), PayPal y Stripe. Para clientes en Pakistán, también admitimos JazzCash, EasyPaisa y transferencia."),
        ("How do I get started after purchase?", "¿Cómo empiezo después de realizar la compra?"),
        ("After purchase, our support team contacts you via WhatsApp or email within a few hours to guide you through setting up your hosting, domain DNS, email, and WordPress installation.", 
         "Después de la compra, nuestro equipo te contactará por WhatsApp o correo en unas horas para guiarte en la configuración del hosting, DNS del dominio, correo y WordPress."),
        ("Can I cancel my hosting anytime?", "¿Puedo cancelar mi cuenta de hosting en cualquier momento?"),
        ("Yes. You can cancel your hosting subscription anytime from your client portal. If within 30 days, you qualify for a full refund.", 
         "Sí. Puedes cancelar tu suscripción en cualquier momento desde tu panel de cliente. Si estás dentro de los primeros 30 días, calificas para reembolso."),
        ("Is my data secure with Hosterlo?", "¿Mis datos están seguros con Hosterlo?"),
        ("Yes. All websites hosted with Hosterlo are protected with free SSL, daily automated backups, DDoS protection, and firewall security through our Digioverse infrastructure partnership.", 
         "Sí. Todos los sitios alojados están protegidos con SSL gratis, copias de seguridad diarias, protección DDoS y cortafuegos mediante nuestra asociación con Digioverse."),
        ("Do you offer phone support?", "¿Ofrecen soporte telefónico?"),
        ("Yes. You can reach us by phone or WhatsApp at our US number +1 (618) 356-1311. WhatsApp is our fastest support channel with typical response times under 15 minutes.", 
         "Sí. Puedes contactarnos por teléfono o WhatsApp en el +1 (618) 356-1311. WhatsApp es nuestro canal más rápido con respuestas en menos de 15 minutos."),
        ("Does Hosterlo support WooCommerce and ecommerce stores?", "¿Hosterlo es compatible con WooCommerce y tiendas online?"),
        ("Yes. Hosterlo's LiteSpeed hosting is compatible with WooCommerce and all major WordPress ecommerce plugins. Our NVMe SSD servers ensure fast product page loading times.", 
         "Sí. El hosting LiteSpeed es plenamente compatible con WooCommerce y plugins de e-commerce. Los servidores NVMe aseguran cargas rápidas de páginas."),
        ("Is Hosterlo a legitimate registered company?", "¿Hosterlo es una empresa registrada legítima?"),
        ("Yes. Hosterlo LLC is a legally registered company in the United States, operating at 16192 Coastal Highway, Lewes, DE 19958, United States. We also operate Hosterlo Ltd in the United Kingdom and Hosterlo Pakistan (FBR Registered) for our regional markets.", 
         "Sí. Hosterlo LLC es una empresa registrada legalmente en Estados Unidos, en la dirección 16192 Coastal Highway, Lewes, DE 19958. También operamos Hosterlo Ltd en el Reino Unido y Hosterlo Pakistan."),

        ("Still Have Questions?", "¿Aún Tienes Preguntas?"),
        ("If you cannot find the answers you are looking for, please contact our support team.", 
         "Si no encuentras las respuestas que buscas, por favor ponte en contacto con nuestro equipo de soporte.")
    ]

    translate_page("faq/index.html", 
                   "Preguntas Frecuentes sobre Hosting y Dominios | Hosterlo", 
                   "Respuestas a las preguntas más frecuentes sobre hosting web, registro de dominios, migración gratuita, correo corporativo y Gemini Pro.",
                   faq_replacements, es_org_schema)


if __name__ == "__main__":
    main()
