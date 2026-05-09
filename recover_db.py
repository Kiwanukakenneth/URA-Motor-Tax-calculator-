import re

with open("First Versions/uganda-car-tax-standalone_3.html", "r", encoding="utf-8") as f:
    html_content = f.read()

match = re.search(r"const DB = \[{", html_content)
start_idx = match.start()
end_idx = html_content.find("];", start_idx)
db_array = html_content[start_idx:end_idx+2]

with open("Js/script.js", "w", encoding="utf-8") as f3:
    # Just write the db array and some basic logic or just extract the logic from the html?
    # Actually, script.js was originally written by separating out the HTML.
    pass

