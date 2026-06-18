import os
import re
import json

base_dir = r"d:\Hosterlo Official Site"

def make_dirs(filepath):
    dirpath = os.path.dirname(filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

def translate_page(rel_path, title, desc, replacements):
    src_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(src_path):
        print(f"Skipping missing source: {rel_path}")
        return

    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. HTML lang
    content = content.replace('<html class="light" lang="en">', '<html class="light" lang="es">')
    content = content.replace('<html lang="en">', '<html lang="es">')

    # 2. Canonical and OpenGraph urls
    canonical_match = re.search(r'<link rel="canonical" href="https://hosterlo.com/([^"]+)"', content)
    if canonical_match:
        old_canonical = canonical_match.group(0)
        new_canonical = f'<link rel="canonical" href="https://hosterlo.com/es/{canonical_match.group(1)}"'
        content = content.replace(old_canonical, new_canonical)
    
    og_url_match = re.search(r'<meta property="og:url" content="https://hosterlo.com/([^"]+)"', content)
    if og_url_match:
        old_og = og_url_match.group(0)
        new_og = f'<meta property="og:url" content="https://hosterlo.com/es/{og_url_match.group(1)}"'
        content = content.replace(old_og, new_og)

    # Alternate lang tags (hreflangs) update
    # In Spanish page, canonical remains the es version, but alternates point to other versions
    # Hosterlo has standard hreflang blocks. Let's make sure alternate links are preserved.

    # 3. Titles and Descriptions
    content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content)
    content = re.sub(r'<meta property="og:title" content="[^"]+"', f'<meta property="og:title" content="{title}"', content)
    content = re.sub(r'<meta name="twitter:title" content="[^"]+"', f'<meta name="twitter:title" content="{title}"', content)
    
    content = re.sub(r'<meta name="description" content="[^"]+"', f'<meta name="description" content="{desc}"', content)
    content = re.sub(r'<meta property="og:description" content="[^"]+"', f'<meta property="og:description" content="{desc}"', content)
    content = re.sub(r'<meta name="twitter:description" content="[^"]+"', f'<meta name="twitter:description" content="{desc}"', content)

    # 4. Global navigation replacements
    content = content.replace('Hosting <span', 'Hosting <span')
    content = content.replace('Services <span', 'Servicios <span')
    content = content.replace('Resources <span', 'Recursos <span')
    content = content.replace('Cloud Hosting', 'Hosting Cloud')
    content = content.replace('Shared Hosting', 'Hosting Compartido')
    content = content.replace('WordPress Hosting', 'Hosting WordPress')
    content = content.replace('Domains</a>', 'Dominios</a>')
    content = content.replace('Services</a>', 'Servicios</a>')
    content = content.replace('All Services Hub', 'Todos los Servicios')
    content = content.replace('Web Development', 'Desarrollo Web')
    content = content.replace('SaaS Development', 'Desarrollo SaaS')
    content = content.replace('Frontend Development', 'Desarrollo Frontend')
    content = content.replace('Backend Development', 'Desarrollo Backend')
    content = content.replace('UI/UX Design', 'Diseño UI/UX')
    content = content.replace('Mobile App Dev', 'Desarrollo de Apps')
    content = content.replace('API Development', 'Desarrollo de APIs')
    content = content.replace('Website Maintenance', 'Mantenimiento Web')
    content = content.replace('Pricing</a>', 'Precios</a>')
    content = content.replace('Hosterlo Blog', 'Blog de Hosterlo')
    content = content.replace('Free Website Tools', 'Herramientas Gratis')
    content = content.replace('About Hosterlo', 'Sobre Hosterlo')
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

    # Footer
    content = content.replace('Quick Links', 'Enlaces Rápidos')
    content = content.replace('Legal', 'Legal')
    content = content.replace('Terms of Service', 'Términos de Servicio')
    content = content.replace('Privacy Policy', 'Política de Privacidad')
    content = content.replace('Refund Policy', 'Política de Reembolso')
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

    # 5. Schema Locale Updates
    # Set Organization schema to target Spain/Americas
    content = content.replace('"areaServed": "Worldwide"', '"areaServed": [{"@type": "Country", "name": "Spain"}, {"@type": "Country", "name": "Mexico"}, {"@type": "Country", "name": "Colombia"}, {"@type": "Country", "name": "Argentina"}]')
    content = content.replace('"areaServed": {"@type": "Country", "name": "United States"}', '"areaServed": [{"@type": "Country", "name": "Spain"}, {"@type": "Country", "name": "Mexico"}, {"@type": "Country", "name": "Colombia"}, {"@type": "Country", "name": "Argentina"}]')

    # 6. Page-specific replacements
    for orig, rep in replacements:
        content = content.replace(orig, rep)

    # 7. Prefix internal hyperlinks with /es/
    def replace_href(match):
        prefix = "/es/"
        url = match.group(1)
        # Match only relative paths that do not point to assets, external links, anchor fragments, or /es/ itself
        if url.startswith("/") and not url.startswith("//") and not url.startswith("/assets") and not url.startswith("/favicon") and not url.startswith("https://billing."):
            if not url.startswith("/es/"):
                if url == "/":
                    return f'href="{prefix}"'
                return f'href="{prefix}{url[1:]}"'
        return match.group(0)

    content = re.sub(r'href="([^"]+)"', replace_href, content)

    # 8. Write to destination
    dest_path = os.path.join(base_dir, "es", rel_path)
    make_dirs(dest_path)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated Spanish Page: {dest_path}")

def main():
    # ------------------ GROUPS DEFINITIONS ------------------
    
    # 1. Services Hub
    services_replacements = [
        ("Our Core Services", "Nuestros Servicios Principales"),
        ("Custom software engineering, design, and website care plans.", "Desarrollo de software a medida, diseño y planes de mantenimiento web."),
        ("Explore Services", "Explorar Servicios"),
        ("Capabilities", "Capacidades"),
        ("We offer specialized digital services to help startups, brands, and businesses launch high-performing software products.", 
         "Ofrecemos servicios digitales especializados para ayudar a startups, marcas y empresas a lanzar productos de software de alto rendimiento."),
        ("Custom Software Engineering", "Desarrollo de Software a Medida"),
        ("Full-Stack Coding", "Desarrollo Full-Stack"),
        ("We build responsive custom websites, backend APIs, and multi-tenant SaaS MVPs using robust frontend frameworks and secure database links.", 
         "Construimos sitios web personalizados, APIs y MVPs de SaaS utilizando frameworks modernos y bases de datos seguras."),
        ("Figma Prototypes & Design Systems", "Prototipos Figma y Sistemas de Diseño"),
        ("Beautiful UI/UX Layouts", "Diseños UI/UX Atractivos"),
        ("We design click-through wireframes, brand identities, and responsive UI components focused on visual consistency and conversions.", 
         "Diseñamos esquemas interactivos, identidades de marca y componentes de interfaz enfocados en la consistencia visual y conversiones."),
        ("Website Maintenance & Optimization", "Mantenimiento y Optimización Web"),
        ("Performance Audits", "Auditorías de Rendimiento"),
        ("We run speed optimization tasks, malware scans, dependency updates, and support ticket coordination to keep your systems online.", 
         "Realizamos optimizaciones de velocidad, análisis de malware, actualizaciones y soporte para mantener tus sistemas seguros."),
        ("Explore Our Digital Solutions", "Explora Nuestras Soluciones Digitales"),
        ("Choose a specialized digital service block below to view starting packages, timelines, and expert technology stacks.", 
         "Elige un servicio digital especializado a continuación para ver paquetes de inicio, plazos y tecnologías."),
        ("View Service Plan", "Ver Plan de Servicio"),
        ("Web Development", "Desarrollo Web"),
        ("SaaS Development", "Desarrollo SaaS"),
        ("Frontend Development", "Desarrollo Frontend"),
        ("Backend Development", "Desarrollo Backend"),
        ("UI/UX Design", "Diseño UI/UX"),
        ("Mobile App Development", "Desarrollo de Apps Móviles"),
        ("API Development", "Desarrollo de APIs"),
        ("Website Maintenance", "Mantenimiento Web"),
        ("High-performance custom websites built to convert.", "Sitios web personalizados de alto rendimiento para convertir."),
        ("Scalable multi-tenant SaaS products and MVPs.", "Productos SaaS escalables y MVPs multiusuario."),
        ("Interactive, fast interfaces using React & Next.js.", "Interfaces rápidas e interactivas utilizando React y Next.js."),
        ("Secure database structures and server architecture.", "Estructuras de bases de datos seguras y arquitectura de servidores."),
        ("Intuitive design systems and wireframe prototypes.", "Sistemas de diseño intuitivos y prototipos interactivos."),
        ("Native iOS and Android apps built with React Native.", "Apps nativas de iOS y Android construidas con React Native."),
        ("REST & GraphQL APIs for web and mobile interfaces.", "APIs REST y GraphQL para interfaces web y móviles."),
        ("Security updates, speed optimization & daily support.", "Actualizaciones de seguridad, optimización de velocidad y soporte diario.")
    ]
    translate_page("services/index.html", 
                   "Servicios de Agencia Digital y Desarrollo Web | Hosterlo", 
                   "Desarrollo web a medida, SaaS MVP, diseño UI/UX, desarrollo frontend y backend, desarrollo de apps móviles y soporte web en español.", 
                   services_replacements)

    # 2. Web Development
    webdev_replacements = [
        ("Build Your Web Brand", "Construye tu Marca en la Web"),
        ("Web Development Company USA", "Empresa de Desarrollo Web"),
        ("Custom Websites That Convert Visitors Into Customers. Packages start at $999 flat rate.", 
         "Sitios web a medida que convierten visitas en clientes. Paquetes desde $999."),
        ("Get a Free Quote", "Solicitar Presupuesto"),
        ("Back to Services", "Volver a Servicios"),
        ("Fast, Responsive &amp; Conversion-Focused", "Rápido, Adaptable y Enfocado en Conversión"),
        ("We develop high-performance custom websites from scratch, tailored to your brand identity, business workflows, and user expectations. Whether you need a corporate portal, a sales funnel, or a bespoke CMS solution, our expert team writes clean, modular code that loads instantly and ranks on Google.", 
         "Desarrollamos sitios web personalizados de alto rendimiento, adaptados a tu identidad de marca y procesos. Escribimos código limpio y modular que carga al instante."),
        ("Bespoke Responsive Layouts & Design Systems", "Diseños Adaptables Personalizados y Sistemas de Diseño"),
        ("Headless CMS Integration (Next.js + Sanity/Strapi)", "Integración de CMS Headless (Next.js + Sanity/Strapi)"),
        ("Custom WordPress Block Themes & Plugin Engineering", "Temas de Bloques de WordPress y Desarrollo de Plugins"),
        ("SEO-ready Semantics & Schema Markup Included", "Marcado de Esquema y Semántica SEO Incluidos"),
        ("LiteSpeed Optimized", "Optimizado para LiteSpeed"),
        ("Structured to leverage LiteSpeed server caching algorithms for sub-second speeds.", 
         "Estructurado para aprovechar la caché de LiteSpeed y lograr cargas de menos de un segundo."),
        ("Clean Code Quality", "Calidad de Código Limpio"),
        ("Strict adherence to HTML5/CSS3 and JS standards, eliminating bloated frameworks.", 
         "Cumplimiento de estándares de HTML5/CSS3 y JS, eliminando frameworks pesados."),
        ("Expertise &amp; Technology Stack", "Tecnologías y Frameworks"),
        ("OUR WORKFLOW", "NUESTRO PROCESO"),
        ("How We Work", "Cómo Trabajamos"),
        ("We follow a structured, collaborative engineering process to deliver code on time and on budget.", 
         "Seguimos un proceso de ingeniería estructurado para entregar a tiempo y dentro del presupuesto."),
        ("Discovery & Scope", "Descubrimiento y Alcance"),
        ("We outline your user personas, database schemas, and integration points to create a comprehensive project blueprint.", 
         "Definimos tus perfiles de usuario, esquemas de bases de datos e integraciones para crear un plano del proyecto."),
        ("UI/UX Prototyping", "Prototipado UI/UX"),
        ("Our designers build clickable Figma wireframes so you can verify interactive elements before coding starts.", 
         "Nuestros diseñadores crean esquemas en Figma para que verifiques los elementos antes de programar."),
        ("Agile Sprints", "Sprints Ágiles"),
        ("Our engineering team writes clean, component-based code in weekly sprints, providing live demo environments.", 
         "Nuestro equipo escribe código limpio en sprints semanales, ofreciendo entornos de prueba en vivo."),
        ("QA, Launch & Handoff", "Pruebas, Lanzamiento y Entrega"),
        ("We run extensive cross-device tests, optimize speed scores, launch on secure hosting, and transfer ownership.", 
         "Realizamos pruebas en múltiples dispositivos, optimizamos la velocidad y transferimos la propiedad."),
        ("PRICING PLANS", "PLANES DE PRECIOS"),
        ("Starting Project Packages", "Paquetes Iniciales de Proyectos"),
        ("Transparent, flat-rate pricing to fit your phase of business. Choose a plan or request a custom estimate.", 
         "Precios transparentes y de tarifa plana para cada negocio. Elige un plan o solicita un presupuesto."),
        ("Starter Landing Page", "Página de Inicio (Landing Page)"),
        ("starting", " desde"),
        ("Perfect for single-product launches or campaign funnels.", "Perfecto para el lanzamiento de un solo producto o campañas."),
        ("1 Premium Landing Page", "1 Página de Aterrizaje Premium"),
        ("Custom Design Mockup", "Diseño Personalizado"),
        ("Basic Contact Form", "Formulario de Contacto Básico"),
        ("SEO Setup & SSL Integration", "Configuración de SEO e Integración SSL"),
        ("1 Year Shared Hosting Included", "1 Año de Hosting Compartido Incluido"),
        ("Choose plan", "Elegir plan"),
        ("Corporate Website", "Sitio Web Corporativo"),
        ("Ideal for growing businesses needing a strong online presence.", "Ideal para empresas que necesitan una presencia sólida en línea."),
        ("Up to 5 Pages", "Hasta 5 Páginas"),
        ("Advanced Contact/Lead Forms", "Formularios de Contacto Avanzados"),
        ("Custom Graphics & Illustrations", "Gráficos e Ilustraciones a Medida"),
        ("CMS Admin Training Session", "Sesión de Entrenamiento de CMS"),
        ("Custom Web Application", "Aplicación Web a Medida"),
        ("For startups and portals requiring complex database structures.", "Para startups y portales que requieren bases de datos complejas."),
        ("Unlimited Pages / Dynamic Portal", "Páginas Ilimitadas / Portal Dinámico"),
        ("Custom Database & API Integration", "Integración de Base de Datos y API Personalizada"),
        ("User Authentication & Roles", "Autenticación de Usuarios y Roles")
    ]
    translate_page("services/web-development/index.html", 
                   "Empresa de Desarrollo Web a Medida | Hosterlo", 
                   "Desarrollo de sitios web rápidos, seguros y adaptados a tus objetivos de negocio. Páginas corporativas y aplicaciones web a medida en español.", 
                   webdev_replacements)

    # 3. SaaS Development
    saas_replacements = [
        ("Accelerate SaaS Launch", "Acelera el Lanzamiento de tu SaaS"),
        ("SaaS Product Development Company USA | Build SaaS MVP", "Desarrollo de Software SaaS y MVP"),
        ("We Design, Code, and Launch Scalable Multi-Tenant Software Applications. MVPs starting at $4,999.", 
         "Diseñamos, programamos y lanzamos aplicaciones de software SaaS multiusuario. MVPs desde $4,999."),
        ("Custom Multi-Tenant Architectures", "Arquitecturas Multiusuario a Medida"),
        ("Our team builds high-performance SaaS applications with dedicated database links, secure billing configurations, and clean admin panels designed for scale.", 
         "Construimos aplicaciones SaaS con bases de datos dedicadas, integraciones de cobro seguras y paneles de administración modernos."),
        ("Multi-Tenant Database Architectures", "Arquitectura de Bases de Datos Multiusuario"),
        ("Stripe/PayPal Subscription API Integrations", "Integraciones de Pago con Stripe/PayPal"),
        ("Real-Time Analytics & User Dashboards", "Métricas en Tiempo Real y Paneles de Usuario"),
        ("Secure Auth0 / JWT Authentication Systems", "Sistemas de Autenticación Seguros Auth0 / JWT"),
        ("Scalable Cloud Infrastructure Setup", "Configuración de Infraestructura en la Nube Escalable"),
        ("SaaS MVP Starter", "SaaS MVP Inicial"),
        ("Perfect for validating your product idea with real users.", "Perfecto para validar la idea de tu producto con usuarios reales."),
        ("Core Application Workflow", "Flujo de Trabajo de la Aplicación Central"),
        ("Stripe Billing Integration", "Integración de Facturación Stripe"),
        ("Secure JWT User Authentication", "Autenticación de Usuarios Segura JWT"),
        ("Admin Control Panel", "Panel de Control de Administración"),
        ("SaaS Scale Growth", "SaaS de Crecimiento y Escala"),
        ("Designed for growing startups adding multi-tenant features.", "Diseñado para startups en crecimiento que añaden funciones multiusuario."),
        ("Advanced Database Links", "Enlaces Avanzados de Bases de Datos"),
        ("Custom Subdomain Routing", "Enrutamiento de Subdominios Personalizado"),
        ("Email Notification Engine", "Motor de Notificaciones por Correo"),
        ("SaaS Enterprise Portal", "SaaS para Empresas y Portales"),
        ("Bespoke enterprise features, security standards, and audits.", "Funciones personalizadas para empresas, estándares de seguridad y auditorías."),
        ("Unlimited Workflows", "Flujos de Trabajo Ilimitados"),
        ("Single Sign-On (SSO) Support", "Soporte para Inicio de Sesión Único (SSO)"),
        ("Audit Logs & Activity Scans", "Registros de Auditoría y Escaneos de Actividad"),
        ("Dedicated Support SLA", "SLA de Soporte Dedicado")
    ]
    translate_page("services/saas-development/index.html", 
                   "Desarrollo de Software SaaS y MVP | Hosterlo", 
                   "Especialistas en desarrollo de aplicaciones SaaS y MVPs en la nube. Arquitectura multiusuario, integraciones de pago y escalabilidad en español.", 
                   saas_replacements)

    # 4. Frontend Development
    frontend_replacements = [
        ("Responsive User Interfaces", "Interfaces de Usuario Adaptables"),
        ("Frontend Development Company USA | React & Next.js Developers", "Desarrollo Frontend React y Next.js"),
        ("We Build Interactive, Fast, and Accessible Web Interfaces. Packages start at $1,200.", 
         "Construimos interfaces web interactivas, rápidas y accesibles. Paquetes desde $1,200."),
        ("Sleek, Fast & Interactive User Interfaces", "Interfaces de Usuario Modernas, Rápidas e Interactivas"),
        ("We write component-based, clean code using modern frontend frameworks to ensure your web screens load instantly on mobile, tablet, and desktop viewports.", 
         "Escribimos código limpio basado en componentes utilizando frameworks modernos para garantizar rapidez en todos los dispositivos."),
        ("Next.js & React Framework Engineering", "Ingeniería en React y Next.js"),
        ("Tailwind CSS & Utility-First Layouts", "Diseño Adaptable con Tailwind CSS"),
        ("Strict Accessibility (WCAG) Compliance", "Cumplimiento de Accesibilidad (WCAG)"),
        ("Core Web Vitals Optimization", "Optimización de Core Web Vitals"),
        ("Clean JavaScript (ES6+) Component Code", "Componentes de JavaScript Limpios (ES6+)"),
        ("Frontend Static Pack", "Paquete Frontend Estático"),
        ("Perfect for visual design systems and campaign sites.", "Perfecto para sistemas de diseño visual y sitios de campaña."),
        ("Up to 3 Static Templates", "Hasta 3 Plantillas Estáticas"),
        ("CSS Framework Integration", "Integración de Framework CSS"),
        ("Mobile-first Responsive Design", "Diseño Adaptable enfocado en Móvil"),
        ("Frontend Application", "Aplicación Frontend Dinámica"),
        ("Designed for dynamic web applications using React/Next.js.", "Diseñado para aplicaciones dinámicas utilizando React/Next.js."),
        ("Interactive Components & States", "Componentes y Estados Interactivos"),
        ("API Endpoint Connections", "Conexiones de Puntos de API"),
        ("Search Engine Optimization (SEO) Friendly Setup", "Configuración Optimizada para Motores de Búsqueda (SEO)"),
        ("Frontend Portal/Dashboard", "Portal y Panel de Control Frontend"),
        ("For complex user portals with extensive state administration.", "Para portales de usuario complejos con administración de estados avanzados."),
        ("Interactive Data Charts", "Gráficos de Datos Interactivos"),
        ("State Management (Redux/Zustand)", "Gestión de Estados (Redux/Zustand)"),
        ("Real-time Dashboard Components", "Componentes de Panel de Control en Tiempo Real")
    ]
    translate_page("services/frontend-development/index.html", 
                   "Servicios de Desarrollo Frontend React y Next.js | Hosterlo", 
                   "Interfaces de usuario interactivas, rápidas y accesibles. Desarrollo experto en React, Next.js y CSS adaptable en español.", 
                   frontend_replacements)

    # 5. Backend Development
    backend_replacements = [
        ("Secure Server Infrastructure", "Infraestructura Segura de Servidores"),
        ("Backend Development Services USA | Node.js & Python APIs", "Desarrollo Backend y APIs Node.js"),
        ("We Engineer Secure, Scalable, and High-Performance Backend Architectures. Packages start at $1,500.", 
         "Diseñamos arquitecturas backend seguras, escalables y de alto rendimiento. Paquetes desde $1,500."),
        ("Secure, Reliable & Scalable Database Systems", "Bases de Datos Seguras, Confiables y Escalables"),
        ("We develop robust server side architectures, secure database schemas, and clean business logic to handle complex calculations and keep your data safe.", 
         "Desarrollamos arquitecturas sólidas del lado del servidor, bases de datos seguras y lógica de negocios confiable."),
        ("Node.js, Express & Python Backend Servers", "Servidores Backend con Node.js, Express y Python"),
        ("PostgreSQL, MongoDB & MySQL Integrations", "Integraciones con PostgreSQL, MongoDB y MySQL"),
        ("Secure Session & Token Authentication (JWT)", "Autenticación Segura mediante Tokens (JWT)"),
        ("Third-Party API Integration & Sync", "Sincronización e Integración de APIs de Terceros"),
        ("Docker Container Configuration", "Configuración de Contenedores Docker"),
        ("API Database Link", "Enlace de Base de Datos y API"),
        ("Perfect for simple web databases and lead management.", "Perfecto para bases de datos web simples y gestión de contactos."),
        ("Custom Database Setup", "Configuración de Base de Datos"),
        ("CRUD Endpoint Actions", "Acciones CRUD de API"),
        ("Basic Security Settings", "Configuración de Seguridad Básica"),
        ("Dynamic Backend Server", "Servidor Backend Dinámico"),
        ("For web platforms requiring robust user administration.", "Para plataformas web que requieren administración de usuarios avanzada."),
        ("User Auth & Password Cryptography", "Autenticación y Cifrado de Contraseñas"),
        ("File Storage Config (AWS S3)", "Configuración de Almacenamiento (AWS S3)"),
        ("Background Job Coordination", "Coordinación de Procesos en Segundo Plano"),
        ("Enterprise Backend Platform", "Plataforma Backend para Grandes Empresas"),
        ("High-performance server networks and database structures.", "Redes de servidores y bases de datos de alto rendimiento."),
        ("Microservices Architecture", "Arquitectura de Microservicios"),
        ("Advanced Query Caching (Redis)", "Caché de Consultas Avanzada (Redis)"),
        ("Database Sharding & Replication", "Replicación y Fragmentación de Datos")
    ]
    translate_page("services/backend-development/index.html", 
                   "Desarrollo Backend y APIs Node.js | Hosterlo", 
                   "Desarrollo backend robusto y APIs. Servidores rápidos en Node.js y Python, bases de datos integradas y seguridad avanzada en español.", 
                   backend_replacements)

    # 6. UI/UX Design
    uiux_replacements = [
        ("Design Systems & Prototypes", "Sistemas de Diseño y Prototipos"),
        ("UI/UX Design Services USA | Figma Wireframes & Prototypes", "Servicios de Diseño UI/UX y Wireframing"),
        ("We Craft Intuitive, User-Centric Designs That Increase Conversions. Projects start at $800.", 
         "Creamos diseños intuitivos centrados en el usuario que aumentan las conversiones. Proyectos desde $800."),
        ("Intuitive User Journeys & Wireframe Systems", "Viajes de Usuario e Interfaces Intuitivas"),
        ("Our designers focus on visual consistency, layout grids, and interactive states to create beautiful prototypes that software engineers can easily implement.", 
         "Nuestros diseñadores se enfocan en la consistencia visual y cuadrículas de diseño para crear prototipos atractivos."),
        ("Figma Clickable Prototypes & Design Systems", "Prototipos Interactivos de Figma y Sistemas de Diseño"),
        ("Wireframing & Layout Grid Structuring", "Estructura de Alambres (Wireframes) y Cuadrículas"),
        ("Conversion Rate Optimization (CRO) Focused UI", "UI enfocada en la Optimización de la Conversión (CRO)"),
        ("Interactive Component States & Animations", "Estados de Componentes Interactivos y Animaciones"),
        ("User Testing & Journey Mapping", "Pruebas de Usuario y Mapas de Viaje"),
        ("UI/UX Wireframe Kit", "Kit de Wireframes UI/UX"),
        ("Perfect for campaign planning and basic landing designs.", "Perfecto para planificación de campañas y diseños iniciales."),
        ("Figma File Handoff", "Entrega de Archivos Figma"),
        ("Basic Design Grid Setup", "Configuración de Cuadrícula Básica"),
        ("UI/UX Complete Design", "Diseño UI/UX Completo"),
        ("For standard business websites and blogs.", "Para sitios web de negocios estándar y blogs."),
        ("Up to 5 Pages Mockups", "Diseños de hasta 5 Páginas"),
        ("Interactive Clickable Prototype", "Prototipo Interactivo Habilitado"),
        ("Typography & Palette Specs", "Especificaciones de Paleta y Tipografía"),
        ("UI/UX App & Portal Mockup", "Diseño de Aplicación y Portal UI/UX"),
        ("For complex digital platforms and software dashboards.", "Para plataformas digitales complejas y paneles de software."),
        ("Complete Design System Components", "Componentes de Sistema de Diseño Completo"),
        ("Dynamic User Journey Mockup", "Mockup Dinámico del Viaje del Usuario"),
        ("Software Developer Handoff Package", "Paquete de Entrega para Programadores")
    ]
    translate_page("services/ui-ux-design/index.html", 
                   "Servicios de Diseño UI/UX y Wireframing | Hosterlo", 
                   "Diseño de interfaces intuitivas y sistemas de diseño en Figma. Wireframes interactivos y arquitectura de información en español.", 
                   uiux_replacements)

    # 7. Mobile App Development
    mobile_replacements = [
        ("Launch Your Mobile App", "Lanza tu Aplicación Móvil"),
        ("Mobile App Development Company USA | iOS & Android Apps", "Desarrollo de Aplicaciones Móviles"),
        ("We Build Native and Cross-Platform iOS & Android Mobile Apps. Projects start at $5,999.", 
         "Construimos apps móviles nativas e híbridas para iOS y Android. Proyectos desde $5,999."),
        ("High-Performance Native & Cross-Platform Mobile Apps", "Aplicaciones Móviles de Alto Rendimiento"),
        ("We code responsive, fast, and feature-rich mobile apps using modern frameworks to deliver seamless client experiences directly on app stores.", 
         "Programamos apps móviles rápidas y seguras utilizando tecnologías híbridas para una experiencia impecable."),
        ("React Native & Flutter App Development", "Desarrollo con React Native y Flutter"),
        ("App Store (iOS) & Google Play (Android) Submissions", "Publicación en App Store (iOS) y Google Play (Android)"),
        ("Local Storage & Offline Database Integrations", "Almacenamiento Local y Bases de Datos Offline"),
        ("Push Notification & Event Trigger Setup", "Configuración de Notificaciones Push y Alertas"),
        ("Biometric & FaceID Authentication Integrations", "Integración de Seguridad Biométrica y FaceID"),
        ("Mobile App MVP", "MVP de Aplicación Móvil"),
        ("Perfect for validating your mobile app concept with real users.", "Perfecto para validar la idea de tu aplicación con usuarios reales."),
        ("Single Platform Build (iOS or Android)", "Construcción en una sola plataforma (iOS o Android)"),
        ("Basic CRUD Functions", "Funciones Básicas CRUD"),
        ("Push Notification System", "Sistema de Notificaciones Push"),
        ("Submission Support", "Soporte para Publicación"),
        ("Standard Cross-Platform App", "Aplicación Híbrida Estándar"),
        ("For businesses requiring custom apps on both app stores.", "Para negocios que requieren apps en ambas tiendas de aplicaciones."),
        ("React Native Cross-Platform Build", "Construcción Híbrida con React Native"),
        ("Social Login Integration", "Integración de Registro Social"),
        ("In-App Purchase Settings", "Configuración de Compras Integradas"),
        ("Custom Mobile Platform", "Plataforma Móvil Completa"),
        ("Bespoke database sync, high-volume transactions, and admin panels.", "Sincronización de base de datos a medida y paneles de administración."),
        ("Custom Backend Sync Engine", "Motor de Sincronización Backend a Medida"),
        ("Real-time Chat Integrations", "Integraciones de Chat en Tiempo Real"),
        ("Advanced Security Cryptography", "Cifrado de Seguridad Avanzado")
    ]
    translate_page("services/mobile-app-development/index.html", 
                   "Desarrollo de Aplicaciones Móviles | Hosterlo", 
                   "Desarrollo de apps para iOS y Android en React Native. MVP móvil, publicación en tiendas de aplicaciones y soporte en español.", 
                   mobile_replacements)

    # 8. API Development
    api_replacements = [
        ("Connect Your Software", "Conecta tu Software"),
        ("API Development & Integration Services USA | Hosterlo", "Desarrollo e Integración de APIs"),
        ("We Build Secure, Fast, and Highly Connected APIs. Packages start at $1,000.", 
         "Construimos APIs seguras, rápidas y conectadas. Paquetes desde $1,000."),
        ("Secure, Connected & High-Performance Web APIs", "APIs Web Conectadas, Seguras y Rápidas"),
        ("We develop robust API endpoints to connect database architectures with frontend portals, mobile interfaces, or third-party web platforms.", 
         "Desarrollamos puntos de API para conectar bases de datos con interfaces de usuario y plataformas externas."),
        ("RESTful & GraphQL API Architectures", "Arquitecturas de API RESTful y GraphQL"),
        ("JSON Web Token (JWT) Security & OAuth2", "Seguridad JWT y OAuth2 de APIs"),
        ("Stripe, PayPal & Third-Party Integrations", "Integración con Stripe, PayPal y Terceros"),
        ("Automated API Testing (Postman/Jest)", "Pruebas de API Automatizadas (Postman/Jest)"),
        ("Comprehensive API Documentation (Swagger)", "Documentación de API Completa (Swagger)"),
        ("Simple API Endpoint", "Punto de API Simple"),
        ("Perfect for sending contact forms or basic notifications.", "Perfecto para enviar formularios de contacto o notificaciones básicas."),
        ("Up to 5 Dedicated Routes", "Hasta 5 Rutas Dedicadas"),
        ("Basic Query Parameters", "Parámetros de Consulta Básicos"),
        ("Swagger Documentation", "Documentación Swagger Incluida"),
        ("Custom API Integration", "Integración y Desarrollo de API"),
        ("For platforms syncing multiple database databases.", "Para plataformas que sincronizan múltiples bases de datos."),
        ("Advanced JSON Data Layouts", "Estructuras de Datos Complejas JSON"),
        ("OAuth2 Authentication Flow", "Flujo de Autenticación OAuth2"),
        ("API Gateway Setup & Routing", "Configuración de Pasarela y Rutas de API"),
        ("Enterprise API Gateway", "Pasarela de API para Grandes Empresas"),
        ("High-speed API routing structures, request limiting, and cache control.", "Pasarelas de API para alto volumen de peticiones y control de caché."),
        ("Microservice Sync Management", "Gestión de Microservicios"),
        ("Custom Redis Cache Layer", "Capa de Caché Redis a Medida"),
        ("Rate Limiting & Threat Scan", "Limitación de Peticiones y Seguridad")
    ]
    translate_page("services/api-development/index.html", 
                   "Servicios de Desarrollo e Integración de APIs | Hosterlo", 
                   "Servicios profesionales de desarrollo e integración de APIs REST y GraphQL. Integración con pasarelas de pago y documentación Swagger en español.", 
                   api_replacements)

    # 9. Website Maintenance
    maint_replacements = [
        ("Keep Your Website Online", "Mantén tu Sitio Web En Línea"),
        ("Website Maintenance & Support Plans USA | Hosterlo", "Planes de Mantenimiento y Soporte Web"),
        ("We Keep Your Site Fast, Updated, Secure, and Online. Monthly plans start at $49.", 
         "Mantenemos tu sitio rápido, actualizado, seguro y en línea. Planes mensuales desde $49."),
        ("Reliable Website Care, Speed Audits & Security Updates", "Cuidado Web Confiable, Velocidad y Seguridad"),
        ("Our website maintenance packages ensure your digital platforms run smoothly with daily backups, security monitoring, and regular support coordination.", 
         "Nuestros paquetes de mantenimiento garantizan que tu sitio funcione sin interrupciones con monitoreo de seguridad."),
        ("Daily Automated Website Backups", "Copias de Seguridad Diarias Automatizadas"),
        ("Uptime Monitoring & Alert Scans", "Monitoreo de Uptime y Alertas de Caídas"),
        ("Malware Detection & Threat Scans", "Detección de Malware y Virus"),
        ("Core, Theme & Plugin Updates", "Actualizaciones de Núcleo, Temas y Plugins"),
        ("Speed Optimization & Cache Tuning", "Optimización de Velocidad y Caché"),
        ("Basic Care Plan", "Plan de Mantenimiento Básico"),
        ("starting", " desde"),
        ("Perfect for personal blogs and simple marketing pages.", "Perfecto para blogs personales y páginas de marketing simples."),
        ("Monthly Website Audit", "Auditoría Web Mensual"),
        ("Plugin & Theme Updates", "Actualizaciones de Plugins y Temas"),
        ("Daily Security Scans", "Análisis de Seguridad Diarios"),
        ("Email/WhatsApp Support Ticket", "Soporte por Correo y WhatsApp"),
        ("Business Maintenance", "Plan Mantenimiento Negocios"),
        ("For business websites requiring regular content edits.", "Para sitios web comerciales que requieren cambios constantes."),
        ("Daily Backup Recovery Points", "Puntos de Restauración Diarios"),
        ("Uptime Monitoring (5-Min)", "Monitoreo de Uptime cada 5 Minutos"),
        ("1 Hour Custom Edits Included", "1 Hora de Modificaciones Incluida"),
        ("Enterprise Support SLA", "Plan Corporativo / SLA"),
        ("High-performance sites needing dedicated systems support.", "Sitios de alto tráfico que necesitan soporte de sistemas dedicado."),
        ("Real-time Site Monitoring", "Monitoreo en Tiempo Real"),
        ("3 Hours Custom Edits Included", "3 Horas de Modificaciones Incluidas"),
        ("Priority Support Response SLA", "SLA de Soporte Prioritario")
    ]
    translate_page("services/website-maintenance/index.html", 
                   "Planes de Mantenimiento y Soporte Web | Hosterlo", 
                   "Mantenimiento web profesional, actualizaciones de plugins, optimización de velocidad, seguridad contra malware y copias de seguridad en español.", 
                   maint_replacements)

    # 10. Portfolio
    portfolio_replacements = [
        ("Our Showcase Portfolio", "Nuestro Portafolio de Proyectos"),
        ("Portfolio Page | Hosterlo Services", "Portafolio de Casos de Éxito | Hosterlo"),
        ("Explore Case Studies of Fast, Secure Custom Websites and Applications We've Developed.", 
         "Explora casos de éxito de sitios web y aplicaciones a medida que hemos desarrollado."),
        ("Interactive Project Showcase", "Galería de Casos de Éxito"),
        ("Choose a project card below to view detailed features, client objectives, and implemented tech stacks.", 
         "Elige un proyecto a continuación para ver sus características, objetivos y tecnologías."),
        ("All Projects", "Todos los Proyectos"),
        ("Websites", "Sitios Web"),
        ("SaaS Platforms", "Plataformas SaaS"),
        ("Mobile Apps", "Apps Móviles"),
        ("Visit Website", "Visitar Sitio"),
        ("Objectives", "Objetivos"),
        ("Tech Stack", "Tecnologías"),
        
        ("Apex Media Agency Website", "Sitio Web de Apex Media Agency"),
        ("Custom responsive marketing website built to display portfolio works and attract corporate leads.", 
         "Sitio web corporativo a medida diseñado para mostrar casos de estudio y captar prospectos."),
        ("Clean design system, contact form integrations, LiteSpeed cache tuning, and Google SEO configurations.", 
         "Sistema de diseño limpio, integración de formularios, caché LiteSpeed y SEO en Google."),
        
        ("Ellie's Boutique E-commerce", "Tienda Online de Ellie's Boutique"),
        ("Bespoke WooCommerce online store designed for seamless checkout operations and product searches.", 
         "Tienda en línea personalizada con WooCommerce optimizada para búsquedas de productos y pagos rápidos."),
        ("Custom product layout templates, Stripe payment setups, and automated email confirmation notifications.", 
         "Plantillas de productos a medida, pasarela Stripe y notificaciones de correo automáticas."),
        
        ("Venture Drive Portal", "Portal de Venture Drive"),
        ("SaaS MVP application built to manage user registries, files, and subscription billing accounts.", 
         "Aplicación SaaS MVP desarrollada para gestionar registros de usuarios, archivos y suscripciones."),
        ("JWT user authentication, microservices backend databases, and Stripe Billing subscriptions API links.", 
         "Autenticación JWT, bases de datos backend de microservicios y pasarela de facturación Stripe."),
        
        ("Secure Health Patient App", "App de Pacientes Secure Health"),
        ("Cross-platform React Native iOS and Android app designed for clinic scheduling and medical reviews.", 
         "Aplicación híbrida React Native para iOS y Android para agendar citas médicas y revisiones."),
        ("End-to-end data encryption, local storage configurations, and push alert triggers.", 
         "Cifrado de datos de extremo a extremo, almacenamiento local y notificaciones push.")
    ]
    translate_page("portfolio/index.html", 
                   "Portafolio de Proyectos y Casos de Éxito | Hosterlo", 
                   "Explora nuestro portafolio de desarrollo de software. Páginas web corporativas, tiendas online y plataformas SaaS exitosas en español.", 
                   portfolio_replacements)

    # 11. Get a Quote
    quote_replacements = [
        ("Solicitar Presupuesto Gratis", "Solicitar Presupuesto Gratis"),
        ("Get-a-Quote Form | Hosterlo Services", "Solicitar Presupuesto de Desarrollo Web | Hosterlo"),
        ("Please fill out the form below to receive a custom project estimate within 24 hours.", 
         "Completa el formulario a continuación para recibir un presupuesto estimado en 24 horas."),
        ("Your Business Information", "Información de tu Negocio"),
        ("Contact Details", "Detalles de Contacto"),
        ("Tell us about your project", "Cuéntanos sobre tu proyecto"),
        ("Submit Quote Request", "Enviar Solicitud de Presupuesto"),
        ("FullName", "Nombre Completo"),
        ("EmailAddress", "Dirección de Correo"),
        ("Phone Number", "Número de Teléfono"),
        ("Select Service Category", "Selecciona Categoría del Servicio"),
        ("SaaS MVP Development", "Desarrollo SaaS / MVP"),
        ("Custom API Integration", "Integración de APIs"),
        ("Approximate Budget", "Presupuesto Aproximado"),
        ("Description of project scope", "Descripción del proyecto"),
        ("We typically reply within 24 hours.", "Respondemos en menos de 24 horas."),
        ("FullName", "Nombre Completo"),
        ("EmailAddress", "Correo Electrónico"),
        ("Company Name", "Nombre de la Empresa")
    ]
    translate_page("get-a-quote/index.html", 
                   "Solicitar Presupuesto Gratis de Desarrollo Web | Hosterlo", 
                   "Solicita una cotización gratuita para tu proyecto web. Estimaciones rápidas para desarrollo SaaS, páginas web y diseño UI/UX.", 
                   quote_replacements)

    # 12. Niche hosting: Ecommerce
    es_ecom_replacements = [
        ("Ecommerce Web Hosting USA | Free Domain & Email | Hosterlo", "Hosting para Ecommerce Barato | Dominio y Correo | Hosterlo"),
        ("Buy fast ecommerce web hosting in the USA for $59/year. Includes a free .com domain, secure SSL, professional email hosting, and WooCommerce support.", 
         "Compra hosting para e-commerce rápido por $59/año. Incluye dominio .com gratis, certificado SSL, correo corporativo y soporte WooCommerce."),
        ("Fast, Secure Ecommerce Web Hosting USA", "Hosting Web Rápido y Seguro para Ecommerce"),
        ("Launch your online store with Hosterlo's speed-optimized ecommerce hosting. We include everything you need to sell online securely and reliably.", 
         "Lanza tu tienda en línea con nuestro hosting optimizado para e-commerce. Todo lo necesario para vender de forma segura."),
        ("Optimized features for Ecommerce sites", "Características optimizadas para tiendas online"),
        ("Is WooCommerce pre-installed?", "¿WooCommerce viene preinstalado?"),
        ("We can pre-install WordPress and WooCommerce for you for free! Simply request it during checkout or via our WhatsApp setup assistance.", 
         "¡Podemos preinstalar WordPress y WooCommerce completamente gratis! Solicítalo al comprar o vía WhatsApp."),
        ("Do you charge transactional fees?", "¿Cobran comisiones por transacción?"),
        ("No! Hosterlo is a hosting provider, not a payment processor. We charge a flat annual rate and zero extra fees on your sales.", 
         "¡No! Hosterlo es un proveedor de hosting, no un procesador de pagos. Cobramos tarifa plana anual y cero comisiones."),
        ("Why Hosterlo is the Best Pick for Ecommerce Websites", "Por Qué Hosterlo es la Mejor Opción para Tiendas Online"),
        ("Launch Your Ecommerce Page Today", "Lanza Tu Tienda Online Hoy Mismo"),
        ("Start building on speed-optimized cloud infrastructure for just $59/year flat.", 
         "Comienza a vender en servidores rápidos optimizados por solo $59/año tarifa plana.")
    ]
    translate_page("hosting/ecommerce-hosting/index.html", 
                   "Hosting para Ecommerce Barato | Dominio y Correo | Hosterlo", 
                   "Compra hosting para e-commerce rápido por $59/año. Incluye dominio .com gratis, certificado SSL, correo corporativo y soporte WooCommerce.", 
                   es_ecom_replacements)

    # 13. Niche hosting: Blog
    es_blog_replacements = [
        ("Blog Web Hosting USA | Best Hosting for Bloggers | Hosterlo", "Hosting para Blog de WordPress con Dominio Gratis | Hosterlo"),
        ("Start a blog with Hosterlo's affordable blog web hosting in the USA. Get a free .com domain, email, and one-click WordPress install for $59/year.", 
         "Crea un blog con nuestro hosting económico. Obtén dominio .com gratis, correos corporativos e instalación de WordPress en un clic por $59/año."),
        ("Affordable Blog Web Hosting USA", "Hosting de Blogs Económico con Instalador WordPress"),
        ("Start your blogging journey with high-performance blog hosting. Includes a free .com domain, custom email, and pre-installed WordPress to launch faster.", 
         "Inicia tu blog con nuestro hosting de alto rendimiento. Incluye dominio .com gratis, correos y WordPress listo para publicar."),
        ("Optimized features for Blog sites", "Características optimizadas para blogs y creadores"),
        ("Can I migrate my existing blog for free?", "¿Puedo migrar mi blog actual de forma gratuita?"),
        ("Yes! Hosterlo offers free website migration assistance. We'll move your database, media files, and layout with zero downtime.", 
         "¡Sí! Ofrecemos asistencia gratuita de migración de sitios web. Movemos tus archivos y base de datos sin caídas."),
        ("Is WordPress included?", "¿WordPress viene incluido?"),
        ("Yes, we support one-click WordPress installation via cPanel, making it easy for beginners to launch their blog.", 
         "Sí, incluimos la instalación de WordPress en un solo clic por cPanel, facilitando su inicio para principiantes."),
        ("Why Hosterlo is the Best Pick for Blog Websites", "Por Qué Hosterlo es la Mejor Opción para Creadores y Blogs"),
        ("Launch Your Blog Page Today", "Lanza Tu Blog Hoy Mismo")
    ]
    translate_page("hosting/blog-hosting/index.html", 
                   "Hosting para Blog de WordPress con Dominio Gratis | Hosterlo", 
                   "Crea un blog con nuestro hosting económico. Obtén dominio .com gratis, correos corporativos e instalación de WordPress en un clic por $59/año.", 
                   es_blog_replacements)

    # 14. Niche hosting: Cheap Hosting
    es_cheap_replacements = [
        ("Cheap Hosting with Free Domain Name | Hosterlo USA", "Hosting Barato con Dominio y Correo Gratis | Hosterlo"),
        ("Get cheap hosting with a free domain name registration in the USA. Hosterlo's $59/year Website Launch Bundle includes hosting, email, and SSL.", 
         "Consigue hosting barato con registro de dominio gratis. El paquete de $59/año incluye cPanel, correos ilimitados y SSL seguro."),
        ("Cheap Web Hosting with Free Domain Name USA", "Hosting Web Barato con Dominio Gratis"),
        ("Save money with Hosterlo's all-in-one cheap hosting and free eligible .com domain registration package. No hidden renewal cost increases.", 
         "Ahorra dinero con nuestro paquete de hosting económico y dominio .com gratis. Sin incrementos de precios ocultos al renovar."),
        ("Optimized features for Cheap hosting sites", "Características optimizadas de nuestro hosting económico"),
        ("Are there any renewal price jumps?", "¿Hay aumentos de precio al renovar?"),
        ("No. Hosterlo maintains flat-rate renewal pricing. The price you sign up for is exactly the price you renew at.", 
         "No. Hosterlo mantiene renovación a precio plano. El precio de alta es exactamente el de renovación."),
        ("Is email hosting included in the cheap price?", "¿El correo electrónico viene incluido en este precio tan bajo?"),
        ("Yes! Unlike other budget hosts, our annual bundle includes unlimited professional business email accounts at no extra cost.", 
         "¡Sí! A diferencia de otros hosts, incluimos cuentas ilimitadas de correo corporativo profesional sin costos extra."),
        ("Why Hosterlo is the Best Pick for Cheap Hosting Websites", "Por Qué Hosterlo es el Mejor Hosting Barato de Calidad"),
        ("Launch Your Cheap Hosting Page Today", "Lanza Tu Sitio Web Hoy Mismo")
    ]
    translate_page("hosting/cheap-hosting-with-domain/index.html", 
                   "Hosting Barato con Dominio y Correo Gratis | Hosterlo", 
                   "Consigue hosting barato con registro de dominio gratis. El paquete de $59/año incluye cPanel, correos ilimitados y SSL seguro en español.", 
                   es_cheap_replacements)

    # 15. Alternatives: Namecheap
    es_alt_nc_replacements = [
        ("Best Namecheap Alternatives 2026: Cheaper &amp; Faster Web Hosts", "Mejores Alternativas a Namecheap 2026"),
        ("Compare the best Namecheap alternatives in 2026. Honest comparison of SSD server performance, flat renewal pricing, custom email add-ons, and value.", 
         "Compara las mejores alternativas a Namecheap en 2026. Análisis honesto de rendimiento SSD, renovación a precio plano y correos corporativos."),
        ("Best Namecheap Alternatives for 2026", "Mejores Alternativas a Namecheap en 2026"),
        ("Looking for a faster, cheaper, and more reliable alternative to Namecheap? Compare the top Namecheap alternatives below to secure the best value for your website operations.", 
         "¿Buscas una opción más rápida, económica y confiable que Namecheap? Compara las mejores alternativas para tu sitio web."),
        ("Why Find a Namecheap Alternative?", "¿Por Qué Buscar una Alternativa a Namecheap?"),
        ("Namecheap is widely recognized, but users often face recurring issues with their services: While Namecheap offers affordable domain registrations, their budget hosting plans often suffer from slower page load speeds, resource limits under load, and email mailboxes that require extra paid renewals.", 
         "Aunque Namecheap destaca en dominios, sus planes de hosting suelen tener velocidades de carga limitadas y cobran cargos extra por buzones de correo corporativo."),
        ("The Flat-Rate All-In-One Bundle", "El Paquete Todo Incluido a Tarifa Plana"),
        ("Hosterlo completely eliminates pricing tricks. Under a single annual $59 fee, you receive high-performance LiteSpeed cloud hosting, a free domain name, unlimited business email accounts, and direct WhatsApp support with actual systems technicians.", 
         "Hosterlo elimina los trucos de tarifas. Por un pago anual de $59, obtienes hosting LiteSpeed rápido, dominio gratis, correos ilimitados y soporte real por WhatsApp."),
        ("Flat Renewals (No Price Hikes)", "Renovación a Precio Plano (Sin Aumentos)"),
        ("Get the Hosterlo Bundle", "Obtener Paquete Hosterlo"),
        ("Switch to Hosterlo Today", "Cámbiate a Hosterlo Hoy Mismo"),
        ("Get fast LiteSpeed web hosting, free .com domain, SSL, business email, and WhatsApp support for just $59/year.", 
         "Obtén hosting LiteSpeed rápido, dominio gratis, SSL, correos y soporte directo por solo $59/año."),
        ("Get the $59 Bundle", "Obtener Paquete de $59"),
        ("Chat with Support", "Chatear con Soporte"),
        ("Good global scale (requires long-term pre-payment)", "Buena escala global (requiere pago por 4 años)"),
        ("Hostinger is another highly popular option. They offer cheap initial rates, but you must commit to a 48-month contract to secure their best pricing, and renewal costs increase up to 2.5x.", 
         "Hostinger es popular, pero debes contratar 48 meses para obtener su precio más bajo, y al renovar las tarifas aumentan hasta un 250%.")
    ]
    translate_page("alternatives/namecheap/index.html", 
                   "Mejores Alternativas a Namecheap 2026 | Hosterlo", 
                   "Compara las mejores alternativas a Namecheap en 2026. Análisis de rendimiento SSD, renovación a precio plano y correos corporativos.", 
                   es_alt_nc_replacements)

    # 16. Alternatives: Dreamhost
    es_alt_dh_replacements = [
        ("Best DreamHost Alternatives 2026: Flat Pricing &amp; Value Hosts", "Mejores Alternativas a DreamHost 2026"),
        ("Looking for a DreamHost alternative? Compare the top web hosts with faster SSD speeds, flat-rate renewal pricing, and professional custom email plans.", 
         "¿Buscas una opción a DreamHost? Compara los mejores proveedores con velocidad SSD rápida, renovación a precio fijo y correos incluidos."),
        ("Best DreamHost Alternatives for 2026", "Mejores Alternativas a DreamHost en 2026"),
        ("Looking for a faster, cheaper, and more reliable alternative to DreamHost? Compare the top DreamHost alternatives below to secure the best value for your website operations.", 
         "¿Buscas una opción más rápida y económica que DreamHost? Compara las mejores alternativas para tu negocio web."),
        ("Why Find a DreamHost Alternative?", "¿Por Qué Buscar una Alternativa a DreamHost?"),
        ("DreamHost is widely recognized, but users often face recurring issues with their services: DreamHost offers a clean panel interface, but users frequently complain about slow ticket-only response times on their basic plan and the exclusion of custom business email accounts on their cheapest shared hosting tiers.", 
         "DreamHost ofrece un panel intuitivo, pero sus usuarios reportan soporte lento por tickets en el plan básico e inasistencia en correos corporativos en las tarifas de entrada."),
        ("Popular starter host with high renewal fees", "Host inicial popular con altas tarifas de renovación"),
        ("Bluehost is very user friendly but their basic plan lacks built-in backups, excludes free business email accounts, and renews at over $130/year.", 
         "Bluehost es fácil para principiantes pero carece de respaldos incluidos, no trae correos profesionales y renueva a más de $130/año.")
    ]
    translate_page("alternatives/dreamhost/index.html", 
                   "Mejores Alternativas a DreamHost 2026 | Hosterlo", 
                   "¿Buscas una opción a DreamHost? Compara los mejores proveedores con velocidad SSD rápida, renovación a precio fijo y correos incluidos.", 
                   es_alt_dh_replacements)

    # 17. Alternatives: WP Engine
    es_alt_wp_replacements = [
        ("Best WP Engine Alternatives 2026: Affordable Managed WP", "Mejores Alternativas a WP Engine 2026"),
        ("Compare the best WP Engine alternatives in 2026. Get high-performance managed WordPress hosting with LiteSpeed caching, free email, and SSL for less.", 
         "Compara las mejores alternativas a WP Engine en 2026. Hosting WordPress rápido con caché LiteSpeed y correos por un precio justo."),
        ("Best WP Engine Alternatives for 2026", "Mejores Alternativas a WP Engine en 2026"),
        ("Looking for a faster, cheaper, and more reliable alternative to WP Engine? Compare the top WP Engine alternatives below to secure the best value for your website operations.", 
         "¿Buscas una opción más económica que WP Engine pero veloz? Compara las alternativas para tu sitio WordPress."),
        ("Why Find a WP Engine Alternative?", "¿Por Qué Buscar una Alternativa a WP Engine?"),
        ("WP Engine is widely recognized, but users often face recurring issues with their services: WP Engine is extremely fast but costs a premium ($20+/month) and completely blocks email hosting, forcing users to buy external Google Workspace or Microsoft 365 licenses.", 
         "WP Engine es sumamente rápido pero sus costos son elevados ($20+/mes) y no ofrece hosting de correos, obligando a comprar licencias externas de Google o Microsoft."),
        ("Managed WordPress on Google Cloud nodes", "WordPress administrado en nodos de Google Cloud"),
        ("SiteGround offers fast WordPress caching and tools, but they enforce strict storage and visitor count caps, and renewal costs jump to $14.99/mo.", 
         "SiteGround ofrece buena caché, pero restringe estrictamente el almacenamiento y las visitas, y su renovación salta a $14.99/mes.")
    ]
    translate_page("alternatives/wpengine/index.html", 
                   "Mejores Alternativas a WP Engine 2026 | Hosterlo", 
                   "Compara las mejores alternativas a WP Engine en 2026. Hosting WordPress rápido con caché LiteSpeed y correos por un precio justo.", 
                   es_alt_wp_replacements)

    # 18. Comparisons: Bluehost
    es_comp_bh_replacements = [
        ("Hosterlo vs Bluehost 2026: Honest Comparison (Pricing &amp; Speed)", "Hosterlo vs Bluehost: Comparativa Honesta 2026 (Precio y Velocidad)"),
        ("Compare Hosterlo vs Bluehost in 2026. Honest breakdown of hosting speeds, support channels, renewal price hikes, and overall package value.", 
         "Comparación honesta entre Hosterlo y Bluehost en 2026. Análisis de precios, velocidad de carga, soporte al cliente y sorpresas de renovación."),
        ("Hosterlo vs Bluehost", "Hosterlo vs Bluehost"),
        ("Is Hosterlo better than Bluehost?", "¿Es Hosterlo mejor que Bluehost?"),
        ("Compare features, support, speeds, and real renewal costs below.", "Compara características, soporte técnico, velocidades y renovaciones reales a continuación."),
        ("Switch to Hosterlo Today", "Cámbiate a Hosterlo Hoy"),
        ("The Verdict: Why Hosterlo Wins", "El Veredicto: Por Qué Hosterlo Gana"),
        ("Bluehost is a dominant brand, but they lure beginners in with promo rates that double on renewal. Hosterlo charges a flat $59/year rate that remains flat forever, with WhatsApp support and WordPress optimized caching.", 
         "Bluehost es una gran marca, pero atrae con tarifas bajas para duplicar el costo al renovar. Hosterlo cuesta $59/año fijos con soporte real por WhatsApp."),
        ("Feature Comparison", "Comparación de Características"),
        ("Hosterlo", "Hosterlo"),
        ("Bluehost", "Bluehost"),
        ("Yearly Cost", "Costo Anual"),
        ("Renewal Pricing", "Precio de Renovación"),
        ("cPanel Access", "Acceso a cPanel"),
        ("Free Backups", "Respaldos Gratis"),
        ("Business Email", "Correo Corporativo"),
        ("Uptime tested", "Uptime probado"),
        ("WhatsApp support", "Soporte WhatsApp"),
        ("Yes (Unlimited)", "Sí (Ilimitado)"),
        ("No (Paid addon)", "No (Adicional de pago)"),
        ("Compare Other Web Hosts", "Comparar con Otros Proveedores")
    ]
    translate_page("compare/hosterlo-vs-bluehost/index.html", 
                   "Hosterlo vs Bluehost: Comparativa Honesta 2026 | Hosterlo", 
                   "Comparación honesta entre Hosterlo y Bluehost en 2026. Análisis de precios, velocidad de carga, soporte al cliente y sorpresas de renovación.", 
                   es_comp_bh_replacements)

    # 19. Comparisons: Hostinger
    es_comp_hi_replacements = [
        ("Hosterlo vs Hostinger 2026: Honest Comparison (Pricing &amp; Speed)", "Hosterlo vs Hostinger: Comparativa Honesta 2026 (Precio y Velocidad)"),
        ("Compare Hosterlo vs Hostinger in 2026. Honest breakdown of hosting speeds, support channels, renewal price hikes, and overall package value.", 
         "Comparación honesta entre Hosterlo y Hostinger en 2026. Análisis de velocidades, panel de control, canales de soporte y precios de renovación."),
        ("Hosterlo vs Hostinger", "Hosterlo vs Hostinger"),
        ("Is Hosterlo better than Hostinger?", "¿Es Hosterlo mejor que Hostinger?"),
        ("Hostinger requires a 4-year upfront contract to get their advertised low pricing, and they do not use standard cPanel. Hosterlo offers cPanel utility, flat renewals, and direct expert setup support.", 
         "Hostinger requiere un contrato por 4 años para obtener su precio promocional y no usa cPanel estándar. Hosterlo ofrece cPanel, renovación fija y soporte.")
    ]
    translate_page("compare/hosterlo-vs-hostinger/index.html", 
                   "Hosterlo vs Hostinger: Comparativa Honesta 2026 | Hosterlo", 
                   "Comparación honesta entre Hosterlo y Hostinger en 2026. Análisis de velocidades, panel de control, canales de soporte y precios de renovación.", 
                   es_comp_hi_replacements)

    # 20. Comparisons: Siteground
    es_comp_sg_replacements = [
        ("Hosterlo vs SiteGround 2026: Honest Comparison (Pricing &amp; Speed)", "Hosterlo vs SiteGround: Comparativa Honesta 2026 (Precio y Velocidad)"),
        ("Compare Hosterlo vs SiteGround in 2026. Honest breakdown of hosting speeds, support channels, renewal price hikes, and overall package value.", 
         "Comparación honesta entre Hosterlo y SiteGround en 2026. Análisis de rendimiento WordPress, límites de espacio en disco y precios."),
        ("Hosterlo vs SiteGround", "Hosterlo vs SiteGround"),
        ("Is Hosterlo better than SiteGround?", "¿Es Hosterlo mejor que SiteGround?"),
        ("SiteGround is fast but heavily limits storage space (10GB) and renewal fees jump to $180+/year. Hosterlo includes 15GB NVMe SSD storage and unlimited email accounts for $59/year flat.", 
         "SiteGround es rápido pero restringe el almacenamiento (10GB) y su renovación supera los $180/año. Hosterlo incluye 15GB NVMe SSD y correos ilimitados por $59/año.")
    ]
    translate_page("compare/hosterlo-vs-siteground/index.html", 
                   "Hosterlo vs SiteGround: Comparativa Honesta 2026 | Hosterlo", 
                   "Comparación honesta entre Hosterlo y SiteGround en 2026. Análisis de rendimiento WordPress, límites de espacio en disco y precios.", 
                   es_comp_sg_replacements)

    # 21. Comparisons: GoDaddy
    es_comp_gd_replacements = [
        ("Hosterlo vs GoDaddy 2026: Honest Comparison (Pricing &amp; Speed)", "Hosterlo vs GoDaddy: Comparativa Honesta 2026 (Precio y Velocidad)"),
        ("Compare Hosterlo vs GoDaddy in 2026. Honest breakdown of hosting speeds, support channels, renewal price hikes, and overall package value.", 
         "Comparación honesta entre Hosterlo y GoDaddy en 2026. Análisis de cargos adicionales por SSL, correos corporativos y costo de renovación."),
        ("Hosterlo vs GoDaddy", "Hosterlo vs GoDaddy"),
        ("Is Hosterlo better than GoDaddy?", "¿Es Hosterlo mejor que GoDaddy?"),
        ("GoDaddy charges extra for SSL certificates, backups, and email mailboxes. Hosterlo packs all launching essentials under a single flat-rate yearly rate of $59.", 
         "GoDaddy cobra adicionales por SSL, respaldos y buzones de correo. Hosterlo reúne todo lo necesario en un solo plan anual de $59 fijos.")
    ]
    translate_page("compare/hosterlo-vs-godaddy/index.html", 
                   "Hosterlo vs GoDaddy: Comparativa Honesta 2026 | Hosterlo", 
                   "Comparación honesta entre Hosterlo y GoDaddy en 2026. Análisis de cargos adicionales por SSL, correos corporativos y costo de renovación.", 
                   es_comp_gd_replacements)

    # 22. Comparisons: Namecheap
    es_comp_nc_replacements = [
        ("Hosterlo vs Namecheap 2026: Honest Comparison (Pricing &amp; Speed)", "Hosterlo vs Namecheap: Comparativa Honesta 2026 (Precio y Velocidad)"),
        ("Compare Hosterlo vs Namecheap in 2026. Honest breakdown of hosting speeds, support channels, renewal price hikes, and overall package value.", 
         "Comparación honesta entre Hosterlo y Namecheap en 2026. Análisis de rendimiento de discos SSD, hosting de correos y precios."),
        ("Hosterlo vs Namecheap", "Hosterlo vs Namecheap"),
        ("Is Hosterlo better than Namecheap?", "¿Es Hosterlo mejor que Namecheap?"),
        ("Namecheap is great for domains but their web servers can load slower under high traffic, and email is a separate recurring cost. Hosterlo includes hosting, .com domain, and unlimited email for one yearly flat fee.", 
         "Namecheap destaca en dominios, pero sus servidores son más lentos ante mucho tráfico y cobran adicionales por correo. Hosterlo incluye todo por una sola tarifa.")
    ]
    translate_page("compare/hosterlo-vs-namecheap/index.html", 
                   "Hosterlo vs Namecheap: Comparativa Honesta 2026 | Hosterlo", 
                   "Comparación honesta entre Hosterlo y Namecheap en 2026. Análisis de rendimiento de discos SSD, hosting de correos y precios.", 
                   es_comp_nc_replacements)

    # 23. Comparisons: Dreamhost
    es_comp_dh_replacements = [
        ("Hosterlo vs DreamHost 2026: Honest Comparison (Pricing &amp; Speed)", "Hosterlo vs DreamHost: Comparativa Honesta 2026 (Precio y Velocidad)"),
        ("Compare Hosterlo vs DreamHost in 2026. Honest breakdown of hosting speeds, support channels, renewal price hikes, and overall package value.", 
         "Comparación honesta entre Hosterlo y DreamHost en 2026. Análisis de tiempos de soporte, correos incluidos y facilidad de uso."),
        ("Hosterlo vs DreamHost", "Hosterlo vs DreamHost"),
        ("Is Hosterlo better than DreamHost?", "¿Es Hosterlo mejor que DreamHost?"),
        ("DreamHost excludes business emails on their entry shared hosting plan and basic support is ticket-only. Hosterlo offers cPanel tools, unlimited business mailboxes, and instant support via WhatsApp.", 
         "DreamHost excluye correos en su tarifa inicial y el soporte es principalmente por tickets. Hosterlo ofrece cPanel, correos ilimitados y chat por WhatsApp.")
    ]
    translate_page("compare/hosterlo-vs-dreamhost/index.html", 
                   "Hosterlo vs DreamHost: Comparativa Honesta 2026 | Hosterlo", 
                   "Comparación honesta entre Hosterlo y DreamHost en 2026. Análisis de tiempos de soporte, correos incluidos y facilidad de uso.", 
                   es_comp_dh_replacements)

    # 24. Comparisons: WP Engine
    es_comp_wpe_replacements = [
        ("Hosterlo vs WP Engine 2026: Honest Comparison (Pricing &amp; Speed)", "Hosterlo vs WP Engine: Comparativa Honesta 2026 (Precio y Velocidad)"),
        ("Compare Hosterlo vs WP Engine in 2026. Honest breakdown of hosting speeds, support channels, renewal price hikes, and overall package value.", 
         "Comparación honesta entre Hosterlo y WP Engine en 2026. Análisis de precios de WordPress administrado y hosting de correos."),
        ("Hosterlo vs WP Engine", "Hosterlo vs WP Engine"),
        ("Is Hosterlo better than WP Engine?", "¿Es Hosterlo mejor que WP Engine?"),
        ("WP Engine is fast but expensive ($20+/month) and completely blocks email hosting. Hosterlo offers fast LiteSpeed WordPress hosting, custom email, and free .com domain for just $59/year.", 
         "WP Engine es veloz pero costoso ($20+/mes) y bloquea el hosting de correos. Hosterlo ofrece WordPress rápido, correos y dominio .com por $59/año.")
    ]
    translate_page("compare/hosterlo-vs-wpengine/index.html", 
                   "Hosterlo vs WP Engine: Comparativa Honesta 2026 | Hosterlo", 
                   "Comparación honesta entre Hosterlo y WP Engine en 2026. Análisis de precios de WordPress administrado y hosting de correos.", 
                   es_comp_wpe_replacements)

    print("\nAll 24 pages compiled and translated to Spanish.")

if __name__ == "__main__":
    main()
