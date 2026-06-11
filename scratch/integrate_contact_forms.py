import os
import re

contact_files = [
    r"contact-us\index.html",
    r"uk\contact-us\index.html",
    r"pk\contact-us\index.html"
]

form_regex = re.compile(
    r'<form action="https://api\.web3forms\.com/submit" method="POST" class="space-y-6">.*?</form>',
    re.DOTALL
)

new_form_content = """<form id="contact-form" onsubmit="handleContactSubmit(event)" class="space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="space-y-1">
                            <label class="text-xs font-bold text-slate-700 ml-1">Full Name</label>
                            <input type="text" name="name" placeholder="John Doe" required class="w-full px-5 py-3.5 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-primary/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all">
                        </div>
                        <div class="space-y-1">
                            <label class="text-xs font-bold text-slate-700 ml-1">Business Email</label>
                            <input type="email" name="email" placeholder="john@example.com" required class="w-full px-5 py-3.5 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-primary/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all">
                        </div>
                    </div>
                    
                    <div class="space-y-1">
                        <label class="text-xs font-bold text-slate-700 ml-1">Inquiry Department</label>
                        <select name="department" class="w-full px-5 py-3.5 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-primary/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all">
                            <option>Sales Inquiry</option>
                            <option>Technical Support</option>
                            <option>Billing Question</option>
                            <option>Partnership</option>
                        </select>
                    </div>
                    
                    <div class="space-y-1">
                        <label class="text-xs font-bold text-slate-700 ml-1">Your Message</label>
                        <textarea name="message" rows="4" placeholder="How can our hosting team help you?" required class="w-full px-5 py-3.5 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-primary/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all resize-none"></textarea>
                    </div>
                    
                    <button type="submit" class="button-shine block w-full py-4 bg-primary text-white font-extrabold rounded-xl shadow-lg shadow-primary/25 active:scale-95 transition-all text-sm">Submit Form</button>
                </form>
                
                <!-- Success State Dialog -->
                <div id="contact-success-state" class="hidden text-center py-10 space-y-5 animate-in">
                    <div class="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto shadow-inner">
                        <span class="material-symbols-outlined text-3xl">task_alt</span>
                    </div>
                    <h3 class="text-2xl font-black text-slate-900">Message Sent!</h3>
                    <p class="text-slate-500 text-sm max-w-sm mx-auto">Thank you! We have received your message and will contact you shortly.</p>
                </div>"""

script_function = """        async function handleContactSubmit(event) {
            event.preventDefault();
            const form = event.target;
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;

            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <span class="inline-flex items-center gap-2 justify-center w-full">
                    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Sending Message...
                </span>
            `;

            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });

            try {
                const response = await fetch("https://formsubmit.co/ajax/hosterlohosting@gmail.com", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    form.classList.add('hidden');
                    document.getElementById('contact-success-state').classList.remove('hidden');
                } else {
                    throw new Error("Submission failed");
                }
            } catch (error) {
                alert("Oops! There was a problem sending your message. Please try again or contact us via WhatsApp.");
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        }
    </script>"""

count = 0
for rel_path in contact_files:
    if os.path.exists(rel_path):
        with open(rel_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace the form
        new_content, n_form = form_regex.subn(new_form_content, content)
        
        # Injects script right before </script> at the end
        if n_form > 0 and 'handleContactSubmit' not in new_content:
            new_content = new_content.replace('</script>', script_function)
            with open(rel_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated contact form in: {rel_path}")
            count += 1
    else:
        print(f"File not found: {rel_path}")

print(f"Successfully updated {count} contact pages.")
