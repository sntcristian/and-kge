from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
from graph_extractor import query_to_graph, kg_to_tsv, kg_statistics
import time
from tqdm import tqdm

sparql = SPARQLWrapper('http://localhost:9999/blazegraph/sparql')


select_query = """
prefix fabio: <http://purl.org/spar/fabio/>
prefix prism: <http://prismstandard.org/namespaces/basic/2.0/>
prefix frbr: <http://purl.org/vocab/frbr/core#>
prefix dcterms: <http://purl.org/dc/terms/>

SELECT DISTINCT ?article
WHERE {
?article a fabio:JournalArticle
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
kg_to_tsv(graph, "./OC-new/")
kg_statistics(graph, "./OC-new/")
print("done")
