import json
import re

with open("./data/global/name_to_pubs_test_100.json", "r") as f1:
    test_set = json.load(f1)

with open("auth_to_id.json") as f2:
    auth_to_id = json.load(f2)

test_data = dict()

n = len(test_set)
for name in test_set:
    pub_lst = []
    for id in test_set[name]:
        for pub in test_set[name][id]:
            pub_id = re.sub('-\d+', '', pub)
            masked_id = ""
            for item in auth_to_id:
                if item["paper"] == pub_id and item["id"] == id:
                    masked_id = item["masked_id"]
                    break
            pub_lst.append((pub_id, id, masked_id))
    test_data[name] = pub_lst
    print(n)
    n-=1

with open("./clustering/eval_data.json", "w") as output_file:
    json.dump(test_data, output_file, indent=4, sort_keys=True)