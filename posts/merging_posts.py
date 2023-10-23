import json
import glob

json_objects = []

for f in glob.glob("*.json"):
    try:
        with open(f, "r", encoding='utf-8') as infile:
            file_content = json.load(infile)
            json_objects.append(file_content)
    except json.JSONDecodeError as e:
        pass

with open("prog_point.json", "w", encoding='utf-8') as outfile:
    json.dump(json_objects, outfile, ensure_ascii=False, indent=4)