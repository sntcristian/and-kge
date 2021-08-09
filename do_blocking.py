
import json
from tqdm import tqdm

with open("./data.json", "r") as f:
    sorted_lst = json.load(f)

blocks = []



def LN_FI(dictionary):
    ln_fi = dictionary["family_name"].strip() + " " + dictionary["given_name"].strip()[0]
    return ln_fi


pbar = tqdm(total=len(sorted_lst))
while len(sorted_lst) > 1:
    key_author = sorted_lst[0]
    block = []
    block.append(key_author)
    idx = 1
    for item in sorted_lst[idx:]:
        if LN_FI(key_author) == LN_FI(item):
            idx += 1
            block.append(item)
        else:
            if len(block) > 1:
                blocks.append(block)
            sorted_lst = sorted_lst[idx:]
            pbar.update(idx)
            break
if len(sorted_lst)>0:
    pbar.update(1)
pbar.close()

with open("lnfi_blocks.json", "w") as output_file:
    json.dump(blocks, output_file, indent=4, sort_keys=True)

