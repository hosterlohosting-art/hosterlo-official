import os

def fix_comparison_table(fp, old_vals, new_vals):
    if not os.path.exists(fp):
        return
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        
    original = content
    for old, new in zip(old_vals, new_vals):
        content = content.replace(old, new)
        
    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed comparison table pricing in: {fp}")

def main():
    root_dir = r"d:\Hosterlo Official Site"
    
    # UK Homepage Fixes
    fix_comparison_table(
        os.path.join(root_dir, 'uk', 'index.html'),
        ['£3.25/mo.00 / year', '£3.25/mo.00 / year (Flat)'],
        ['£3.25 / month', '£3.25 / month (Flat)']
    )
    
    # PH Homepage Fixes
    fix_comparison_table(
        os.path.join(root_dir, 'ph', 'index.html'),
        ['₱239/mo.00 / year', '₱239/mo.00 / year (Flat)'],
        ['₱239 / month', '₱239 / month (Flat)']
    )
    
    # Let's check PK homepage
    fix_comparison_table(
        os.path.join(root_dir, 'pk', 'index.html'),
        ['Rs. 1,150/mo.00 / year', 'Rs. 1,150/mo.00 / year (Flat)'],
        ['Rs. 1,150 / month', 'Rs. 1,150 / month (Flat)']
    )
    
    # Let's check ES homepage
    fix_comparison_table(
        os.path.join(root_dir, 'es', 'index.html'),
        ['$4.08/mo.00 / year', '$4.08/mo.00 / year (Flat)'],
        ['$4.08 / mes', '$4.08 / mes (Tarifa plana)']
    )

if __name__ == '__main__':
    main()
