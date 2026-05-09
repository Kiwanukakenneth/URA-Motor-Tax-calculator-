import json
import re

input_file = "csvjson.json"
output_file = "Js/script.js"

with open(input_file, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

normalized_data = []

for row in raw_data:
    if row.get("Motor vehicle Value Guide - Uganda Revenue Authority") == "S/N":
        continue
        
    desc = row.get("__2", "")
    if not desc:
        continue
        
    parts = [p.strip() for p in desc.split(",")]
    
    make_model_part = parts[0]
    first_space = make_model_part.find(" ")
    if first_space != -1:
        make = make_model_part[:first_space].strip()
        model = make_model_part[first_space+1:].strip()
    else:
        make = make_model_part.strip()
        model = ""
        
    chassis = ""
    year = 0
    
    other_parts = parts[1:]
    if other_parts:
        last_part = other_parts[-1]
        year_match = re.search(r'\b(19|20)\d{2}\b', last_part)
        if year_match:
            year = int(year_match.group())
            last_part = last_part.replace(year_match.group(), "").strip()
            other_parts[-1] = last_part
            
        for p in other_parts:
            if not p:
                continue
            if p.lower().startswith("model"):
                ch_candidate = p[5:].strip()
                if ch_candidate:
                    chassis = ch_candidate
            else:
                model += " " + p
                
    model = model.strip()
    
    cc_str = row.get("__3", "")
    cc_match = re.search(r'\d+', str(cc_str))
    cc = cc_match.group() if cc_match else ""
    
    cif_str = row.get("__4", "0")
    if isinstance(cif_str, str):
        cif_str = cif_str.replace(",", "").replace("$", "").strip()
    try:
        cif = float(cif_str)
    except ValueError:
        cif = 0.0
        
    normalized_data.append({
        "make": make,
        "model": model,
        "chassis": chassis,
        "cc": cc,
        "fuel": "",
        "year": year,
        "cif": cif
    })

with open("First Versions/uganda-car-tax-standalone_3.html", "r", encoding="utf-8") as f:
    html_text = f.read()

matches = list(re.finditer(r"<script>([\s\S]*?)</script>", html_text))
if matches:
    script_content = matches[-1].group(1)
    
    match = re.search(r"const DB = \[{", script_content)
    if match:
        s_start = match.start()
        s_end = script_content.find("// Stats", s_start)
        if s_end != -1:
            logic_only = script_content[s_end:]
            
            new_db_str = "const DB = " + json.dumps(normalized_data, separators=(',', ':')) + ";\n\n"
            # we also need the comment headers if any were before const DB = 
            headers = script_content[:s_start]
            
            new_script = headers + new_db_str + logic_only
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(new_script.strip())
            print(f"Successfully processed {len(normalized_data)} records and created clean script.js")
        else:
            print("Failed to find '// Stats'")
    else:
        print("Failed to find start of old DB array in logic")
else:
    print("Failed to extract logic from HTML")
