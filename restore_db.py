import re

with open("First Versions/uganda-car-tax-standalone_3.html", "r") as f:
    html_content = f.read()

# find const DB = [ ... ];
match = re.search(r'const DB\s*=\s*(\[.*?\]);', html_content)
if match:
    db_json = match.group(1)
    
    with open("Js/script.js", "r") as f2:
        script_content = f2.read()
        
    # replace the current DB in script.js
    script_content = re.sub(r'const DB = \[\{.*?\}\];', f'const DB = {db_json};', script_content, flags=re.DOTALL)
    
    with open("Js/script.js", "w") as f3:
        f3.write(script_content)
    print("Successfully restored the 13,888 DB from backup!")
else:
    print("Could not find DB in backup.")
