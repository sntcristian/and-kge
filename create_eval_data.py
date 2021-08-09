from SPARQLWrapper import SPARQLWrapper, JSON
import time
import json
from tqdm import tqdm

with open('../OC-888K/authors_lst.txt', 'r') as f:
    authors_lst = f.read().split("\n")

list_of_dicts = []
sparql = SPARQLWrapper('http://localhost:9999/blazegraph/sparql')
pbar = tqdm(total=len(authors_lst))
for author_uri in authors_lst:
    select_query = """
    prefix pro: <http://purl.org/spar/pro/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix literal: <http://www.essepuntato.it/2010/06/literalreification/>
    prefix datacite: <http://purl.org/spar/datacite/>
    prefix dcterms: <http://purl.org/dc/terms/>
    prefix fabio: <http://purl.org/spar/fabio/>
    SELECT ?familyName ?givenName ?orcid ?article ?title
    WHERE {?article a fabio:Expression;
    dcterms:title ?title;
    pro:isDocumentContextFor ?role.
    ?role pro:isHeldBy <"""+author_uri+""">.
    <"""+author_uri+"""> foaf:familyName ?familyName;
    foaf:givenName ?givenName;
    datacite:hasIdentifier ?id.
    ?id literal:hasLiteralValue ?orcid
    }"""
    sparql.setQuery(select_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if len(results["results"]["bindings"]) > 0:
        result = results["results"]["bindings"][0]
        familyName = result["familyName"]["value"]
        givenName = result["givenName"]["value"]
        orcid = result["orcid"]["value"]
        article = result["article"]["value"]
        article_title = result["title"]["value"]
        references = []
        coauthors = []
        journal_title = ""
        select_query1 = """
            prefix dcterms: <http://purl.org/dc/terms/>
            prefix frbr: <http://purl.org/vocab/frbr/core#>
            prefix fabio: <http://purl.org/spar/fabio/>
            SELECT ?journalTitle
            WHERE {<"""+ article + """> a fabio:JournalArticle;
            dcterms:title ?title;
            frbr:partOf ?journalissue.
            ?journalissue a fabio:JournalIssue;
            frbr:partOf ?journalvolume.
            ?journalvolume a fabio:JournalVolume;
            frbr:partOf ?journal.
            ?journal a fabio:Journal;
            dcterms:title ?journalTitle.
            }"""
        sparql.setQuery(select_query1)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            journal_title = results["results"]["bindings"][0]["journalTitle"]["value"]
        select_query2 = """
        prefix cito: <http://purl.org/spar/cito/>
        SELECT ?reference
        WHERE {<"""+article+"""> cito:cites ?reference}"""
        sparql.setQuery(select_query2)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            for result in results["results"]["bindings"]:
                references.append(result["reference"]["value"])
        select_query3 = """
        prefix pro: <http://purl.org/spar/pro/>
        prefix foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?familyName ?givenName
        WHERE {<"""+article+"""> pro:isDocumentContextFor ?role.
        ?role pro:isHeldBy ?author.
        ?author foaf:familyName ?familyName;
        foaf:givenName ?givenName.
        MINUS {?role pro:isHeldBy <"""+author_uri+""">}.}
        """
        sparql.setQuery(select_query3)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            for result in results["results"]["bindings"]:
                coauthors.append(result["familyName"]["value"]+" "+result["givenName"]["value"])
        entry = {
            "author": author_uri,
            "family_name": familyName,
            "given_name": givenName,
            "article": article_title,
            "journal": journal_title,
            "references": references,
            "coauthors": coauthors,
            "label": orcid
            }
        list_of_dicts.append(entry)
    pbar.update(1)
pbar.close()
sorted_lst = sorted(list_of_dicts, key=lambda k: k['family_name'].strip()+" "+k["given_name"].strip())

print("writing authors to ./clustering/data.json")

with open("./clustering/data.json", "w") as output_file:
    json.dump(sorted_lst, output_file, indent=4, sort_keys=True)
