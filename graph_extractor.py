from SPARQLWrapper import SPARQLWrapper, RDFXML
from rdflib import Graph
import csv
import re
import json

def query_endpoint(query, path):
    print("[INFO: Querying the SPARQL Endpoint]")
    sparql.setQuery(query)
    sparql.setReturnFormat(RDFXML)
    results = sparql.query().convert()
    print("[INFO: Parsing results in a graph and storing it in '" + path + "']")
    graph = Graph().parse(data=results.serialize(format='xml'), format='xml')
    graph.serialize(destination=path, format='turtle')
    return graph


def kg_to_tsv(graph_lst, path):
    datatype_relations = {"http://xmlns.com/foaf/0.1/name", "http://xmlns.com/foaf/0.1/familyName", "http://xmlns.com/foaf/0.1/givenName", "http://purl.org/spar/fabio/hasSubtitle", "http://prismstandard.org/namespaces/basic/2.0/publicationDate", "http://purl.org/dc/terms/title", "http://purl.org/spar/c4o/hasContent"}
    print("[INFO: Writing the knowledge graph in " + path + "kg.tsv]")
    with open(path+'kg.tsv', "w", encoding="utf-8") as f:
        for g in graph_lst:
            for s, p, o in g:
                if str(p) in datatype_relations:
                    obj = re.sub("\s+", " ", str(o))
                else:
                    obj = str(o)
                f.write(str(s) + "\t" + str(p) + "\t" + obj + "\n")



def kg_statistics(graph_lst, path):
    num_of_triples = 0
    num_of_literal_triples = 0
    num_of_obj_triples = 0
    entities = set()
    textual_literals = set()
    date_literals = set()
    relations = set()
    datatype_relations = {"http://xmlns.com/foaf/0.1/name", "http://xmlns.com/foaf/0.1/familyName", "http://xmlns.com/foaf/0.1/givenName", "http://purl.org/spar/fabio/hasSubtitle", "http://prismstandard.org/namespaces/basic/2.0/publicationDate", "http://purl.org/dc/terms/title", "http://purl.org/spar/c4o/hasContent"}
    for g in graph_lst:
        for s, p, o in g:
            num_of_triples += 1
            if str(p) in datatype_relations:
                num_of_literal_triples += 1
                if str(p) == "http://prismstandard.org/namespaces/basic/2.0/publicationDate":
                    date_literals.add(str(o))
                else:
                    textual_literals.add(str(o))
            else:
                entities.add(str(o))
                num_of_obj_triples += 1
            entities.add(str(s))
            relations.add(str(p))
    output_dict = {
        "num_of_triples": num_of_triples,
        "num_of_literal_triples": num_of_literal_triples,
        "num_of_obj_triples": num_of_obj_triples,
        "num_of_entities": len(entities),
        "num_of_relations": len(relations),
        "num_of_textual_literals": len(textual_literals),
        "num_of_numeric_literals": len(date_literals)
    }
    print("[INFO: Writing knowledge graph statistics in " + path + "kg_statistics.json]")
    with open(path + 'kg_statistics.json', 'w') as fp:
        json.dump(output_dict, fp)