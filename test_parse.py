import json
import re

with open("csvjson.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

for i, row in enumerate(raw_data[100:150]):
    desc = row.get("__2", "")
    if not desc:
        continue
        
    parts = [p.strip() for p in desc.split(",")]
    
    make_model_part = parts[0]
    
    # split make and model from the first part
    first_space = make_model_part.find(" ")
    if first_space != -1:
        make = make_model_part[:first_space]
        model = make_model_part[first_space+1:]
    else:
        make = make_model_part
        model = ""
        
    chassis = ""
    year = 0
    
    # Process other parts
    other_parts = parts[1:]
    if other_parts:
        last_part = other_parts[-1]
        # try to extract year from the last part
        year_match = re.search(r'\b(19|20)\d{2}\b', last_part)
        if year_match:
            year = int(year_match.group())
            # remove year from last_part
            last_part = last_part.replace(year_match.group(), "").strip()
            other_parts[-1] = last_part
            
        for p in other_parts:
            if not p:
                continue
            if p.lower().startswith("model"):
                chassis = p[5:].strip()
            else:
                model += " " + p
                
    model = model.strip()
    
    print(f"RAW: {desc}")
    print(f" -> Make: '{make}', Model: '{model}', Chassis: '{chassis}', Year: {year}")

