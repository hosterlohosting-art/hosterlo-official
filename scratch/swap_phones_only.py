import os
import re

base_dir = r"d:\Hosterlo Official Site"

def read_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def swap_phones_and_whatsapp_in_file(path, is_pk, is_uk):
    content = read_file(path)
    changed = False
    
    if is_pk:
        # PK pages keep PK coordinates:
        # WhatsApp: 923394437730
        # Phone: +92 3394437730
        pass
    else:
        # For default/US and UK pages:
        # 1) WhatsApp must be US: wa.me/16183561311
        # 2) Phone must be UK: +44 7575 803760 (tel:+447575803760)
        
        # Replace WhatsApp links
        if "wa.me/923394437730" in content:
            content = content.replace("wa.me/923394437730", "wa.me/16183561311")
            changed = True
            
        # Replace WhatsApp tooltip or display labels
        if "+92 3394437730" in content:
            content = content.replace("+92 3394437730", "+1 (618) 356-1311")
            changed = True
        if "+923394437730" in content:
            content = content.replace("+923394437730", "+1 (618) 356-1311")
            changed = True
            
        # Replace Phone links/tooltips/displays
        for tel_val in ["+16183561311", "+13022039118"]:
            if f"tel:{tel_val}" in content:
                content = content.replace(f"tel:{tel_val}", "tel:+447575803760")
                changed = True
                
        for phone_disp in ["+1 (618) 356-1311", "+1 (302) 203-9118"]:
            content = content.replace(f"Call: {phone_disp}", "Call: +44 7575 803760")
            content = content.replace(f"Call: {phone_disp.replace(' ', '')}", "Call: +44 7575 803760")
            
            # If it is in contact-us page phone section next to a call icon, let's replace it
            call_icon_pattern = re.compile(rf'material-symbols-outlined[^>]*>call</span>\s*<span>{re.escape(phone_disp)}</span>', re.IGNORECASE)
            if call_icon_pattern.search(content):
                content = call_icon_pattern.sub('material-symbols-outlined text-primary text-xl">call</span><span>+44 7575 803760</span>', content)
                changed = True
                
            # Replace telephone in schemas for organization support telephone
            schema_phone_pattern = re.compile(rf'"telephone"\s*:\s*"{re.escape(phone_disp)}"', re.IGNORECASE)
            if schema_phone_pattern.search(content):
                content = schema_phone_pattern.sub('"telephone": "+44 7575 803760"', content)
                changed = True

    if changed:
        write_file(path, content)
        print(f"Swapped phone/WhatsApp in: {path}")

def main():
    for root, dirs, files in os.walk(base_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_dir)
                norm_rel = rel_path.replace("\\", "/").lower()
                
                is_pk = "pk/" in norm_rel or norm_rel.startswith("pk/")
                is_uk = "uk/" in norm_rel or norm_rel.startswith("uk/")
                
                swap_phones_and_whatsapp_in_file(file_path, is_pk, is_uk)
                
    print("Phone/WhatsApp swapping completed!")

if __name__ == "__main__":
    main()
