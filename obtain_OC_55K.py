from SPARQLWrapper import SPARQLWrapper, JSON
from graph_extractor import query_to_graph, kg_to_tsv, kg_statistics, train_test_valid_split, create_literals
import time
from tqdm import tqdm

sparql = SPARQLWrapper('http://localhost:9999/blazegraph/sparql')

query = """prefix pro:	<http://purl.org/spar/pro/>
prefix fabio:	<http://purl.org/spar/fabio/>
prefix cito:	<http://purl.org/spar/cito/>
prefix dcterms:	<http://purl.org/dc/terms/>
prefix foaf:   <http://xmlns.com/foaf/0.1/>
prefix prism: <http://prismstandard.org/namespaces/basic/2.0/>
SELECT DISTINCT ?article
WHERE {
?article a fabio:JournalArticle;
pro:isDocumentContextFor ?author;
dcterms:title ?title;
prism:publicationDate ?date1;
cito:cites ?article2.
?author pro:withRole pro:author;
pro:isHeldBy ?person.
?person foaf:name ?name.
?article2 a fabio:Expression;
dcterms:title ?title2;
prism:publicationDate ?date2}
LIMIT 1000"""

##FILTER regex(?date1, "\d{4}-\d{2}-\d{2}")
##FILTER regex(?date2, "\d{4}-\d{2}-\d{2}")

sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print("query for selecting articles launched")
start_time = time.time()
print("query took %s seconds" % (time.time() - start_time))


print("constructing the graph for 1000 papers")
graph_lst = []
start_time = time.time()
pbar = tqdm(total=1000)
idx = 0
for result in results["results"]["bindings"]:
    idx += 1
    if idx == 1001:
        break
    else:
        article_uri = result["article"]["value"]
        construct_query = 'prefix pro:	<http://purl.org/spar/pro/>\
                prefix fabio:	<http://purl.org/spar/fabio/>\
                prefix cito:	<http://purl.org/spar/cito/>\
                prefix dcterms:	<http://purl.org/dc/terms/>\
                prefix foaf:   <http://xmlns.com/foaf/0.1/>\
                prefix prism: <http://prismstandard.org/namespaces/basic/2.0/>\
                CONSTRUCT {<'+ article_uri + '> dcterms:title ?title;\
                cito:cites ?article2;\
                prism:publicationDate ?date1;\
                pro:isDocumentContextFor ?author.\
                ?author foaf:name ?name.\
                ?article2 dcterms:title ?title2;\
                prism:publicationDate ?date2}\
                WHERE {<'+ article_uri + '> a fabio:JournalArticle;\
                        pro:isDocumentContextFor ?author;\
                            dcterms:title ?title;\
                            prism:publicationDate ?date1;\
                            cito:cites ?article2.\
                        ?author pro:withRole pro:author;\
                            pro:isHeldBy ?person.\
                        ?person foaf:name ?name.\
                        ?article2 a fabio:Expression;\
                            prism:publicationDate ?date2;\
                            dcterms:title ?title2}'
        graph_lst.append(query_to_graph(construct_query, sparql))
        pbar.update(1)
pbar.close()
print("process took %s seconds" % (time.time() - start_time))
kg_to_tsv(graph_lst, "./OC-55K/")
kg_statistics(graph_lst, "./OC-55K/")
train_test_valid_split("./OC-55K/")
create_literals("./OC-55K/")
print("done")

