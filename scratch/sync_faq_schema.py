import os
import re
import json

base_dir = r"d:\Hosterlo Official Site"

def clean_html_text(text):
    # Remove span tags and clean extra whitespace
    text = re.sub(r'<span\b[^>]*>.*?</span>', '', text, flags=re.DOTALL)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_file(rel_path):
    path = os.path.join(base_dir, rel_path)
    if not os.path.exists(path):
        print(f"File not found: {rel_path}")
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Extract all FAQs
    faqs = []
    details_pattern = re.compile(r'<details\b[^>]*>(.*?)</details>', re.DOTALL)
    for match in details_pattern.finditer(content):
        inner = match.group(1)
        summary_match = re.search(r'<summary\b[^>]*>(.*?)</summary>', inner, re.DOTALL)
        div_match = re.search(r'<div\b[^>]*class="[^"]*pb-6[^"]*"[^>]*>(.*?)</div>', inner, re.DOTALL)
        
        if summary_match and div_match:
            q = clean_html_text(summary_match.group(1))
            a = clean_html_text(div_match.group(1))
            faqs.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            })
            
    print(f"Extracted {len(faqs)} FAQs from {rel_path}")
    
    if not faqs:
        return
        
    # 2. Parse the JSON-LD schema and replace the FAQPage mainEntity
    # Find the script block
    script_pattern = re.compile(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
    
    modified = False
    
    def replace_schema(match):
        nonlocal modified
        script_content = match.group(1)
        try:
            schema_data = json.loads(script_content)
            
            # Helper to update FAQPage
            def update_graph(graph_list):
                updated = False
                for obj in graph_list:
                    if obj.get("@type") == "FAQPage":
                        obj["mainEntity"] = faqs
                        updated = True
                return updated
                
            if isinstance(schema_data, dict):
                if "@graph" in schema_data:
                    if update_graph(schema_data["@graph"]):
                        modified = True
                elif schema_data.get("@type") == "FAQPage":
                    schema_data["mainEntity"] = faqs
                    modified = True
                    
            if modified:
                # Format JSON with indent
                formatted_json = json.dumps(schema_data, indent=2, ensure_ascii=False)
                # Align prefix space
                lines = formatted_json.splitlines()
                indented_lines = [lines[0]] + [f"  {line}" for line in lines[1:]]
                return f'<script type="application/ld+json">\n' + '\n'.join(indented_lines) + '\n</script>'
        except Exception as e:
            print("Error parsing schema:", e)
            
        return match.group(0)
        
    new_content = script_pattern.sub(replace_schema, content)
    
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully updated JSON-LD FAQ schema in {rel_path}")
    else:
        print(f"No FAQPage schema found or updated in {rel_path}")

def main():
    process_file("faq/index.html")
    process_file("es/faq/index.html")

if __name__ == "__main__":
    main()
