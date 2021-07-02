from SPARQLWrapper import SPARQLWrapper, RDFXML
from rdflib import Graph
import csv, re, json



def query_to_graph(query, graph, sparql):
    print("[INFO: Querying the SPARQL Endpoint]")
    sparql.setQuery(query)
    sparql.setReturnFormat(RDFXML)
    results = sparql.query().convert()
    graph.parse(data=results.serialize(format='xml'), format='xml')




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