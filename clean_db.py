import json
import re

file_path = "/Users/ninetynine/Documents/Tax calculator/Js/script.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the DB array
start_marker = "const DB = \n["
end_marker = "]\n// Stats"
start_idx = content.find(start_marker)
if start_idx == -1:
    start_marker = "const DB = \n[\n"
    start_idx = content.find(start_marker)
    if start_idx == -1:
        start_marker = "const DB ="
        start_idx = content.find(start_marker)

end_idx = content.find("// Stats", start_idx)

if start_idx != -1 and end_idx != -1:
    json_str = content[start_idx + len("const DB ="):end_idx].strip()
    try:
        data = json.loads(json_str)
        cleaned_data = []
        for item in data:
            cif_raw = item.get("__4", "0")
            cif_str = str(cif_raw).replace(",", "").strip()
            try:
                cif = float(cif_str)
            except:
                cif = 0.0

            cc_raw = item.get("__3", "")
            cc_str = str(cc_raw).replace("cc", "").replace("Hp", "").replace("Ton", "").replace("kW", "").strip()

            desc = item.get("__2", "")
            parts = [p.strip() for p in desc.split(",")]
            
            year = 0
            if parts and parts[-1].isdigit():
                year = int(parts[-1])
                model_desc = ", ".join(parts[:-1])
            else:
                model_desc = desc
            
            # Simple heuristic for Make/Model: first word is Make, rest is Model
            words = model_desc.split(" ", 1)
            if len(words) == 2:
                make = words[0]
                model = words[1]
                # specific fixes for two-word makes
                two_word_makes = ["Alfa Romeo", "Aston Martin", "Land Rover", "Ashok Leyland", "AM General", "Great Wall"]
                for tm in two_word_makes:
                    if model_desc.startswith(tm):
                        make = tm
                        model = model_desc[len(tm):].strip()
                        break
            else:
                make = model_desc
                model = ""

            cleaned_data.append({
                "make": make,
                "model": model,
                "chassis": "",
                "cc": cc_str,
                "fuel": "",
                "year": year,
                "cif": cif
            })

        new_json_str = json.dumps(cleaned_data, separators=(',', ':'))
        new_content = content[:start_idx] + "const DB = " + new_json_str + "\n" + content[end_idx:]
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Data cleaned and written successfully. Total records:", len(cleaned_data))
    except Exception as e:
        print("Error parsing JSON:", e)
else:
    print("Could not find DB array bounds")
