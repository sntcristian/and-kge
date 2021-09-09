from SPARQLWrapper import SPARQLWrapper, JSON
import time
import json
from tqdm import tqdm
import pandas as pd
from re import match

dataset_directory = "../dataset/"
df = pd.read_csv(filepath_or_buffer=dataset_directory+"kg.txt", sep="\t", header=None)

authors_lst = [ent for ent in df[2].values if match('https://github.com/arcangelo7/time_agnostic/ra/', ent)]
authors_set = set(authors_lst)
pub_set = set()
list_of_dicts = []
sparql = SPARQLWrapper('http://localhost:9999/blazegraph/sparql')
pbar = tqdm(total=len(authors_set))
for author_uri in authors_set:
    select_query = """
    prefix pro: <http://purl.org/spar/pro/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix literal: <http://www.essepuntato.it/2010/06/literalreification/>
    prefix datacite: <http://purl.org/spar/datacite/>
    prefix fabio: <http://purl.org/spar/fabio/>
    SELECT ?familyName ?givenName ?orcid ?article
    WHERE {?article a fabio:JournalArticle;
    pro:isDocumentContextFor ?role.
    ?role pro:isHeldBy <"""+author_uri+""">.
    <"""+author_uri+"""> foaf:familyName ?familyName;
    foaf:givenName ?givenName;
    datacite:hasIdentifier ?id.
    ?id literal:hasLiteralValue ?orcid
    }
    """
    sparql.setQuery(select_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if len(results["results"]["bindings"]) > 0:
        for result in results["results"]["bindings"]:
            author = author_uri
            familyName = result["familyName"]["value"]
            givenName = result["givenName"]["value"]
            orcid = result["orcid"]["value"]
            article = result["article"]["value"]
            if article not in pub_set:
                pub_set.add(article)
                list_of_dicts.append({"author": author,
                "family_name": familyName,
                "given_name": givenName,
                "orcid": orcid,
                "article": article})
    pbar.update(1)
pbar.close()
sorted_lst = sorted(list_of_dicts, key=lambda k: k['family_name']+" "+k["given_name"])

print("writing authors to ../clustering/data.json")


print("writing authors to ../clustering/authors.csv")
keys = sorted_lst[0].keys()
with open("../clustering/authors.csv", 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(sorted_lst)
output_file.close()
