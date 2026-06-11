import os
import re

competitors = ['bluehost', 'godaddy', 'hostinger', 'siteground']

def get_ld_json(content):
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if match:
        return match.group(0)
    return None

def update_page_schema(source_path, target_path, region):
    if not os.path.exists(source_path) or not os.path.exists(target_path):
        print(f"Skipping {source_path} or {target_path} - file not found.")
        return

    with open(source_path, 'r', encoding='utf-8') as f:
        source_content = f.read()

    source_schema = get_ld_json(source_content)
    if not source_schema:
        print(f"Could not find JSON-LD in {source_path}")
        return

    # Adapt schema
    schema = source_schema
    if region == 'uk':
        # Replace price & currency
        schema = schema.replace('"price": "59.00"', '"price": "47.00"')
        schema = schema.replace('"priceCurrency": "USD"', '"priceCurrency": "GBP"')
        schema = schema.replace('$59/year', '£47/year')
        # Replace compare path links but keep organization global
        schema = schema.replace('https://hosterlo.com/compare/', 'https://hosterlo.com/uk/compare/')
        # Change BreadcrumbList items
        schema = schema.replace('{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://hosterlo.com/"}',
                                '{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://hosterlo.com/uk/"}')
        schema = schema.replace('{"@type": "ListItem", "position": 2, "name": "Compare", "item": "https://hosterlo.com/compare/"}',
                                '{"@type": "ListItem", "position": 2, "name": "Compare", "item": "https://hosterlo.com/uk/compare/"}')
        schema = schema.replace('"item": "https://hosterlo.com/compare/', '"item": "https://hosterlo.com/uk/compare/')
        # Change FAQ answer texts if needed
        schema = schema.replace('$59/year', '£47/year')
        schema = schema.replace('~$131.88/year', '~£110/year') # rough estimate or keep it
    elif region == 'pk':
        schema = schema.replace('"price": "59.00"', '"price": "16500"')
        schema = schema.replace('"priceCurrency": "USD"', '"priceCurrency": "PKR"')
        schema = schema.replace('$59/year', 'Rs. 16,500/year')
        schema = schema.replace('https://hosterlo.com/compare/', 'https://hosterlo.com/pk/compare/')
        schema = schema.replace('{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://hosterlo.com/"}',
                                '{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://hosterlo.com/pk/"}')
        schema = schema.replace('{"@type": "ListItem", "position": 2, "name": "Compare", "item": "https://hosterlo.com/compare/"}',
                                '{"@type": "ListItem", "position": 2, "name": "Compare", "item": "https://hosterlo.com/pk/compare/"}')
        schema = schema.replace('"item": "https://hosterlo.com/compare/', '"item": "https://hosterlo.com/pk/compare/')
        schema = schema.replace('$59/year', 'Rs. 16,500/year')
        schema = schema.replace('~$131.88/year', '~Rs. 36,000/year')

    # Read target content
    with open(target_path, 'r', encoding='utf-8') as f:
        target_content = f.read()

    target_schema = get_ld_json(target_content)
    if target_schema:
        # Replace the target schema with the updated schema
        updated_content = target_content.replace(target_schema, schema)
    else:
        # Insert before </head>
        updated_content = target_content.replace('</head>', schema + '\n</head>')

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"Updated schema in {target_path}")

def main():
    for comp in competitors:
        # Source US compare page
        source = f"compare/hosterlo-vs-{comp}/index.html"
        
        # Target UK compare page
        target_uk = f"uk/compare/hosterlo-vs-{comp}/index.html"
        update_page_schema(source, target_uk, 'uk')
        
        # Target PK compare page
        target_pk = f"pk/compare/hosterlo-vs-{comp}/index.html"
        update_page_schema(source, target_pk, 'pk')

if __name__ == '__main__':
    main()
