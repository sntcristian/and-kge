from SPARQLWrapper import SPARQLWrapper, RDFXML
from rdflib import Graph
import csv, re, json
import socket
import time
from tqdm import tqdm

sparql = SPARQLWrapper('http://localhost:9999/blazegraph/sparql')

directory = "../dataset/"

def query_to_graph(article_uri, graph, exception_lst):
    query = """
        prefix fabio: <http://purl.org/spar/fabio/>
        prefix prism: <http://prismstandard.org/namespaces/basic/2.0/>
        prefix frbr: <http://purl.org/vocab/frbr/core#>
        prefix dcterms: <http://purl.org/dc/terms/>
        prefix foaf: <http://xmlns.com/foaf/0.1/>
        prefix cito: <http://purl.org/spar/cito/>
        prefix pro: <http://purl.org/spar/pro/>
        prefix oco: <https://w3id.org/oc/ontology/>

        CONSTRUCT {<""" + article_uri + """> dcterms:title ?title;
        prism:publicationDate ?date;
        frbr:partOf ?Journal;
        dcterms:creator ?author;
        cito:cites ?article2.
        ?Journal dcterms:title ?JournalTitle.
        ?author foaf:knows ?coauthor.
        ?coauthor foaf:knows ?author.
        }
        WHERE {
        {<""" + article_uri + """> dcterms:title ?title;
        pro:isDocumentContextFor ?role.
        ?role pro:withRole pro:author;
        pro:isHeldBy ?author.}
        UNION {<""" + article_uri + """> prism:publicationDate ?date}
        UNION {
        <""" + article_uri + """> frbr:partOf ?Issue.
        ?Issue a fabio:JournalIssue;
        frbr:partOf ?Volume.
        ?Volume a fabio:JournalVolume;
        frbr:partOf ?Journal.
        ?Journal a fabio:Journal;
        dcterms:title ?JournalTitle.
        }
        UNION
        {<""" + article_uri + """> cito:cites ?article2.
        ?article2 a fabio:Expression;
        pro:isDocumentContextFor ?role1;
        dcterms:title ?citedtitle}
        UNION
        {<""" + article_uri + """> pro:isDocumentContextFor ?role.
        ?role pro:withRole pro:author;
        pro:isHeldBy ?author.
        ?role oco:hasNext ?role2.
        ?role2 pro:isHeldBy ?coauthor}
        }
        """
    sparql = SPARQLWrapper('http://localhost:9999/blazegraph/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(RDFXML)
    sparql.setTimeout(60)
    print("[INFO: Querying the SPARQL Endpoint]")
    try:
        results = sparql.query().convert()
        graph.parse(data=results.serialize(format='xml'), format='xml')
    except socket.timeout:
        exception_lst.append(article_uri)


def kg_to_tsv(graph, path):
    print("[INFO: Writing the knowledge graph in " + path + "kg.txt]")
    with open(path+'kg.txt', "w", encoding="utf-8") as kg:
        with open(path + 'textual_literals.txt', "w", encoding="utf-8") as kg_txt_literals:
            with open(path + 'numeric_literals.txt', "w", encoding="utf-8") as kg_num_literals:
                for s, p, o in graph:
                    if str(p) == "http://purl.org/spar/cito/cites" and s == o:
                        continue
                    elif str(p) == "http://purl.org/dc/terms/title":
                        lit = re.sub("\s+", " ", str(o))
                        kg_txt_literals.write(str(s) + "\t" + str(p) + "\t" + lit + "\n")
                    elif str(p) == "http://prismstandard.org/namespaces/basic/2.0/publicationDate":
                        match = re.match(r"(\d{4}).*?", str(o))
                        if match:
                            obj = match.group(1)
                            kg_num_literals.write(str(s) + "\t" + str(p) + "\t" + obj + "\n")
                    else:
                        obj = str(o)
                        kg.write(str(s) + "\t" + str(p) + "\t" + obj + "\n")



select_query = """
prefix fabio: <http://purl.org/spar/fabio/>
prefix pro: <http://purl.org/spar/pro/>
prefix dcterms: <http://purl.org/dc/terms/>

SELECT DISTINCT ?article
WHERE {
?article a fabio:Expression;
dcterms:title ?title;
pro:isDocumentContextFor ?author.
?author pro:withRole pro:author.
}
"""
start_time = time.time()
print("query for selecting articles launched")
sparql.setQuery(select_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print("query took %s seconds" % (time.time() - start_time))

print("constructing the graph for papers")
graph = Graph()
start_time = time.time()
exceptions = []
pbar = tqdm(total=len(results["results"]["bindings"]))
for result in results["results"]["bindings"]:
    article_uri = result["article"]["value"]
    query_to_graph(article_uri, graph, exceptions)
    pbar.update(1)
pbar.close()
print("process took %s seconds" % (time.time() - start_time))

with open('exceptions.txt', 'w') as f:
    f.writelines("%s\n" % exception for exception in exceptions)

kg_to_tsv(graph, directory)
print("done")
