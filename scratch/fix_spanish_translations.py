import os

base_dir = r"d:\Hosterlo Official Site"

replacements_index = [
    # H1 & Subheading
    ("Lanzar Mi Web with Hosting, Domain, Email &amp; Gemini Pro — All for $59/año", 
     "Lanza Tu Sitio Web con Hosting, Dominio, Correo y Gemini Pro — Todo por $59/año"),
    ("Get fast hosting, a free .com domain, SSL security, business email, setup guidance, WhatsApp support, and Gemini Pro for 18 months in one simple website launch bundle.",
     "Obtén hosting web rápido, un dominio .com gratis, seguridad SSL, correo corporativo, guía de configuración, soporte por WhatsApp y la bonificación de Gemini Pro por 18 meses en un solo paquete de lanzamiento."),
    # Domain section subheadline
    ("Start your online journey with a domain name that represents your brand. Search, register, and connect your domain with Hosterlo hosting in minutes.",
     "Inicia tu presencia en línea con un nombre de dominio que represente tu marca. Busca, registra y conecta tu dominio con el hosting de Hosterlo en minutos."),
    # FAQs
    ("Yes. Hosterlo is beginner-friendly and designed to make hosting easier. You can manage your website, domain, emails, SSL, and hosting tools from a simple control panel.",
     "Sí. Hosterlo es ideal para principiantes y está diseñado para facilitar el hosting. Puedes administrar tu sitio web, dominio, correos, SSL y herramientas de hosting desde un panel de control simple."),
    ("Yes. Hosterlo hosting is suitable for WordPress websites, business websites, blogs, portfolios, and ecommerce stores.",
     "Sí. El hosting de Hosterlo es compatible con sitios WordPress, webs de negocios, blogs, portafolios y tiendas online."),
    ("Yes. Hosterlo supports SSL security so your website can use HTTPS and provide a safer browsing experience for visitors.",
     "Sí. Hosterlo admite la seguridad SSL para que tu sitio web pueda usar HTTPS y ofrecer una experiencia de navegación más segura para los visitantes.")
]

replacements_hosting = [
    # Hero / Intro paragraph
    ("Launch your web applications on our speed-optimized cloud node. Hosterlo hosting provides LiteSpeed Enterprise caching, secure solid-state NVMe storage, daily backup safeguards, and pre-sales setup assistance, backed by a 30-day money-back guarantee.",
     "Lanza tus aplicaciones web en nuestro nodo en la nube optimizado para velocidad. El hosting de Hosterlo ofrece caché LiteSpeed Enterprise, almacenamiento SSD NVMe seguro, copias de seguridad de respaldo diarias y asistencia en la configuración, respaldado por una garantía de reembolso de 30 días."),
    # FAQs
    ("What is included in Hosterlo hosting?",
     "¿Qué está incluido en el hosting de Hosterlo?"),
    ("Yes. Hosterlo is made for beginners, small businesses, bloggers, and website owners who want a simple hosting setup with support.",
     "Sí. Hosterlo está diseñado para principiantes, pequeños negocios, creadores y dueños de sitios web que desean una configuración de hosting simple con soporte."),
    ("Yes. Hosterlo hosting supports WordPress websites, business websites, blogs, portfolios, and landing pages.",
     "Sí. El hosting de Hosterlo es compatible con sitios WordPress, webs de negocios, blogs, portafolios y páginas de aterrizaje.")
]

def apply_replacements(file_rel, replacements):
    filepath = os.path.join(base_dir, file_rel)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for orig, rep in replacements:
        content = content.replace(orig, rep)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Applied translations to {file_rel}")

def main():
    apply_replacements("es/index.html", replacements_index)
    apply_replacements("es/hosting/index.html", replacements_hosting)

if __name__ == "__main__":
    main()
