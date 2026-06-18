import os
import re

base_dir = r"d:\Hosterlo Official Site"

def optimize_file(file_rel, lang_prefix=""):
    filepath = os.path.join(base_dir, file_rel)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define translated link texts based on language prefix
    if lang_prefix == "es/":
        business_title = "Hosting Corporativo"
        business_desc = "Crea credibilidad con correos profesionales y seguridad HTTPS."
        business_tag = "Popular"
        
        ecommerce_title = "Hosting para E-commerce"
        ecommerce_desc = "Soporte para tiendas online, catálogos de productos y cargas rápidas."
        ecommerce_tag = "Crecimiento"
        
        wp_title = "Hosting WordPress"
        wp_desc = "WordPress preinstalado, caché optimizada y actualizaciones automáticas."
        wp_tag = "Optimizado"
        
        agency_title = "Hosting para Agencias y Portafolio"
        agency_desc = "Gestiona dominios de clientes, bases de datos y muestra tu portafolio."
        agency_tag = "Escalable"
    elif lang_prefix == "pk/":
        business_title = "Business Hosting"
        business_desc = "Build credibility with custom email inboxes & HTTPS security."
        business_tag = "Popular"
        
        ecommerce_title = "Ecommerce Hosting"
        ecommerce_desc = "Support shopping checkouts, product directories & fast page loads."
        ecommerce_tag = "Growth"
        
        wp_title = "WordPress Hosting"
        wp_desc = "Pre-installed WordPress setups, caching & auto security updates."
        wp_tag = "Optimized"
        
        agency_title = "Agency & Portfolio Hosting"
        agency_desc = "Manage client domains, database links & showcase your digital brand."
        agency_tag = "Scalable"
    elif lang_prefix == "uk/":
        business_title = "Business Hosting"
        business_desc = "Build credibility with custom email inboxes & HTTPS security."
        business_tag = "Popular"
        
        ecommerce_title = "Ecommerce Hosting"
        ecommerce_desc = "Support shopping checkouts, product directories & fast page loads."
        ecommerce_tag = "Growth"
        
        wp_title = "WordPress Hosting"
        wp_desc = "Pre-installed WordPress setups, caching & auto security updates."
        wp_tag = "Optimized"
        
        agency_title = "Agency & Portfolio Hosting"
        agency_desc = "Manage client domains, database links & showcase your digital brand."
        agency_tag = "Scalable"
    else:
        business_title = "Business Hosting"
        business_desc = "Build credibility with custom email inboxes & HTTPS security."
        business_tag = "Popular"
        
        ecommerce_title = "Ecommerce Hosting"
        ecommerce_desc = "Support shopping checkouts, product directories & fast page loads."
        ecommerce_tag = "Growth"
        
        wp_title = "WordPress Hosting"
        wp_desc = "Pre-installed WordPress setups, caching & auto security updates."
        wp_tag = "Optimized"
        
        agency_title = "Agency & Portfolio Hosting"
        agency_desc = "Manage client domains, database links & showcase your digital brand."
        agency_tag = "Scalable"

    # Define target URLs with language prefix
    business_url = f"/{lang_prefix}hosting/business-email/"
    ecommerce_url = f"/{lang_prefix}hosting/shared-hosting/"
    wp_url = f"/{lang_prefix}hosting/wordpress-hosting/"
    agency_url = f"/{lang_prefix}hosting/" # Link agency card to hosting catalog overview

    # The block of HTML to find
    # Let's target the exact four cards in their container
    target_block_pattern = r'<!-- Business Hosting -->.*?<!-- Agency Hosting -->.*?</div>\s*</div>\s*</div>\s*</section>'
    
    # We will reconstruct the cards as anchor tags
    new_cards_block = f"""<!-- Business Hosting -->
            <a href="{business_url}" class="block bg-white p-5 rounded-2xl border border-slate-200/50 shadow-sm flex items-center justify-between gap-4 hover:translate-x-1 hover:border-primary/40 hover:shadow transition-all duration-300 group">
                <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-600 shrink-0 group-hover:bg-blue-600 group-hover:text-white transition-all duration-300"><span class="material-symbols-outlined text-lg">storefront</span></div>
                    <div>
                        <h4 class="font-extrabold text-[#111c2d] text-sm group-hover:text-primary transition-colors">{business_title}</h4>
                        <p class="text-slate-500 text-xs mt-0.5">{business_desc}</p>
                    </div>
                </div>
                <span class="px-2.5 py-1 bg-blue-55 text-blue-700 text-[10px] font-black uppercase rounded-full shrink-0">{business_tag}</span>
            </a>
            
            <!-- Ecommerce Hosting -->
            <a href="{ecommerce_url}" class="block bg-white p-5 rounded-2xl border border-slate-200/50 shadow-sm flex items-center justify-between gap-4 hover:translate-x-1 hover:border-primary/40 hover:shadow transition-all duration-300 group">
                <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center text-emerald-600 shrink-0 group-hover:bg-emerald-600 group-hover:text-white transition-all duration-300"><span class="material-symbols-outlined text-lg">shopping_cart</span></div>
                    <div>
                        <h4 class="font-extrabold text-[#111c2d] text-sm group-hover:text-primary transition-colors">{ecommerce_title}</h4>
                        <p class="text-slate-500 text-xs mt-0.5">{ecommerce_desc}</p>
                    </div>
                </div>
                <span class="px-2.5 py-1 bg-emerald-50 text-emerald-700 text-[10px] font-black uppercase rounded-full shrink-0">{ecommerce_tag}</span>
            </a>
            
            <!-- WordPress Hosting -->
            <a href="{wp_url}" class="block bg-white p-5 rounded-2xl border border-slate-200/50 shadow-sm flex items-center justify-between gap-4 hover:translate-x-1 hover:border-primary/40 hover:shadow transition-all duration-300 group">
                <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center text-purple-600 shrink-0 group-hover:bg-purple-600 group-hover:text-white transition-all duration-300"><span class="material-symbols-outlined text-lg">auto_awesome</span></div>
                    <div>
                        <h4 class="font-extrabold text-[#111c2d] text-sm group-hover:text-primary transition-colors">{wp_title}</h4>
                        <p class="text-slate-500 text-xs mt-0.5">{wp_desc}</p>
                    </div>
                </div>
                <span class="px-2.5 py-1 bg-purple-50 text-purple-700 text-[10px] font-black uppercase rounded-full shrink-0">{wp_tag}</span>
            </a>
            
            <!-- Agency Hosting -->
            <a href="{agency_url}" class="block bg-white p-5 rounded-2xl border border-slate-200/50 shadow-sm flex items-center justify-between gap-4 hover:translate-x-1 hover:border-primary/40 hover:shadow transition-all duration-300 group">
                <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center text-amber-600 shrink-0 group-hover:bg-amber-600 group-hover:text-white transition-all duration-300"><span class="material-symbols-outlined text-lg">work</span></div>
                    <div>
                        <h4 class="font-extrabold text-[#111c2d] text-sm group-hover:text-primary transition-colors">{agency_title}</h4>
                        <p class="text-slate-500 text-xs mt-0.5">{agency_desc}</p>
                    </div>
                </div>
                <span class="px-2.5 py-1 bg-amber-50 text-amber-700 text-[10px] font-black uppercase rounded-full shrink-0">{agency_tag}</span>
            </a>
        </div>
    </div>
</section>"""

    # Perform replace using re.sub with DOTALL
    original_segment_pattern = re.compile(r'<!-- Business Hosting -->.*?<!-- Agency Hosting -->.*?(<!-- Agency Hosting -->.*?</span>\s*</div>\s*</div>\s*</div>\s*</section>|</span>\s*</div>\s*</div>\s*</div>\s*</section>)', re.DOTALL)
    
    updated_content = original_segment_pattern.sub(new_cards_block, content)
    if updated_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Successfully optimized linking block on {file_rel}")
    else:
        print(f"Warning: Could not match linking block pattern in {file_rel}")

def main():
    optimize_file("index.html")
    optimize_file("uk/index.html", "uk/")
    optimize_file("pk/index.html", "pk/")
    optimize_file("es/index.html", "es/")

if __name__ == '__main__':
    main()
