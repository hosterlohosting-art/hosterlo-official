import os
import re

COMPETITORS = {
    'bluehost': 'Bluehost',
    'hostinger': 'Hostinger',
    'siteground': 'SiteGround',
    'godaddy': 'GoDaddy',
    'namecheap': 'Namecheap',
    'dreamhost': 'DreamHost',
    'wpengine': 'WP Engine'
}

def get_interlink_html(market, current_host):
    # Translations
    if market == 'es':
        title = "Compara Hosterlo con otros Proveedores"
        desc = "Descubre cómo se compara Hosterlo frente a los nombres más grandes del hosting."
        card_prefix = "Comparar"
    else:
        title = "Compare Hosterlo With Other Hosts"
        desc = "See how Hosterlo stacks up against the biggest names in web hosting."
        card_prefix = "Compare"
        
    cards = []
    prefix = f"/{market}" if market != 'us' else ""
    
    for host_key, host_name in COMPETITORS.items():
        if host_key == current_host:
            continue
            
        url = f"{prefix}/compare/hosterlo-vs-host_key/"
        # Correctly replace host_key inside string formatting
        url = url.replace('host_key', host_key)
        cards.append(f"""                    <a href="{url}" class="bg-white border border-slate-200 rounded-2xl p-5 text-center hover:border-primary/30 hover:shadow-md transition-all group">
                        <div class="text-xs font-black text-slate-500 uppercase tracking-wider mb-1 group-hover:text-primary">{card_prefix}</div>
                        <div class="font-extrabold text-sm text-[#111c2d]">vs {host_name}</div>
                    </a>""")
                    
    cards_str = '\n'.join(cards)
    
    html = f"""<!-- Compare Other Hosts Section -->
        <section class="py-16 bg-slate-50 border-t border-slate-100">
            <div class="max-w-[1440px] mx-auto px-6">
                <div class="text-center mb-10">
                    <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-primary/5 text-primary text-xs font-black uppercase rounded-full mb-4">MORE COMPARISONS</span>
                    <h2 class="text-2xl font-black text-[#111c2d]">{title}</h2>
                    <p class="text-slate-500 text-sm mt-2">{desc}</p>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
{cards_str}
                </div>
            </div>
        </section>"""
        
    return html

def main():
    root_dir = r"d:\Hosterlo Official Site"
    print("Injecting comparison interlinks...")
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'scratch' in dirs:
            dirs.remove('scratch')
            
        # Check if under compare folder
        parts = os.path.relpath(root, root_dir).replace('\\', '/').split('/')
        if 'compare' in parts and len(parts) > parts.index('compare') + 1:
            folder_after_compare = parts[parts.index('compare') + 1]
            if folder_after_compare.startswith('hosterlo-vs-'):
                for file in files:
                    if file.endswith('.html'):
                        html_files.append((os.path.join(root, file), folder_after_compare.replace('hosterlo-vs-', '')))
                        
    updated_count = 0
    for fp, host in html_files:
        norm_path = os.path.relpath(fp, root_dir).replace('\\', '/')
        parts = norm_path.split('/')
        if parts[0] in ['uk', 'pk', 'es']:
            market = parts[0]
        else:
            market = 'us'
            
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        # Find start of section
        start_comment = '<!-- Compare Other Hosts Section -->'
        start_idx = content.find(start_comment)
        
        if start_idx != -1:
            # Find the closing </section> after the comment
            end_tag = '</section>'
            end_idx = content.find(end_tag, start_idx)
            if end_idx != -1:
                end_idx += len(end_tag)
                new_section_html = get_interlink_html(market, host)
                new_content = content[:start_idx] + new_section_html + content[end_idx:]
            else:
                print(f"Warning: Could not find closing </section> in {fp}")
                continue
        else:
            # Missing section completely, insert before </main>
            main_close_tag = '</main>'
            main_idx = content.find(main_close_tag)
            if main_idx != -1:
                new_section_html = get_interlink_html(market, host)
                new_content = content[:main_idx] + new_section_html + "\n" + content[main_idx:]
            else:
                print(f"Warning: Could not find </main> in {fp}")
                continue
                
        if new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Interlinked: {os.path.relpath(fp, root_dir)}")
            updated_count += 1
            
    print(f"\nDone! Interlinked {updated_count} comparison files.")

if __name__ == '__main__':
    main()
