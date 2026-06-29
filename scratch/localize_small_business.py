import os
import re

def main():
    root_dir = r"d:\Hosterlo Official Site"
    src_file = os.path.join(root_dir, 'hosting-for-small-business', 'index.html')
    
    if not os.path.exists(src_file):
        print(f"Error: Source file not found at {src_file}")
        return
        
    with open(src_file, 'r', encoding='utf-8', errors='replace') as f:
        original_content = f.read()
        
    # ---------------- 1. UK LOCALIZATION ----------------
    uk_content = original_content
    # Replacements
    uk_replacements = [
        ('https://hosterlo.com/hosting-for-small-business/', 'https://hosterlo.com/uk/hosting-for-small-business/'),
        ('href="/hosting-for-small-business/"', 'href="/uk/hosting-for-small-business/"'),
        ('h1_text = "Best Web Hosting for Small Business USA 2026"', 'h1_text = "Best Web Hosting for Small Business UK 2026"'),
        ('Best Web Hosting for Small Business USA 2026', 'Best Web Hosting for Small Business UK 2026'),
        ('best web hosting for small business websites in the USA.', 'best web hosting for small business websites in the UK.'),
        ('small business hosting USA', 'small business hosting UK'),
        ('USA small businesses', 'UK small businesses'),
        ('US small businesses', 'UK small businesses'),
        ('in the USA?', 'in the UK?'),
        ('$4.08/mo', '£3.25/mo'),
        ('$4.08-200/year', '£3.25-200/year'),
        ('$4.08 price', '£3.25 price'),
        ('at $4.08/mo', 'at £3.25/mo'),
        ('just $4.08/mo', 'just £3.25/mo'),
        ('for $4.08/mo', 'for £3.25/mo'),
        ('for $4.08', 'for £3.25'),
        ('The $4.08/mo', 'The £3.25/mo'),
        ('under $100/year', 'under £80/year'),
        ('+1 (618) 356-1311', '+44 7575 803760'),
        ('+16183561311', '447575803760'),
    ]
    for old, new in uk_replacements:
        uk_content = uk_content.replace(old, new)
        
    uk_dir = os.path.join(root_dir, 'uk', 'hosting-for-small-business')
    if not os.path.exists(uk_dir):
        os.makedirs(uk_dir)
    with open(os.path.join(uk_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(uk_content)
    print("Created UK Small Business page.")
    
    # ---------------- 2. PK LOCALIZATION ----------------
    pk_content = original_content
    pk_replacements = [
        ('https://hosterlo.com/hosting-for-small-business/', 'https://hosterlo.com/pk/hosting-for-small-business/'),
        ('href="/hosting-for-small-business/"', 'href="/pk/hosting-for-small-business/"'),
        ('h1_text = "Best Web Hosting for Small Business USA 2026"', 'h1_text = "Best Web Hosting for Small Business Pakistan 2026"'),
        ('Best Web Hosting for Small Business USA 2026', 'Best Web Hosting for Small Business Pakistan 2026'),
        ('best web hosting for small business websites in the USA.', 'best web hosting for small business websites in Pakistan.'),
        ('small business hosting USA', 'small business hosting Pakistan'),
        ('USA small businesses', 'Pakistan small businesses'),
        ('US small businesses', 'Pakistan small businesses'),
        ('in the USA?', 'in Pakistan?'),
        ('$4.08/mo', 'Rs. 1,150/mo'),
        ('$4.08-200/year', 'Rs. 1,150-50,000/year'),
        ('$4.08 price', 'Rs. 1,150 price'),
        ('at $4.08/mo', 'at Rs. 1,150/mo'),
        ('just $4.08/mo', 'just Rs. 1,150/mo'),
        ('for $4.08/mo', 'for Rs. 1,150/mo'),
        ('for $4.08', 'for Rs. 1,150'),
        ('The $4.08/mo', 'The Rs. 1,150/mo'),
        ('under $100/year', 'under Rs. 30,000/year'),
        ('+1 (618) 356-1311', '+92 3394437730'),
        ('+16183561311', '923394437730'),
    ]
    for old, new in pk_replacements:
        pk_content = pk_content.replace(old, new)
        
    pk_dir = os.path.join(root_dir, 'pk', 'hosting-for-small-business')
    if not os.path.exists(pk_dir):
        os.makedirs(pk_dir)
    with open(os.path.join(pk_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pk_content)
    print("Created PK Small Business page.")
    
    # ---------------- 3. ES LOCALIZATION ----------------
    es_content = original_content
    # Translate lang code
    es_content = es_content.replace('<html class="light" lang="en">', '<html class="light" lang="es">')
    es_content = es_content.replace('<html lang="en">', '<html lang="es">')
    
    es_replacements = [
        ('https://hosterlo.com/hosting-for-small-business/', 'https://hosterlo.com/es/hosting-for-small-business/'),
        ('href="/hosting-for-small-business/"', 'href="/es/hosting-for-small-business/"'),
        
        # Meta tags
        ('Best Web Hosting for Small Business USA 2026 | Hosterlo', 'Mejor Hosting Web para Pequeñas Empresas 2026 | Hosterlo'),
        ('Compare the best web hosting for small business websites in the USA. Hosterlo offers affordable NVMe hosting, free domain, SSL, and email.', 
         'Compara el mejor hosting web para sitios de pequeñas empresas. Hosterlo ofrece hosting NVMe económico, dominio gratis, SSL y correo corporativo.'),
        
        # Navigation menus (Header & Footer global replacements)
        ('Hosting <span', 'Hosting <span'),
        ('Services <span', 'Servicios <span'),
        ('Resources <span', 'Recursos <span'),
        ('Free Website Tools', 'Herramientas Gratis'),
        ('Contact Us</a>', 'Contacto</a>'),
        ('Client Login', 'Portal de Clientes'),
        ('Get the $59 Bundle', 'Obtener Paquete $59'),
        
        # Hero Section
        ('BEST WEB HOSTING FOR SMALL BUSINESS', 'EL MEJOR HOSTING PARA PEQUEÑAS EMPRESAS'),
        ('Best Web Hosting for Small Business USA 2026', 'Mejor Hosting Web para Pequeñas Empresas en 2026'),
        ('Host your small business website with Hosterlo. Get unlimited NVMe hosting, free .com domain, SSL, business email, and expert WhatsApp setup support in one simple $4.08/mo bundle.',
         'Aloja el sitio web de tu pequeña empresa con Hosterlo. Obtén hosting NVMe ilimitado, dominio .com gratis, SSL, correo corporativo y soporte técnico por WhatsApp en un paquete simple de $4.08/mes.'),
        ('Start Business Hosting', 'Comenzar Hosting de Negocio'),
        
        # Subheaders & Features Section
        ('Everything a Small Business Needs', 'Todo lo que un Pequeño Negocio Necesita'),
        ('Start, grow, and manage your website with Hosterlo\'s all-in-one bundle.', 'Comienza, crece y gestiona tu sitio web con el paquete todo en uno de Hosterlo.'),
        ('Fast NVMe SSD Storage', 'Almacenamiento NVMe SSD Rápido'),
        ('Websites load up to 10x faster with solid-state NVMe drives and LiteSpeed caching.', 'Los sitios web cargan hasta 10 veces más rápido con almacenamiento NVMe y caché LiteSpeed.'),
        ('Unlimited Business Email', 'Correo Corporativo Ilimitado'),
        ('Create professional email addresses (e.g., info@yourdomain.com) for your team.', 'Crea correos electrónicos profesionales (ej. info@tudominio.com) para tu equipo.'),
        ('Free .com Domain Name', 'Dominio .com Gratis'),
        ('Get a free eligible domain name for the first year to build your business brand.', 'Consigue un dominio gratis el primer año para crear tu identidad de negocio.'),
        ('Free SSL Certificate', 'Certificado SSL Gratis'),
        ('Secure customer payments and trust with automated HTTPS encryption on all domains.', 'Asegura los pagos y la confianza de tus clientes con cifrado HTTPS automático.'),
        ('WhatsApp Setup Support', 'Soporte por WhatsApp'),
        ('Launch with confidence using our direct WhatsApp assistance for any setup steps.', 'Lanza con total confianza usando nuestra asistencia directa por WhatsApp.'),
        ('Premium AI Writer Bonus', 'Bono de Redactor IA Premium'),
        ('Generate SEO articles, emails, and website copy using Gemini Pro tools (18 months).', 'Genera artículos SEO, correos y textos con herramientas de Gemini Pro (18 meses).'),
        ('1-Click WordPress Install', 'Instalación de WordPress en 1 Clic'),
        ('Set up WordPress, WooCommerce, and standard builder scripts instantly.', 'Instala WordPress, WooCommerce y constructores web de forma instantánea.'),
        ('Flat Renewal Pricing', 'Precio de Renovación Plano'),
        ('The $4.08/mo hosting price remains unchanged upon yearly renewal. No surprise hikes.', 'El precio de hosting de $4.08/mes no cambia en la renovación. Sin sorpresas.'),
        
        # Comparison Section
        ('Hosterlo vs The Big Names', 'Hosterlo frente a los Grandes Nombres'),
        ('Compare Hosterlo\'s flat-rate Website Launch Bundle with standard competitor offerings.', 'Compara el paquete de Hosterlo con tarifas planas frente a los planes de competidores.'),
        ('Hosterlo Bundle', 'Paquete Hosterlo'),
        ('Intro Price', 'Precio Intro'),
        ('Renewal Price', 'Precio de Renovación'),
        ('Hidden Add-ons', 'Extras Ocultos'),
        ('Flat Rate Renewal', 'Renovación Plana'),
        ('No Email Fees', 'Sin Tarifas de Correo'),
        ('Free Setup Help', 'Configuración Gratis'),
        ('Standard Plan', 'Plan Estándar'),
        ('Price Spike', 'Aumento de Precio'),
        ('Paid Emails', 'Correos de Pago'),
        ('Paid SSL', 'SSL de Pago'),
        ('No Help', 'Sin Soporte Directo'),
        
        # FAQ Section
        ('Small Business Hosting FAQs', 'Preguntas Frecuentes sobre Hosting para Negocios'),
        ('What is the best web hosting for small business in the USA?', '¿Cuál es el mejor hosting para pequeños negocios?'),
        ('How much does small business hosting cost?', '¿Cuánto cuesta el hosting para pequeños negocios?'),
        ('Do I need business email for my small business website?', '¿Necesito correo corporativo para mi sitio web de negocios?'),
        ('Can a small business build a website for under $100/year?', '¿Puede un pequeño negocio crear un sitio web por menos de $100/año?'),
        
        # CTA Section
        ('Launch Your Small Business Website Today', 'Lanza el Sitio Web de tu Pequeño Negocio Hoy'),
        ('Get everything you need to start online for just $4.08/mo.', 'Consigue todo lo que necesitas para empezar en Internet por solo $4.08/mes.'),
    ]
    for old, new in es_replacements:
        es_content = es_content.replace(old, new)
        
    es_dir = os.path.join(root_dir, 'es', 'hosting-for-small-business')
    if not os.path.exists(es_dir):
        os.makedirs(es_dir)
    with open(os.path.join(es_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(es_content)
    print("Created ES Small Business page.")

if __name__ == '__main__':
    main()
