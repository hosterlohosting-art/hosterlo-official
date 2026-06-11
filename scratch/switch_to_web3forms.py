#!/usr/bin/env python3
"""
switch_to_web3forms.py
Replaces all formsubmit.co forms with Web3Forms (api.web3forms.com).
Uses AJAX submission so thank-you modal appears in-page instantly (no redirect).
"""

import os
import re
import glob

# ─── CONFIG ───────────────────────────────────────────────────────────────────
WEB3FORMS_KEY = "YOUR_WEB3FORMS_KEY_HERE"   # <-- paste key from web3forms.com
TARGET_EMAIL  = "hosterlohosting@gmail.com"
# ──────────────────────────────────────────────────────────────────────────────

# AJAX submit script (inline, no deps)
AJAX_SCRIPT = '''<script>
(function(){
  // ── Web3Forms AJAX submit for all forms on this page ──
  function showThankyou(){
    var m = document.getElementById('hl-thankyou-modal');
    if(!m){
      // contact-us page modal has different id
      m = document.getElementById('contact-thankyou-modal');
    }
    if(m){ m.classList.remove('hidden'); }
  }

  function bindForm(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var btn = form.querySelector('[type="submit"]');
      var origText = btn ? btn.innerHTML : '';
      if(btn){
        btn.disabled = true;
        btn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:6px"><svg style="animation:spin 1s linear infinite;width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;viewBox:0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke-opacity="0.25"/><path d="M22 12a10 10 0 01-10 10"/></svg>Sending...</span>';
      }
      var data = new FormData(form);
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        body: data
      })
      .then(function(res){ return res.json(); })
      .then(function(json){
        if(json.success){
          form.reset();
          showThankyou();
        } else {
          alert('Something went wrong. Please try again or contact us via WhatsApp.');
        }
      })
      .catch(function(){
        alert('Network error. Please check your connection and try again.');
      })
      .finally(function(){
        if(btn){ btn.disabled = false; btn.innerHTML = origText; }
      });
    });
  }

  // Bind all Web3Forms on page
  document.querySelectorAll('form[data-w3f]').forEach(bindForm);

  // Also check ?sent=1 fallback (shouldn't be needed but just in case)
  if(window.location.search.includes('sent=1')){
    showThankyou();
    history.replaceState({}, document.title, window.location.pathname);
  }
})();
</script>
<style>
@keyframes spin { to { transform: rotate(360deg); } }
</style>'''

# Patterns to fix
FORMSUBMIT_ACTION = re.compile(
    r'action="https://formsubmit\.co/[^"]*"',
    re.IGNORECASE
)
FORMSUBMIT_HIDDEN_FIELDS = re.compile(
    r'\s*<input[^>]+name="_(?:subject|captcha|template|next|honey)"[^>]*>\s*',
    re.IGNORECASE | re.DOTALL
)
HONEYPOT_FIELD = re.compile(
    r'\s*<input[^>]+name="_honey"[^>]*>\s*',
    re.IGNORECASE
)
# Remove the inline script that handled ?sent=1 redirect
SENT_SCRIPT = re.compile(
    r'<script>\s*\(function\(\)\{[^<]*sent=1[^<]*\}\)\(\);\s*</script>',
    re.IGNORECASE | re.DOTALL
)

def patch_file(path, key):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if 'formsubmit.co' not in content and 'web3forms.com' not in content:
        return False  # nothing to do

    original = content

    # 1. Replace action URL
    content = FORMSUBMIT_ACTION.sub(
        'action="https://api.web3forms.com/submit" data-w3f="1"',
        content
    )

    # 2. Replace hidden config fields with web3forms fields
    # We'll do it by finding each form block and rewriting the hidden fields
    def replace_hidden_fields(m):
        return ''  # remove formsubmit-specific fields
    content = FORMSUBMIT_HIDDEN_FIELDS.sub(replace_hidden_fields, content)

    # 3. Remove old sent=1 inline scripts
    content = SENT_SCRIPT.sub('', content)

    # 4. Inject Web3Forms access_key after each form opening tag
    def inject_w3f_fields(m):
        form_tag = m.group(0)
        # Extract _subject value from nearby text if possible (we'll set a generic one)
        return form_tag
    
    # 4. Add access_key hidden input after each <form data-w3f="1" ...>
    def add_access_key(m):
        form_open = m.group(0)
        return form_open + (
            f'\n                    <!-- Web3Forms config -->\n'
            f'                    <input type="hidden" name="access_key" value="{key}">\n'
            f'                    <input type="hidden" name="from_name" value="Hosterlo Website">\n'
            f'                    <input type="hidden" name="botcheck" style="display:none">\n'
        )

    content = re.sub(
        r'(<form[^>]+data-w3f="1"[^>]*>)',
        add_access_key,
        content
    )

    # Also fix old contact-us form if it still has web3forms fields from before
    # but now has web3forms URL — add access key there too
    content = re.sub(
        r'(<form[^>]+action="https://api\.web3forms\.com/submit"(?![^>]*data-w3f)[^>]*>)',
        lambda m: m.group(0).replace(
            'action="https://api.web3forms.com/submit"',
            'action="https://api.web3forms.com/submit" data-w3f="1"'
        ),
        content
    )

    # 5. Inject AJAX script before </body> if not already there
    if 'Web3Forms AJAX submit' not in content:
        content = content.replace('</body>', AJAX_SCRIPT + '\n</body>', 1)

    if content == original:
        return False

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


if __name__ == '__main__':
    import sys
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    key  = WEB3FORMS_KEY

    # Accept key as CLI arg: python switch_to_web3forms.py MYKEY
    if len(sys.argv) > 1:
        key = sys.argv[1].strip()

    if key == 'YOUR_WEB3FORMS_KEY_HERE':
        print('ERROR: Please set WEB3FORMS_KEY in script or pass as argument.')
        print('  1. Go to https://web3forms.com/')
        print('  2. Enter hosterlohosting@gmail.com')
        print('  3. Copy the Access Key from the email')
        print('  4. Run: python scratch/switch_to_web3forms.py YOUR_KEY_HERE')
        sys.exit(1)

    modified = 0
    for html in glob.glob(os.path.join(base, '**', '*.html'), recursive=True):
        rel = os.path.relpath(html, base)
        if '.git' in rel:
            continue
        if patch_file(html, key):
            print(f'  [OK] {rel}')
            modified += 1

    print(f'\nDone! Modified {modified} file(s).')
    print(f'Access Key used: {key[:8]}...')
    print(f'Emails will go to: {TARGET_EMAIL}')
