import os

ROOT = "d:\\Hosterlo Official Site"

# 1. Fix incorrect Pakistani WhatsApp number in es/ folder
es_dir = os.path.join(ROOT, "es")
for root, dirs, files in os.walk(es_dir):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if "923394437730" in content:
                content = content.replace("923394437730", "16183561311")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed WA number in: {filepath}")

# 2. Inject captcha logic into AJAX forms
old_js = "  function handleForm(form){\n    form.addEventListener('submit', function(e){\n      e.preventDefault();"
new_js = """  function handleForm(form){
    var n1 = Math.floor(Math.random() * 9) + 1;
    var n2 = Math.floor(Math.random() * 9) + 1;
    var isEs = document.documentElement.lang === 'es' || window.location.pathname.includes('/es/');
    var capDiv = document.createElement('div');
    capDiv.className = 'space-y-1 mt-4';
    capDiv.innerHTML = '<label class="text-xs font-bold text-slate-700 ml-1">' + (isEs ? 'Seguridad: ¿Cuánto es ' + n1 + ' + ' + n2 + '?' : 'Security: What is ' + n1 + ' + ' + n2 + '?') + '</label><input type="number" required class="w-full px-5 py-3.5 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-primary/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all hl-captcha-input" placeholder="' + (isEs ? 'Tu respuesta' : 'Your answer') + '">';
    var submitBtn = form.querySelector('button[type="submit"]');
    if(submitBtn) form.insertBefore(capDiv, submitBtn);
    else form.appendChild(capDiv);

    form.addEventListener('submit', function(e){
      var capInput = form.querySelector('.hl-captcha-input');
      if(capInput && parseInt(capInput.value, 10) !== (n1 + n2)){
        e.preventDefault();
        alert(isEs ? 'Respuesta de seguridad incorrecta. Por favor, inténtelo de nuevo.' : 'Incorrect security answer. Please try again.');
        capInput.focus();
        return;
      }
      e.preventDefault();"""

for root, dirs, files in os.walk(ROOT):
    for skip in ['.git', 'node_modules', '.agents', '.gemini', 'scratch']:
        if skip in dirs:
            dirs.remove(skip)
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if old_js in content:
                content = content.replace(old_js, new_js)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added captcha to AJAX form in: {filepath}")

# 3. Quote forms captcha injection
quote_files = ["get-a-quote\\index.html", "es\\get-a-quote\\index.html"]
q_inj = """    var n1 = Math.floor(Math.random() * 9) + 1;
    var n2 = Math.floor(Math.random() * 9) + 1;
    var isEs = document.documentElement.lang === 'es' || window.location.pathname.includes('/es/');
    
    document.addEventListener("DOMContentLoaded", function() {
        var form = document.getElementById('quote-request-form');
        if (form) {
            var capDiv = document.createElement('div');
            capDiv.className = 'space-y-1 mt-4';
            capDiv.innerHTML = '<label class="text-xs font-bold text-slate-700">' + (isEs ? 'Seguridad: ¿Cuánto es ' + n1 + ' + ' + n2 + '?' : 'Security: What is ' + n1 + ' + ' + n2 + '?') + '</label><input type="number" id="quote-captcha" required class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-[#4f17ce]/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all" placeholder="' + (isEs ? 'Tu respuesta' : 'Your answer') + '">';
            var submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) form.insertBefore(capDiv, submitBtn);
            else form.appendChild(capDiv);
        }
    });

    async function handleQuoteSubmit(event) {"""

q_val = """        event.preventDefault();
        var capVal = document.getElementById('quote-captcha') ? document.getElementById('quote-captcha').value : '';
        if (parseInt(capVal, 10) !== (n1 + n2)) {
            alert(isEs ? 'Respuesta de seguridad incorrecta. Por favor, inténtelo de nuevo.' : 'Incorrect security answer. Please try again.');
            var capInput = document.getElementById('quote-captcha');
            if (capInput) capInput.focus();
            return;
        }

        const form = document.getElementById('quote-request-form');"""

for rel in quote_files:
    filepath = os.path.join(ROOT, rel)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if "async function handleQuoteSubmit(event) {" in content and "quote-captcha" not in content:
            content = content.replace("async function handleQuoteSubmit(event) {", q_inj)
            content = content.replace("event.preventDefault();\n            const form = document.getElementById('quote-request-form');", q_val)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added captcha to quote form: {rel}")

# 4. PK contact page captcha
pk_path = os.path.join(ROOT, "pk\\contact-us\\index.html")
if os.path.exists(pk_path):
    with open(pk_path, 'r', encoding='utf-8') as f:
        content = f.read()
    pk_script = """    <script>
        var n1 = Math.floor(Math.random() * 9) + 1;
        var n2 = Math.floor(Math.random() * 9) + 1;
        document.addEventListener("DOMContentLoaded", function() {
            var form = document.querySelector('form[action="https://api.web3forms.com/submit"]');
            if (form) {
                var capDiv = document.createElement('div');
                capDiv.className = 'space-y-1 mt-4';
                capDiv.innerHTML = '<label class="text-xs font-bold text-slate-700 ml-1">Security: What is ' + n1 + ' + ' + n2 + '?</label><input type="number" id="pk-contact-captcha" required class="w-full px-5 py-3.5 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-primary/25 focus:border-transparent focus:bg-white outline-none text-sm transition-all" placeholder="Your answer">';
                var submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) form.insertBefore(capDiv, submitBtn);
                else form.appendChild(capDiv);
                
                form.addEventListener('submit', function(e) {
                    var capVal = document.getElementById('pk-contact-captcha') ? document.getElementById('pk-contact-captcha').value : '';
                    if (parseInt(capVal, 10) !== (n1 + n2)) {
                        e.preventDefault();
                        alert('Incorrect security answer. Please try again.');
                        var capInput = document.getElementById('pk-contact-captcha');
                        if (capInput) capInput.focus();
                    }
                });
            }
        });
    </script>
    <script src="https://unpkg.com/aos@next/dist/aos.js"></script>"""
    if "pk-contact-captcha" not in content and '<script src="https://unpkg.com/aos@next/dist/aos.js"></script>' in content:
        content = content.replace('<script src="https://unpkg.com/aos@next/dist/aos.js"></script>', pk_script)
        with open(pk_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Added captcha to PK contact page.")
