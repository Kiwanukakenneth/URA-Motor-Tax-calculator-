import json

file_path = "/Users/ninetynine/Documents/Tax calculator/Js/script.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# The file is messed up. Let's find the dirty JSON array.
# It starts with "[" and ends with "]" and has a bunch of items.
start_idx = content.find("[\n  {\n    \"Motor vehicle Value Guide")
if start_idx == -1:
    start_idx = content.find("[\n  {")

end_idx = content.rfind("]\n")
if end_idx == -1:
    end_idx = content.rfind("]")

print(f"JSON bounds: {start_idx} to {end_idx}")

if start_idx != -1 and end_idx != -1:
    json_str = content[start_idx:end_idx+1]
    
    # Try parsing
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
            
            words = model_desc.split(" ", 1)
            if len(words) == 2:
                make = words[0]
                model = words[1]
                two_word_makes = ["Alfa Romeo", "Aston Martin", "Land Rover", "Ashok Leyland", "AM General", "Great Wall"]
                for tm in two_word_makes:
                    if model_desc.startswith(tm):
                        make = tm
                        model = model_desc[len(tm):].strip()
                        break
            else:
                make = model_desc
                model = ""

            # Only add if it looks like a valid car (has Make)
            if make and cif > 0:
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
        print(f"Cleaned {len(cleaned_data)} records.")
        
        # Now let's grab the JS logic
        # It's at the top of the file up to the JSON array, but wait! The user overwrote lines 1-457.
        # Let's extract the JS logic from the start up to the `[`
        js_logic = content[:start_idx]
        
        # But wait, the user's diff shows `const DB = \n// Stats` at the top.
        # So we need to inject the new_json_str right after `const DB = `
        
        js_logic = js_logic.replace("const DB = \n// Stats", "const DB = " + new_json_str + "\n// Stats")
        js_logic = js_logic.replace("const DB =\n// Stats", "const DB = " + new_json_str + "\n// Stats")
        
        if "const DB =" not in js_logic:
            # Fallback
            js_logic = "const DB = " + new_json_str + ";\n" + js_logic

        # Write the completely fixed file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(js_logic)
            
        print("File completely rebuilt!")

    except Exception as e:
        print("JSON parse error:", e)
else:
    print("Could not find dirty JSON array bounds")

