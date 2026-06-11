#!/usr/bin/env python3
"""Replace alert() error with friendly inline error box in all forms."""
import os, glob

OLD = "alert('Oops! Something went wrong. Please try WhatsApp or email us directly at hosterlohosting@gmail.com');"

NEW = """// Show inline error
var errBox = form.querySelector('.hl-form-error');
if(!errBox){
  errBox = document.createElement('p');
  errBox.className = 'hl-form-error';
  errBox.style.cssText = 'background:#fff1f2;border:1px solid #fecaca;color:#b91c1c;padding:10px 14px;border-radius:10px;font-size:12px;font-weight:700;margin-top:10px;';
  errBox.innerHTML = '&#9888; Message failed to send. Please contact us via <a href="https://wa.me/923394437730" style="color:#4f17ce;text-decoration:underline">WhatsApp</a> or email hosterlohosting@gmail.com directly.';
  form.appendChild(errBox);
} else { errBox.style.display='block'; }"""

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
count = 0
for html in glob.glob(os.path.join(base, '**', '*.html'), recursive=True):
    if '.git' in html:
        continue
    with open(html, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if OLD in content:
        with open(html, 'w', encoding='utf-8') as f:
            f.write(content.replace(OLD, NEW))
        count += 1
        print(f'Fixed: {os.path.relpath(html, base)}')

print(f'Done: {count} files updated')
