import json
with open("clustering/lnfi_blocks.json", "r") as f:
    lst_of_lst = json.load(f)

total_orcids = set()
entries = 0
comparisons = 0
for block in lst_of_lst:
    orcid_set = set()
    for dictionary in block:
        orcid_set.add(dictionary["label"])
        entries += 1
    comparisons += (len(block)*(len(block)-1))/2
    total_orcids.update(orcid_set)

def compute_matches(lst_of_lists):
    # takes as input two lists of lists of dictionaries
    # and compute matches among labels for each block (list)
    # and returns a list of matches
    output = []
    for block in lst_of_lists:
      for idx1 in range(1, len(block)):
        for idx2 in range(0, idx1):
            if block[idx1]["label"] == block[idx2]["label"]:
                output.append(1)
            else:
                output.append(0)
    return output

true_matches = compute_matches(lst_of_lst)
positives = [match for match in true_matches if match==1]
negatives = [match for match in true_matches if match==0]
print("True positives are", len(positives))
print("True negatives are", len(negatives))
print("true authors are "+ str(len(total_orcids)) + " while author entries are "+ str(entries))
print("blocks are ", len(lst_of_lst))
print("number of comparisons are ", comparisons, "instead of ", entries*(entries-1)/2)
print("longest block in the list is", len(max(lst_of_lst, key=len)))