#!/usr/bin/env python3
"""
add_cta_forms.py - Injects FormSubmit.co CTA contact sections into service/key pages.
Sends all submissions to hosterlohosting@gmail.com
"""

import os
import re

# ─────────────────────────────────────────────────────────────────────────────
# Helper: detect if a page is a "service" page (needs extended fields)
# ─────────────────────────────────────────────────────────────────────────────
SERVICE_PATHS = [
    'services/web-development',
    'services/saas-development',
    'services/frontend-development',
    'services/backend-development',
    'services/ui-ux-design',
    'services/mobile-app-development',
    'services/api-development',
    'services/website-maintenance',
    'services/index',  # services hub
]

OTHER_KEY_PAGES = [
    'hosting/index',
    'hosting/shared-hosting',
    'hosting/wordpress-hosting',
    'domains/index',
    'pricing/index',
    'about-hosterlo/index',
    'portfolio/index',
    'get-a-quote/index',
]

# Thank-you modal HTML (shared)
THANKYOU_MODAL = '''
    <!-- ======= Thank-You Modal (FormSubmit redirect) ======= -->
    <div id="hl-thankyou-modal" class="hidden fixed inset-0 z-[99999] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" onclick="document.getElementById('hl-thankyou-modal').classList.add('hidden')"></div>
        <div class="relative bg-white rounded-[32px] p-10 md:p-14 max-w-md w-full text-center shadow-2xl z-10">
            <div class="w-20 h-20 bg-emerald-50 rounded-full flex items-center justify-center mx-auto mb-6">
                <span class="material-symbols-outlined text-5xl text-emerald-500">check_circle</span>
            </div>
            <h3 class="text-2xl font-black text-slate-900 mb-3">We Got Your Message! 🎉</h3>
            <p class="text-slate-500 text-sm leading-relaxed mb-6">Thank you for reaching out to Hosterlo! Our team will review your request and contact you within 24 hours. We look forward to working with you.</p>
            <button onclick="document.getElementById('hl-thankyou-modal').classList.add('hidden')" class="px-8 py-3 bg-[#4f17ce] text-white font-bold rounded-full text-sm hover:opacity-90 transition-all">Got it, Thanks!</button>
        </div>
    </div>
    <script>
    (function(){
        if(window.location.search.includes('sent=1')){
            var m = document.getElementById('hl-thankyou-modal');
            if(m){ m.classList.remove('hidden'); }
            history.replaceState({}, document.title, window.location.pathname);
        }
    })();
    </script>
'''

# SERVICE CTA SECTION - comprehensive project inquiry form
def get_service_cta(page_url_hint, service_label):
    return f'''
    <!-- ======= Service CTA Contact Form ======= -->
    <section class="py-24 bg-gradient-to-br from-[#0f0a1e] via-[#1a1145] to-[#2d1b69] relative overflow-hidden" id="get-quote">
        <div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image:radial-gradient(circle at 20% 50%, #7c3aed 0%, transparent 50%), radial-gradient(circle at 80% 20%, #4f46e5 0%, transparent 50%);"></div>
        <div class="max-w-[1100px] mx-auto px-6 relative z-10">
            <div class="grid lg:grid-cols-2 gap-12 items-start">
                <!-- Left: Info -->
                <div class="text-white pt-4" data-aos="fade-right">
                    <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-white/10 text-indigo-300 text-xs font-black uppercase rounded-full mb-6 tracking-widest">FREE CONSULTATION</span>
                    <h2 class="text-3xl md:text-4xl font-black leading-tight mb-6">Ready to Start Your Project?</h2>
                    <p class="text-white/70 text-base leading-relaxed mb-8">Tell us about your idea and we'll provide a detailed project roadmap and flat-rate estimate within 24 hours — completely free.</p>
                    <div class="space-y-4">
                        <div class="flex items-center gap-3 text-white/80 text-sm font-semibold">
                            <span class="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-base text-indigo-300">timer</span></span>
                            Response within 24 hours
                        </div>
                        <div class="flex items-center gap-3 text-white/80 text-sm font-semibold">
                            <span class="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-base text-indigo-300">verified</span></span>
                            Free project estimate &amp; roadmap
                        </div>
                        <div class="flex items-center gap-3 text-white/80 text-sm font-semibold">
                            <span class="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-base text-indigo-300">lock</span></span>
                            100% confidential — no obligation
                        </div>
                        <div class="flex items-center gap-3 text-white/80 text-sm font-semibold">
                            <span class="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-base text-indigo-300">support_agent</span></span>
                            Direct WhatsApp support available
                        </div>
                    </div>
                    <div class="mt-10 pt-8 border-t border-white/10">
                        <p class="text-white/50 text-xs mb-4">Prefer instant chat?</p>
                        <a href="https://wa.me/923394437730" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-6 py-3 bg-[#25D366] text-white font-bold rounded-full text-sm hover:opacity-90 transition-all shadow-lg">
                            <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.246 2.248 3.484 5.237 3.483 8.42-.003 6.557-5.338 11.892-11.893 11.892-1.997-.001-3.951-.5-5.688-1.448l-6.308 1.648zm6.757-4.041c1.574.933 3.109 1.423 4.919 1.424 5.456 0 9.897-4.437 9.9-9.899 0-2.646-1.03-5.132-2.903-7.003-1.871-1.871-4.358-2.901-7.001-2.902-5.463 0-9.897 4.437-9.9 9.902-.001 1.933.535 3.551 1.558 5.178l-.999 3.644 3.742-.979zm11.287-5.125c-.3-.15-1.771-.874-2.046-.975-.276-.101-.476-.15-.676.15-.199.3-.776.975-.951 1.176-.175.199-.349.225-.649.075-.3-.15-1.266-.467-2.411-1.487-.893-.797-1.495-1.782-1.67-2.083-.175-.3-.019-.462.13-.611.135-.134.3-.349.449-.525.151-.176.199-.3.3-.499.1-.199.05-.375-.025-.525-.075-.15-.676-1.631-.926-2.231-.242-.583-.491-.504-.676-.513-.174-.009-.375-.011-.575-.011-.2 0-.525.075-.8.375-.276.3-1.051 1.026-1.051 2.502 0 1.475 1.074 2.901 1.224 3.102.15.199 2.115 3.227 5.123 4.525.714.308 1.272.492 1.707.631.717.227 1.369.195 1.884.118.574-.085 1.771-.724 2.021-1.424.25-.699.25-1.299.175-1.424-.075-.125-.275-.199-.575-.349z"/></svg>
                            Chat on WhatsApp
                        </a>
                    </div>
                </div>
                <!-- Right: Form -->
                <div class="bg-white rounded-[32px] p-8 md:p-10 shadow-2xl" data-aos="fade-left">
                    <h3 class="text-xl font-black text-slate-900 mb-2">Tell Us About Your Project</h3>
                    <p class="text-slate-500 text-sm mb-6">Fill out the form below and our team will reach out with a tailored proposal.</p>
                    <form action="https://formsubmit.co/hosterlohosting@gmail.com" method="POST" class="space-y-4">
                        <!-- FormSubmit.co config -->
                        <input type="hidden" name="_subject" value="🚀 New Project Inquiry — {service_label} | Hosterlo">
                        <input type="hidden" name="_captcha" value="false">
                        <input type="hidden" name="_template" value="table">
                        <input type="hidden" name="_next" value="https://hosterlo.com{page_url_hint}?sent=1">
                        <input type="text" name="_honey" style="display:none">

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="space-y-1">
                                <label class="text-xs font-bold text-slate-700">Your Full Name *</label>
                                <input type="text" name="Full Name" placeholder="e.g. John Smith" required class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all">
                            </div>
                            <div class="space-y-1">
                                <label class="text-xs font-bold text-slate-700">Your Email *</label>
                                <input type="email" name="Email" placeholder="john@example.com" required class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all">
                            </div>
                        </div>

                        <div class="space-y-1">
                            <label class="text-xs font-bold text-slate-700">Phone / WhatsApp</label>
                            <input type="tel" name="Phone" placeholder="+1 (555) 000-0000" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all">
                        </div>

                        <div class="space-y-1">
                            <label class="text-xs font-bold text-slate-700">Service You Need *</label>
                            <select name="Service Required" required class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all">
                                <option value="">— Select a Service —</option>
                                <option value="Web Development">Web Development</option>
                                <option value="SaaS Product Development">SaaS Product Development</option>
                                <option value="Frontend Engineering">Frontend Engineering</option>
                                <option value="Backend Engineering">Backend Engineering</option>
                                <option value="UI/UX Design">UI/UX Design</option>
                                <option value="Mobile App Development">Mobile App Development</option>
                                <option value="API Integration">API Integration</option>
                                <option value="Website Maintenance">Website Maintenance</option>
                                <option value="Web Hosting">Web Hosting</option>
                                <option value="Domain Registration">Domain Registration</option>
                                <option value="Other / Not Sure">Other / Not Sure</option>
                            </select>
                        </div>

                        <div class="space-y-1">
                            <label class="text-xs font-bold text-slate-700">Website Name / URL (if you have one)</label>
                            <input type="text" name="Website URL" placeholder="e.g. myawesomebusiness.com" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all">
                        </div>

                        <div class="space-y-1">
                            <label class="text-xs font-bold text-slate-700">Estimated Budget *</label>
                            <select name="Budget" required class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all">
                                <option value="">— Select Your Budget —</option>
                                <option value="Under $500">Under $500</option>
                                <option value="$500 – $1,500">$500 – $1,500</option>
                                <option value="$1,500 – $5,000">$1,500 – $5,000</option>
                                <option value="$5,000 – $15,000">$5,000 – $15,000</option>
                                <option value="$15,000 – $50,000">$15,000 – $50,000</option>
                                <option value="$50,000+">$50,000+</option>
                                <option value="Not sure yet">Not sure yet</option>
                            </select>
                        </div>

                        <div class="space-y-1">
                            <label class="text-xs font-bold text-slate-700">Project Description *</label>
                            <textarea name="Project Description" rows="4" placeholder="Briefly describe what you need. Include any key features, deadline, or special requirements..." required class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all resize-none"></textarea>
                        </div>

                        <button type="submit" class="w-full py-4 bg-[#4f17ce] text-white font-extrabold rounded-xl shadow-lg shadow-[#4f17ce]/25 hover:bg-[#673de6] active:scale-95 transition-all text-sm flex items-center justify-center gap-2">
                            <span class="material-symbols-outlined text-[18px]">send</span>
                            Send My Project Details
                        </button>
                        <p class="text-center text-[10px] text-slate-400 font-semibold">We'll respond within 24 hours · No spam · 100% confidential</p>
                    </form>
                </div>
            </div>
        </div>
    </section>
'''

# SIMPLE CTA SECTION - for hosting/domain/other pages (shorter form)
def get_simple_cta(page_url_hint, page_label):
    return f'''
    <!-- ======= CTA Contact Section ======= -->
    <section class="py-20 bg-slate-50 border-t border-slate-100" id="get-in-touch">
        <div class="max-w-[900px] mx-auto px-6">
            <div class="bg-white rounded-[36px] border border-slate-100 shadow-xl p-8 md:p-14">
                <div class="text-center mb-10" data-aos="fade-up">
                    <span class="inline-flex items-center gap-1.5 px-4 py-1.5 bg-[#4f17ce]/5 text-[#4f17ce] text-xs font-black uppercase rounded-full mb-4 tracking-widest">GET IN TOUCH</span>
                    <h2 class="text-2xl md:text-3xl font-black text-slate-900 mb-3">Have a Question? We're Here.</h2>
                    <p class="text-slate-500 text-sm max-w-lg mx-auto">Fill in the form below and our team will get back to you quickly. For urgent help, use WhatsApp — we typically respond in minutes.</p>
                </div>
                <form action="https://formsubmit.co/hosterlohosting@gmail.com" method="POST" class="space-y-4 max-w-2xl mx-auto" data-aos="fade-up">
                    <input type="hidden" name="_subject" value="📩 New Inquiry — {page_label} | Hosterlo">
                    <input type="hidden" name="_captcha" value="false">
                    <input type="hidden" name="_template" value="table">
                    <input type="hidden" name="_next" value="https://hosterlo.com{page_url_hint}?sent=1">
                    <input type="text" name="_honey" style="display:none">

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div class="space-y-1">
                            <label class="text-xs font-bold text-slate-700">Full Name *</label>
                            <input type="text" name="Full Name" placeholder="Your name" required class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/20 focus:bg-white outline-none text-sm transition-all">
                        </div>
                        <div class="space-y-1">
                            <label class="text-xs font-bold text-slate-700">Email Address *</label>
                            <input type="email" name="Email" placeholder="you@example.com" required class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/20 focus:bg-white outline-none text-sm transition-all">
                        </div>
                    </div>
                    <div class="space-y-1">
                        <label class="text-xs font-bold text-slate-700">What do you need help with?</label>
                        <select name="Inquiry Type" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/20 focus:bg-white outline-none text-sm transition-all">
                            <option>General Question</option>
                            <option>Sales &amp; Pricing</option>
                            <option>Technical Support</option>
                            <option>Billing / Account</option>
                            <option>Migration Help</option>
                        </select>
                    </div>
                    <div class="space-y-1">
                        <label class="text-xs font-bold text-slate-700">Message *</label>
                        <textarea name="Message" rows="4" placeholder="Tell us what you need..." required class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/20 focus:bg-white outline-none text-sm transition-all resize-none"></textarea>
                    </div>
                    <div class="flex flex-col sm:flex-row gap-4 items-center">
                        <button type="submit" class="w-full sm:w-auto px-10 py-3.5 bg-[#4f17ce] text-white font-extrabold rounded-full shadow-md hover:bg-[#673de6] active:scale-95 transition-all text-sm flex items-center justify-center gap-2">
                            <span class="material-symbols-outlined text-[18px]">send</span>
                            Send Message
                        </button>
                        <a href="https://wa.me/923394437730" target="_blank" rel="noopener noreferrer" class="w-full sm:w-auto px-8 py-3.5 bg-[#25D366] text-white font-bold rounded-full text-sm text-center hover:opacity-90 transition-all flex items-center justify-center gap-2">
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.246 2.248 3.484 5.237 3.483 8.42-.003 6.557-5.338 11.892-11.893 11.892-1.997-.001-3.951-.5-5.688-1.448l-6.308 1.648zm6.757-4.041c1.574.933 3.109 1.423 4.919 1.424 5.456 0 9.897-4.437 9.9-9.899 0-2.646-1.03-5.132-2.903-7.003-1.871-1.871-4.358-2.901-7.001-2.902-5.463 0-9.897 4.437-9.9 9.902-.001 1.933.535 3.551 1.558 5.178l-.999 3.644 3.742-.979zm11.287-5.125c-.3-.15-1.771-.874-2.046-.975-.276-.101-.476-.15-.676.15-.199.3-.776.975-.951 1.176-.175.199-.349.225-.649.075-.3-.15-1.266-.467-2.411-1.487-.893-.797-1.495-1.782-1.67-2.083-.175-.3-.019-.462.13-.611.135-.134.3-.349.449-.525.151-.176.199-.3.3-.499.1-.199.05-.375-.025-.525-.075-.15-.676-1.631-.926-2.231-.242-.583-.491-.504-.676-.513-.174-.009-.375-.011-.575-.011-.2 0-.525.075-.8.375-.276.3-1.051 1.026-1.051 2.502 0 1.475 1.074 2.901 1.224 3.102.15.199 2.115 3.227 5.123 4.525.714.308 1.272.492 1.707.631.717.227 1.369.195 1.884.118.574-.085 1.771-.724 2.021-1.424.25-.699.25-1.299.175-1.424-.075-.125-.275-.199-.575-.349z"/></svg>
                            WhatsApp
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </section>
'''

# ─────────────────────────────────────────────────────────────────────────────
# Page map: relative html path → (url_hint, label, form_type)
# ─────────────────────────────────────────────────────────────────────────────
PAGES = {
    # Service pages - detailed form
    'services/web-development/index.html':      ('/services/web-development/', 'Web Development', 'service'),
    'services/saas-development/index.html':     ('/services/saas-development/', 'SaaS Development', 'service'),
    'services/frontend-development/index.html': ('/services/frontend-development/', 'Frontend Development', 'service'),
    'services/backend-development/index.html':  ('/services/backend-development/', 'Backend Development', 'service'),
    'services/ui-ux-design/index.html':         ('/services/ui-ux-design/', 'UI/UX Design', 'service'),
    'services/mobile-app-development/index.html': ('/services/mobile-app-development/', 'Mobile App Development', 'service'),
    'services/api-development/index.html':      ('/services/api-development/', 'API Development', 'service'),
    'services/website-maintenance/index.html':  ('/services/website-maintenance/', 'Website Maintenance', 'service'),
    'services/index.html':                      ('/services/', 'Services Hub', 'service'),
    # Other key pages - simple form
    'hosting/index.html':                       ('/hosting/', 'Cloud Hosting', 'simple'),
    'hosting/shared-hosting/index.html':        ('/hosting/shared-hosting/', 'Shared Hosting', 'simple'),
    'hosting/wordpress-hosting/index.html':     ('/hosting/wordpress-hosting/', 'WordPress Hosting', 'simple'),
    'domains/index.html':                       ('/domains/', 'Domains', 'simple'),
    'pricing/index.html':                       ('/pricing/', 'Pricing', 'simple'),
    'about-hosterlo/index.html':                ('/about-hosterlo/', 'About Hosterlo', 'simple'),
    'portfolio/index.html':                     ('/portfolio/', 'Portfolio', 'simple'),
    'get-a-quote/index.html':                   ('/get-a-quote/', 'Get a Quote', 'service'),
}

def already_has_form(content):
    """Check if page already has a formsubmit.co form injected."""
    return 'formsubmit.co/hosterlohosting@gmail.com' in content or 'hl-thankyou-modal' in content

def inject_before_footer(content, injection):
    """Insert content just before the </main> or <footer tag."""
    # Try before </main>
    idx = content.rfind('</main>')
    if idx != -1:
        return content[:idx] + injection + content[idx:]
    # Fallback: before <footer
    idx = content.rfind('<footer')
    if idx != -1:
        return content[:idx] + injection + content[idx:]
    # Last resort: before </body>
    idx = content.rfind('</body>')
    if idx != -1:
        return content[:idx] + injection + content[idx:]
    return content

base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(base_dir)  # parent of scratch/

modified = 0
skipped = 0
errors = []

for rel_path, (url_hint, label, form_type) in PAGES.items():
    full_path = os.path.join(project_dir, rel_path.replace('/', os.sep))
    if not os.path.exists(full_path):
        print(f'  [SKIP] File not found: {rel_path}')
        skipped += 1
        continue
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if already_has_form(content):
        print(f'  [SKIP] Already has FormSubmit: {rel_path}')
        skipped += 1
        continue
    
    # Build the injection
    if form_type == 'service':
        cta_html = get_service_cta(url_hint, label)
    else:
        cta_html = get_simple_cta(url_hint, label)
    
    # Add the thank-you modal + CTA section before footer/</main>
    injection = THANKYOU_MODAL + cta_html
    
    new_content = inject_before_footer(content, injection)
    
    if new_content == content:
        print(f'  [WARN] Could not find injection point in: {rel_path}')
        errors.append(rel_path)
        continue
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'  [OK]   Injected {form_type} CTA into: {rel_path}')
    modified += 1

print(f'\n✅ Done! Modified: {modified} | Skipped: {skipped} | Errors: {len(errors)}')
if errors:
    print('⚠️  Could not inject into:')
    for e in errors:
        print(f'   - {e}')
