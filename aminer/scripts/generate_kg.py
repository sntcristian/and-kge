import json
import pandas as pd
from tqdm import tqdm
import re

with open("./data/global/name_to_pubs_test_100.json", "r") as f1:
    test_set = json.load(f1)


with open("./data/global/pubs_raw.json", "r") as f2:
    data = json.load(f2)

dataset_directory = "../AMiner-534K/"

pub_test = []
authors_test = set()


for author_name in test_set:
    for id in test_set[author_name]:
        pub_test.extend(test_set[author_name][id])
        authors_test.add(id)

pub_test = set([re.sub('-\d+', '', pub) for pub in pub_test])

structural_triples = []
textual_triples = []
numeric_triples = []

venues = {}
orgs = {}
venue_n = 0
org_n = 0
auth_n = 0
pbar = tqdm(total=len(data.keys()))
auth_to_id = list()
for pub_id in data.keys():
    if pub_id in pub_test:
        authors_lst = []
        pub = data[pub_id]
        for author in pub["authors"]:
            authors_lst.append({"id": author["id"],
                                "org": author.get("org", "")})
        title = pub["title"]
        venue = pub.get("venue", "")
        year = str(pub.get("year", ""))

        for author in authors_lst:
            if author["id"] not in authors_test:
                structural_triples.append([pub_id, "dcterms:creator", author["id"]])
                if len(author["org"]) > 0:
                    if author["org"] in orgs:
                        structural_triples.append([author["id"], "pro:relatesToOrganization", orgs[author["org"]]])
                    else:
                        orgs[author["org"]] = "org-" + str(org_n)
                        org_n += 1
                        structural_triples.append([author["id"], "pro:relatesToOrganization", orgs[author["org"]]])
            else:
                masked_id = "auth-"+str(auth_n)
                auth_n += 1
                structural_triples.append([pub_id, "dcterms:creator", masked_id])
                auth_to_id.append({"id": author["id"],
                                   "masked_id": masked_id,
                                   "paper": pub_id})

                if len(author["org"]) > 0:
                    if author["org"] in orgs:
                        structural_triples.append([masked_id, "pro:relatesToOrganization", orgs[author["org"]]])
                    else:
                        orgs[author["org"]] = "org-" + str(org_n)
                        org_n += 1
                        structural_triples.append([masked_id, "pro:relatesToOrganization", orgs[author["org"]]])

        textual_triples.append([pub_id, "dcterms:title", title])
        if len(year) > 0:
            numeric_triples.append([pub_id, "prism:publicationDate", year])
        if len(venue) > 0:
            if venue in venues:
                structural_triples.append([pub_id, "frbr:partOf", venues[venue]])
                textual_triples.append([venues[venue], "dcterms:title", venue])
            else:
                venues[venue] = "venue-"+str(venue_n)
                venue_n += 1
                structural_triples.append([pub_id, "frbr:partOf", venues[venue]])
                textual_triples.append([venues[venue], "dcterms:title", venue])
    pbar.update(1)

pbar.close()

structural_triples_df = pd.DataFrame(structural_triples)
textual_triples_df = pd.DataFrame(textual_triples)
numeric_triples_df = pd.DataFrame(numeric_triples)

structural_triples_df.to_csv(dataset_directory+"kg.txt", sep="\t", header=False, index=False)
textual_triples_df.to_csv(dataset_directory+"textual_literals.txt", sep="\t", header=False, index=False)
numeric_triples_df.to_csv(dataset_directory+"numeric_literals.txt", sep="\t", header=False, index=False)

with open(dataset_directory+'auth_to_id.json', 'w') as fp:
    json.dump(auth_to_id, fp, indent=4, sort_keys=True)