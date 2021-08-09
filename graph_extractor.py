from SPARQLWrapper import SPARQLWrapper, RDFXML
from rdflib import Graph
import csv, re, json
import socket


def query_to_graph(article_uri, graph, exception_lst):
    query = """
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

        CONSTRUCT {<""" + article_uri + """> dcterms:title ?title;
        prism:publicationDate ?date;
        frbr:partOf ?Journal;
        dcterms:creator ?author;
        cito:cites ?article2;
        skos:related ?reference.
        ?reference c4o:hasContent ?referenceTxt;
        skos:related ?citingArticle.
        ?Journal dcterms:title ?JournalTitle.
        }
        WHERE {
        {<""" + article_uri + """> dcterms:title ?title;
        prism:publicationDate ?date;
        pro:isDocumentContextFor ?role.
        ?role pro:withRole pro:author;
        pro:isHeldBy ?author.}
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
        ?article2 a fabio:JournalArticle}
        UNION 
        {<""" + article_uri + """> frbr:part ?reference.
        ?reference c4o:hasContent ?referenceTxt;
        biro:references ?citingArticle}
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
    datatype_relations = {"http://purl.org/dc/terms/title", "http://purl.org/spar/c4o/hasContent"}
    print("[INFO: Writing the knowledge graph in " + path + "kg.txt]")
    with open(path+'kg.txt', "w", encoding="utf-8") as kg:
        with open(path + 'textual_literals.txt', "w", encoding="utf-8") as kg_txt_literals:
            with open(path + 'numerical_literals.txt', "w", encoding="utf-8") as kg_num_literals:
                for s, p, o in graph:
                    if str(p) == "http://purl.org/spar/cito/cites" and s == o:
                        continue
                    elif str(p) in datatype_relations:
                        lit = re.sub("\s+", " ", str(o))
                        kg_txt_literals.write(str(s) + "\t" + str(p) + "\t" + lit + "\n")
                    elif str(p) == "http://prismstandard.org/namespaces/basic/2.0/publicationDate":
                        match = re.match(r"(\d{4})-\d{2}-\d{2}", str(o))
                        obj = match.group(1)
                        kg_num_literals.write(str(s) + "\t" + str(p) + "\t" + obj + "\n")
                    else:
                        obj = str(o)
                        kg.write(str(s) + "\t" + str(p) + "\t" + obj + "\n")


def kg_statistics(graph, path):
    num_of_triples = 0
    num_of_textual_triples = 0
    num_of_numeric_triples = 0
    num_of_obj_triples = 0
    entities = set()
    textual_literals = set()
    numerical_literals = set()
    relations = set()
    datatype_relations = {"http://xmlns.com/foaf/0.1/name", "http://xmlns.com/foaf/0.1/familyName", "http://xmlns.com/foaf/0.1/givenName", "http://purl.org/spar/fabio/hasSubtitle", "http://purl.org/dc/terms/title", "http://purl.org/spar/c4o/hasContent"}
    for s, p, o in graph:
        if str(p) == "http://purl.org/spar/cito/cites" and s==o:
            continue
        elif str(p) in datatype_relations:
            num_of_textual_triples += 1
            lit = re.sub("\s+", " ", str(o))
            textual_literals.add(str(lit))
        elif str(p) == "http://prismstandard.org/namespaces/basic/2.0/publicationDate":
            num_of_numeric_triples += 1
            numerical_literals.add(str(o))
        else:
            entities.add(str(o))
            num_of_obj_triples += 1
        entities.add(str(s))
        relations.add(str(p))
        num_of_triples+=1
    output_dict = {
        "num_of_triples": num_of_triples,
        "num_of_textual_triples": num_of_textual_triples,
        "num_of_numeric_triples": num_of_numeric_triples,
        "num_of_obj_triples": num_of_obj_triples,
        "num_of_entities": len(entities),
        "num_of_relations": len(relations),
        "num_of_textual_literals": len(textual_literals),
        "num_of_numerical_literals": len(numerical_literals),
    }
    print("[INFO: Writing knowledge graph statistics in " + path + "kg_statistics.json]")
    with open(path + 'kg_statistics.json', 'w') as fp:
        json.dump(output_dict, fp)