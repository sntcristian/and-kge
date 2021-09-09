
import json
import csv
from tqdm import tqdm

with open("../clustering/authors.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    lst_of_dicts = list(reader)

blocks = []

def LN_FI(dictionary):
    ln_fi = dictionary["family_name"] + " " + dictionary["given_name"][0]
    return ln_fi


pbar = tqdm(total=len(lst_of_dicts))

while len(lst_of_dicts) > 1:
    key_author = lst_of_dicts[0]
    block = [{"id": key_author["author"], "label": key_author["orcid"], "article": key_author["article"]}]
    idx = 1
    for item in lst_of_dicts[idx:]:
        if LN_FI(key_author) == LN_FI(item):
            idx += 1
            block.append({"id": item["author"], "label": item["orcid"], "article": item["article"]})
        else:
            if len(block) > 1:
                blocks.append(block)
            lst_of_dicts = lst_of_dicts[idx:]
            pbar.update(idx)
            break

if len(lst_of_dicts)>0:
    pbar.update(1)
pbar.close()


with open("../clustering/lnfi_blocks.json", "w") as output_file:
    json.dump(blocks, output_file, indent=4, sort_keys=True)
output_file.close()

