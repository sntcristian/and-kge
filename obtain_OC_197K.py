
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
from graph_extractor import query_to_graph, kg_to_tsv, kg_statistics
import time
from tqdm import tqdm

sparql = SPARQLWrapper('http://localhost:9999/blazegraph/sparql')

query = """prefix pro:	<http://purl.org/spar/pro/>
prefix fabio:	<http://purl.org/spar/fabio/>
prefix cito:	<http://purl.org/spar/cito/>
prefix dcterms:	<http://purl.org/dc/terms/>
prefix foaf:   <http://xmlns.com/foaf/0.1/>
prefix prism: <http://prismstandard.org/namespaces/basic/2.0/>
prefix frbr: <http://purl.org/vocab/frbr/core#>
SELECT DISTINCT ?article
WHERE {
?article a fabio:JournalArticle;
pro:isDocumentContextFor ?author1;
dcterms:title ?title;
prism:publicationDate ?date1;
cito:cites ?article2;
frbr:partOf ?issue1.
?issue1 a fabio:JournalIssue;
frbr:partOf ?volume1.
?volume1 a fabio:JournalVolume;
frbr:partOf ?journal1.
?journal1 a fabio:Journal;
dcterms:title ?journalTitle1.
?author1 pro:withRole pro:author;
pro:isHeldBy ?person1.
?person1 foaf:name ?name1.
?article2 a fabio:Expression;
dcterms:title ?title2;
prism:publicationDate ?date2;
pro:isDocumentContextFor ?author2.
?author2 pro:withRole pro:author.}
LIMIT 1000"""


sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print("query for selecting articles launched")
start_time = time.time()
print("query took %s seconds" % (time.time() - start_time))


print("constructing the graph for 1000 papers")
graph = Graph()
start_time = time.time()
pbar = tqdm(total=1000)
idx = 0

for result in results["results"]["bindings"]:
    idx += 1
    if idx == 1001:
        break
    else:
        article_uri = result["article"]["value"]
        construct_query = """prefix pro:	<http://purl.org/spar/pro/>
                prefix fabio:	<http://purl.org/spar/fabio/>
                prefix cito:	<http://purl.org/spar/cito/>
                prefix dcterms:	<http://purl.org/dc/terms/>
                prefix foaf:   <http://xmlns.com/foaf/0.1/>
                prefix prism: <http://prismstandard.org/namespaces/basic/2.0/>
                prefix frbr: <http://purl.org/vocab/frbr/core#>
                CONSTRUCT {<"""+ article_uri + """> dcterms:title ?title;
                cito:cites ?article2;
                prism:publicationDate ?date1;
                pro:isDocumentContextFor ?author1;
                frbr:partOf ?journal1.
                ?journal1 dcterms:title ?journalTitle1.
                ?author1 foaf:name ?name1.
                ?article2 dcterms:title ?title2;
                prism:publicationDate ?date2;
                frbr:partOf ?journal2;
                pro:isDocumentContextFor ?author2.
                ?journal2 dcterms:title ?journalTitle2.
                ?author2 foaf:name ?name2}
                WHERE {{<""" + article_uri + """> a fabio:JournalArticle;
                        pro:isDocumentContextFor ?author1;
                        dcterms:title ?title;
                        prism:publicationDate ?date1;
                        cito:cites ?article2;
                        frbr:partOf ?issue1.
                        ?issue1 a fabio:JournalIssue;
                        frbr:partOf ?volume1.
                        ?volume1 a fabio:JournalVolume;
                        frbr:partOf ?journal1.
                        ?journal1 a fabio:Journal;
                        dcterms:title ?journalTitle1.
                        ?author1 pro:withRole pro:author;
                        pro:isHeldBy ?person1.
                        ?person1 foaf:name ?name1.
                        ?article2 a fabio:Expression;
                        dcterms:title ?title2;
                        prism:publicationDate ?date2;
                        pro:isDocumentContextFor ?author2.
                        ?author2 pro:withRole pro:author;
                        pro:isHeldBy ?person2.
                        ?person2 foaf:name ?name2.}
                        UNION {
                        <""" + article_uri + """> a fabio:JournalArticle;
                        cito:cites ?article2.
                        ?article2 a fabio:Expression;
                        frbr:partOf ?issue2.
                        ?issue2 a fabio:JournalIssue;
                        frbr:partOf ?volume2.
                        ?volume2 a fabio:JournalVolume;
                        frbr:partOf ?journal2.
                        ?journal2 a fabio:Journal;
                        dcterms:title ?journalTitle2.
                        }}
                        """
        query_to_graph(construct_query, graph, sparql)
        pbar.update(1)
pbar.close()
print("process took %s seconds" % (time.time() - start_time))
kg_to_tsv(graph, "./OC-new/")
kg_statistics(graph, "./OC-new/")
#train_test_valid_split("./OC-new/")
#create_literals("./OC-new/")
print("done")