import os

competitors = ['bluehost', 'godaddy', 'hostinger', 'siteground']

other_hosts_us_template = """        <!-- Compare Other Hosts Section -->
        <section class="py-16 bg-slate-50 border-t border-slate-100">
            <div class="max-w-[1440px] mx-auto px-6">
                <div class="text-center mb-10">
                    <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-primary/5 text-primary text-xs font-black uppercase rounded-full mb-4">MORE COMPARISONS</span>
                    <h2 class="text-2xl font-black text-[#111c2d]">Compare Hosterlo With Other Hosts</h2>
                    <p class="text-slate-500 text-sm mt-2">See how Hosterlo stacks up against the biggest names in web hosting.</p>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <a href="/{region}compare/hosterlo-vs-bluehost/" class="bg-white border border-slate-200 rounded-2xl p-5 text-center hover:border-primary/30 hover:shadow-md transition-all group">
                        <div class="text-xs font-black text-slate-500 uppercase tracking-wider mb-1 group-hover:text-primary">Compare</div>
                        <div class="font-extrabold text-sm text-[#111c2d]">vs Bluehost</div>
                    </a>
                    <a href="/{region}compare/hosterlo-vs-hostinger/" class="bg-white border border-slate-200 rounded-2xl p-5 text-center hover:border-primary/30 hover:shadow-md transition-all group">
                        <div class="text-xs font-black text-slate-500 uppercase tracking-wider mb-1 group-hover:text-primary">Compare</div>
                        <div class="font-extrabold text-sm text-[#111c2d]">vs Hostinger</div>
                    </a>
                    <a href="/{region}compare/hosterlo-vs-siteground/" class="bg-white border border-slate-200 rounded-2xl p-5 text-center hover:border-primary/30 hover:shadow-md transition-all group">
                        <div class="text-xs font-black text-slate-500 uppercase tracking-wider mb-1 group-hover:text-primary">Compare</div>
                        <div class="font-extrabold text-sm text-[#111c2d]">vs SiteGround</div>
                    </a>
                    <a href="/{region}compare/hosterlo-vs-godaddy/" class="bg-white border border-slate-200 rounded-2xl p-5 text-center hover:border-primary/30 hover:shadow-md transition-all group">
                        <div class="text-xs font-black text-slate-500 uppercase tracking-wider mb-1 group-hover:text-primary">Compare</div>
                        <div class="font-extrabold text-sm text-[#111c2d]">vs GoDaddy</div>
                    </a>
                </div>
            </div>
        </section>"""

def inject_section(file_path, region):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} - not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "Compare Other Hosts Section" in content:
        print(f"Section already exists in {file_path}")
        return

    # Render section for region
    region_prefix = f"{region}/" if region else ""
    section_to_inject = other_hosts_us_template.replace("{region}", region_prefix)

    # We want to inject it right before <!-- Final CTA Section -->
    target_str = "<!-- Final CTA Section -->"
    if target_str in content:
        updated_content = content.replace(target_str, section_to_inject + "\n\n        " + target_str)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Injected Compare Other Hosts section in {file_path}")
    else:
        print(f"Could not find target marker in {file_path}")

def main():
    for comp in competitors:
        # UK Page
        uk_page = f"uk/compare/hosterlo-vs-{comp}/index.html"
        inject_section(uk_page, "uk")

        # PK Page
        pk_page = f"pk/compare/hosterlo-vs-{comp}/index.html"
        inject_section(pk_page, "pk")

if __name__ == '__main__':
    main()
