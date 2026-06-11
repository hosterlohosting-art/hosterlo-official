#!/usr/bin/env python3
"""
fix_forms_ajax.py
Converts all FormSubmit.co forms from full-page-redirect to AJAX fetch.
- Changes action URL to formsubmit.co/ajax/EMAIL
- Removes _next redirect hidden field
- Adds JS to intercept submit, show spinner, show thank-you modal
"""

import os
import re
import glob

EMAIL = "hosterlohosting@gmail.com"
AJAX_URL = f"https://formsubmit.co/ajax/{EMAIL}"

AJAX_HANDLER = '''
<script>
(function(){
  function showModal(){
    var m1 = document.getElementById('hl-thankyou-modal');
    var m2 = document.getElementById('contact-thankyou-modal');
    var m = m1 || m2;
    if(m){ m.classList.remove('hidden'); }
  }

  function handleForm(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var originalHTML = btn ? btn.innerHTML : '';

      // Show spinner
      if(btn){
        btn.disabled = true;
        btn.innerHTML = '<svg style="display:inline-block;animation:hosterlo-spin 0.8s linear infinite;width:20px;height:20px;vertical-align:middle;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10" stroke-opacity="0.3"/><path d="M22 12a10 10 0 01-10 10" stroke-linecap="round"/></svg>Sending...';
      }

      var formData = new FormData(form);

      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: { 'Accept': 'application/json' }
      })
      .then(function(res){ return res.json(); })
      .then(function(data){
        if(btn){ btn.disabled = false; btn.innerHTML = originalHTML; }
        if(data.success === "true" || data.success === true){
          form.reset();
          showModal();
        } else {
          alert('Oops! Something went wrong. Please try WhatsApp or email us directly at hosterlohosting@gmail.com');
        }
      })
      .catch(function(err){
        if(btn){ btn.disabled = false; btn.innerHTML = originalHTML; }
        alert('Network error. Please check your internet connection and try again, or contact us on WhatsApp.');
        console.error('Form error:', err);
      });
    });
  }

  // Bind all forms on page
  document.querySelectorAll('form[data-hl-form]').forEach(handleForm);
})();
</script>
<style>
@keyframes hosterlo-spin { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
</style>
'''

def patch_html(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if f'formsubmit.co/{EMAIL}' not in content and f'formsubmit.co/ajax/{EMAIL}' not in content:
        return False  # nothing to do

    original = content

    # 1. Replace normal action URL with AJAX URL and add data-hl-form marker
    content = content.replace(
        f'action="https://formsubmit.co/{EMAIL}"',
        f'action="{AJAX_URL}" data-hl-form="1"'
    )
    # If already ajax but no marker
    content = content.replace(
        f'action="{AJAX_URL}"',
        f'action="{AJAX_URL}" data-hl-form="1"'
    )
    # Remove duplicate markers
    content = content.replace('data-hl-form="1" data-hl-form="1"', 'data-hl-form="1"')

    # 2. Remove _next redirect field (not needed for AJAX)
    content = re.sub(
        r'\s*<input[^>]+name="_next"[^>]*/?\s*>\s*',
        '\n                    ',
        content
    )

    # 3. Inject AJAX handler script before </body> if not already there
    if 'hosterlo-spin' not in content:
        content = content.replace('</body>', AJAX_HANDLER + '\n</body>', 1)

    if content == original:
        return False

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


if __name__ == '__main__':
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    modified = 0

    for html in glob.glob(os.path.join(base, '**', '*.html'), recursive=True):
        rel = os.path.relpath(html, base)
        if '.git' in rel or 'scratch' in rel:
            continue
        try:
            if patch_html(html):
                print(f'  [OK] {rel}')
                modified += 1
        except Exception as ex:
            print(f'  [ERR] {rel}: {ex}')

    print(f'\nDone! Fixed {modified} file(s).')
    print('Forms now use AJAX - no page reload, instant thank-you modal!')
