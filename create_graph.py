from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
from graph_extractor import query_to_graph, kg_to_tsv, kg_statistics
import time
from tqdm import tqdm

sparql = SPARQLWrapper('http://192.168.2.1:9999/blazegraph/sparql')


select_query = """
prefix fabio: <http://purl.org/spar/fabio/>
prefix prism: <http://prismstandard.org/namespaces/basic/2.0/>
prefix frbr: <http://purl.org/vocab/frbr/core#>
prefix dcterms: <http://purl.org/dc/terms/>

SELECT ?article
WHERE {
?article a fabio:JournalArticle;
frbr:partOf ?Issue.
?Issue frbr:partOf ?Volume.
?Volume frbr:partOf <https://github.com/arcangelo7/time_agnostic/br/1>
}
"""
start_time = time.time()
print("query for selecting articles launched")
sparql.setQuery(select_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print("query took %s seconds" % (time.time() - start_time))

print("constructing the graph for scientometrics papers after 2000s")
graph = Graph()
start_time = time.time()
pbar = tqdm(total=len(results["results"]["bindings"]))

construct_scient = """
prefix dcterms: <http://purl.org/dc/terms/>
CONSTRUCT {
<https://github.com/arcangelo7/time_agnostic/br/1> dcterms:title ?title
}
WHERE {
<https://github.com/arcangelo7/time_agnostic/br/1> dcterms:title ?title
}
"""
query_to_graph(construct_scient, graph, sparql)

for result in results["results"]["bindings"]:
    article_uri = result["article"]["value"]
    construct_query = """
        prefix fabio: <http://purl.org/spar/fabio/>
        prefix prism: <http://prismstandard.org/namespaces/basic/2.0/>
        prefix frbr: <http://purl.org/vocab/frbr/core#>
        prefix dcterms: <http://purl.org/dc/terms/>
        prefix foaf: <http://xmlns.com/foaf/0.1/>
        prefix cito: <http://purl.org/spar/cito/>
        prefix skos: <http://www.w3.org/2004/02/skos/core#>
        prefix c4o: <http://purl.org/spar/c4o/>
        prefix pro: <http://purl.org/spar/pro/>
        prefix biro: <http://purl.org/spar/biro/>
        
        CONSTRUCT {<""" + article_uri + """> dcterms:title ?title1;
        prism:publicationDate ?date1;
        frbr:partOf <https://github.com/arcangelo7/time_agnostic/br/1>;
        dcterms:creator ?author1;
        cito:cites ?article2;
        skos:related ?reference.
        ?reference c4o:hasContent ?referenceTxt;
        skos:related ?citingArticle.
        ?article2 dcterms:title ?title2;
        prism:publicationDate ?date2;
        frbr:partOf ?citedJournal;
        dcterms:creator ?author2.
        ?citedJournal dcterms:title ?citedJournalTitle.
        ?author1 foaf:knows ?coauthor1.
        ?author2 foaf:knows ?coauthor2.
        }
        WHERE {
        {<""" + article_uri + """> dcterms:title ?title1;
        prism:publicationDate ?date1;
        pro:isDocumentContextFor ?role1.
        ?role1 pro:isHeldBy ?author1.}
        UNION 
        {<""" + article_uri + """> pro:isDocumentContextFor ?role1;
        pro:isDocumentContextFor ?role3.
        ?role1 pro:isHeldBy ?author1.
        ?role3 pro:isHeldBy ?coauthor1.
        ?author1 foaf:name ?name1
        MINUS {?coauthor1 foaf:name ?name1}}
        UNION
        {<""" + article_uri + """> cito:cites ?article2.
        ?article2 dcterms:title ?title2;
        prism:publicationDate ?date2;
        pro:isDocumentContextFor ?role2.
        ?role2 pro:isHeldBy ?author2.}
        UNION
        {<""" + article_uri + """> cito:cites ?article2.
        ?article2 pro:isDocumentContextFor ?role2;
        pro:isDocumentContextFor ?role4.
        ?role2 pro:isHeldBy ?author2.
        ?role4 pro:isHeldBy ?coauthor2.
        ?author2 foaf:name ?name2
        MINUS {?coauthor2 foaf:name ?name2}}
        UNION 
        {<""" + article_uri + """> cito:cites ?article2.
        ?article2 a fabio:JournalArticle;
        frbr:partOf ?issue.
        ?issue frbr:partOf ?volume.
        ?volume frbr:partOf ?citedJournal.
        ?citedJournal dcterms:title ?citedJournalTitle.}
        UNION 
        {<""" + article_uri + """> frbr:part ?reference.
        ?reference c4o:hasContent ?referenceTxt;
        biro:references ?citingArticle}
        }
        """
    query_to_graph(construct_query, graph, sparql)
    pbar.update(1)
pbar.close()
print("process took %s seconds" % (time.time() - start_time))
graph.serialize(destination="OC-new/graph.xml", format="xml")
kg_to_tsv(graph, "./OC-new/")
kg_statistics(graph, "./OC-new/")
print("done")
