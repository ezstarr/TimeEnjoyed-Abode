import json
from pprint import pprint

with open('tarot-images.json') as f:
    tarot_data = json.load(f)

tarot_keep = []
for tarot in tarot_data['cards']:
    new_card = {}
    new_card["deck"] = "5"
    new_card["name"] = tarot["name"]
    new_card["number"] = int(tarot["number"])
    new_card["keywords"] = ','.join(tarot["keywords"])
    new_card["description"] = ','.join(tarot["fortune_telling"])
    new_card["upright"] = ','.join(tarot["meanings"]["light"])
    new_card["reverse"] = ','.join(tarot["meanings"]["shadow"])
    new_card["element"] = tarot.get("Elemental", "")
    new_card["question"] = ','.join(tarot["Questions to Ask"])
    tarot_keep.append(new_card)


# pprint(tarot_keep)



with open('new_tarot', 'w') as f:
    json.dump(tarot_keep, f, indent=4)
