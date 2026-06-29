import os

def replace_in_file(fp, replacements):
    if not os.path.exists(fp):
        print(f"Warning: File not found: {fp}")
        return False
        
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
        
    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Optimized keywords in: {os.path.relpath(fp, os.path.dirname(fp))}")
        return True
    return False

def main():
    root_dir = r"d:\Hosterlo Official Site"
    
    # ---------------- US Homepage replacements ----------------
    us_home_replacements = [
        ('<title>Cheap Web Hosting with Free Domain &amp; Email | Hosterlo</title>',
         '<title>Cheap Web Hosting with Free Domain &amp; Email 2026 | Hosterlo</title>'),
        ('<meta name="description" content="Get fast NVMe hosting in the USA with a free .com domain, custom business email, SSL, and Premium AI Writer. Cheap web hosting starting at $4.08/mo.">',
         '<meta name="description" content="Get cheap web hosting with a free .com domain and professional business email. Hosterlo offers the best web hosting for small business starting at $4.08/mo.">'),
        ('Cheap Web Hosting with Free Domain &amp; Email for $4.08/mo',
         'Cheap Web Hosting with Free Domain &amp; Business Email')
    ]
    replace_in_file(os.path.join(root_dir, 'index.html'), us_home_replacements)
    
    # ---------------- UK Homepage replacements ----------------
    uk_home_replacements = [
        ('<title>Hosterlo | Web Hosting with Free Domain, Email &amp; Premium AI Writer</title>',
         '<title>Cheap UK Web Hosting with Free Domain &amp; Email 2026 | Hosterlo</title>'),
        ('<meta name="description" content="Launch your website with Hosterlo starting at £3.25/mo. Get fast web hosting, a free .com domain, business email, SSL, setup support, and Premium AI Writer Access.">',
         '<meta name="description" content="Get cheap UK web hosting with a free .com domain and professional business email. Hosterlo offers the best web hosting for small business starting at £3.25/mo.">'),
        ('Affordable Web Hosting UK | Fast Hosting &amp; Free Domain for £3.25/mo',
         'Cheap UK Web Hosting | Free Domain &amp; Business Email')
    ]
    replace_in_file(os.path.join(root_dir, 'uk', 'index.html'), uk_home_replacements)
    
    # ---------------- PK Homepage replacements ----------------
    pk_home_replacements = [
        ('<title>Hosterlo | Web Hosting with Free Domain, Email &amp; Premium AI Writer</title>',
         '<title>Web Hosting in Pakistan - Cheap Hosting with Free Domain | Hosterlo</title>'),
        ('<meta name="description" content="Launch your website with Hosterlo for Rs. 1,150/mo. Get fast hosting, a free .com domain, business email, SSL, setup support, and Premium AI Writer Access.">',
         '<meta name="description" content="Looking for cheap web hosting in Pakistan? Get high-speed NVMe hosting with a free .com domain, business email, and local support starting at Rs. 1,150/mo.">'),
        ('Affordable Web Hosting Pakistan | Fast Hosting &amp; Free Domain for Rs. 1,150/mo',
         'Cheap Web Hosting in Pakistan | Free Domain &amp; Email')
    ]
    replace_in_file(os.path.join(root_dir, 'pk', 'index.html'), pk_home_replacements)
    
    # ---------------- ES Homepage replacements ----------------
    es_home_replacements = [
        ('<title>Hosting Web Barato con Dominio y Correo Gratis | Hosterlo</title>',
         '<title>Hosting Barato con Dominio y Correo Gratis 2026 | Hosterlo</title>'),
        ('<meta name="description" content="Hosting web barato en España y Latinoamérica por $4.08/mes. Incluye almacenamiento NVMe rápido, dominio .com gratis, correo corporativo, SSL y Premium AI Writer.">',
         '<meta name="description" content="Consigue hosting barato con dominio gratis y cuentas de correo corporativo. Hosterlo ofrece el mejor hosting wordpress en España desde $4.08/mes.">'),
        ('Hosting Web Barato | Lanza tu Sitio con Dominio y Correo Gratis por $4.08/mes',
         'Hosting Barato con Dominio Gratis y Correo Corporativo')
    ]
    replace_in_file(os.path.join(root_dir, 'es', 'index.html'), es_home_replacements)

if __name__ == '__main__':
    main()
