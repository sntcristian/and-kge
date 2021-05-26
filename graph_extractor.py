from SPARQLWrapper import SPARQLWrapper, RDFXML
from rdflib import Graph
import csv, re, json
import numpy as np
import pandas as pd
from ampligraph.evaluation import train_test_split_no_unseen

def query_to_graph(query, sparql):
    print("[INFO: Querying the SPARQL Endpoint]")
    sparql.setQuery(query)
    sparql.setReturnFormat(RDFXML)
    results = sparql.query().convert()
    graph = Graph().parse(data=results.serialize(format='xml'), format='xml')
    return graph



def kg_to_tsv(graph_lst, path):
    datatype_relations = {"http://xmlns.com/foaf/0.1/name", "http://xmlns.com/foaf/0.1/familyName", "http://xmlns.com/foaf/0.1/givenName", "http://purl.org/spar/fabio/hasSubtitle", "http://prismstandard.org/namespaces/basic/2.0/publicationDate", "http://purl.org/dc/terms/title", "http://purl.org/spar/c4o/hasContent"}
    print("[INFO: Writing the knowledge graph in " + path + "kg.txt]")
    with open(path+'kg.txt', "w", encoding="utf-8") as f:
        for g in graph_lst:
            for s, p, o in g:
                if str(p) in datatype_relations:
                    if str(p) == "http://prismstandard.org/namespaces/basic/2.0/publicationDate":
                        match = re.match(r"(\d{4})-\d{2}-\d{2}", str(o))
                        obj = match.group(1)
                    else:
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
    numerical_literals = set()
    relations = set()
    datatype_relations = {"http://xmlns.com/foaf/0.1/name", "http://xmlns.com/foaf/0.1/familyName", "http://xmlns.com/foaf/0.1/givenName", "http://purl.org/spar/fabio/hasSubtitle", "http://prismstandard.org/namespaces/basic/2.0/publicationDate", "http://purl.org/dc/terms/title", "http://purl.org/spar/c4o/hasContent"}
    for g in graph_lst:
        for s, p, o in g:
            num_of_triples += 1
            if str(p) in datatype_relations:
                num_of_literal_triples += 1
                if str(p) == "http://prismstandard.org/namespaces/basic/2.0/publicationDate":
                    numerical_literals.add(str(o))
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
        "num_of_numeric_literals": len(numerical_literals)
    }
    print("[INFO: Writing knowledge graph statistics in " + path + "kg_statistics.json]")
    with open(path + 'kg_statistics.json', 'w') as fp:
        json.dump(output_dict, fp)


def train_test_valid_split(path):
    df = pd.read_csv(path+"kg.txt", sep='\t', header=None)
    train, test = \
        np.split(df.sample(frac=1, random_state=42),
                 [int(.9 * len(df))])
    X_train, X_validate = train_test_split_no_unseen(train.values, test_size=5505, seed=48)
    pd.DataFrame(X_train).to_csv(path+'train.txt', sep='\t', header=None, index=False)
    test.to_csv(path+'test.txt', sep='\t', header=None, index=False)
    pd.DataFrame(X_validate).to_csv(path+'valid.txt', sep='\t', header=None, index=False)

def create_literals(path):
    df = pd.read_csv(path + "kg.txt", sep='\t', header=None)
    text_literals = []
    numerical_literals = []
    datatype_prop = {"http://xmlns.com/foaf/0.1/name", \
                     "http://xmlns.com/foaf/0.1/familyName", "http://xmlns.com/foaf/0.1/givenName", \
                     "http://purl.org/spar/fabio/hasSubtitle", \
                     "http://prismstandard.org/namespaces/basic/2.0/publicationDate", \
                     "http://purl.org/dc/terms/title", "http://purl.org/spar/c4o/hasContent"}
    for s, p, o in df.itertuples(index=False, name=None):
        if p in datatype_prop:
            if p == "http://prismstandard.org/namespaces/basic/2.0/publicationDate":
                numerical_literals.append([s, p, o])
            else:
                text_literals.append([s, p, o])
    pd.DataFrame(text_literals).to_csv(path+'literals/text_literals.txt', sep='\t', header=None, index=False)
    pd.DataFrame(numerical_literals).to_csv(path + 'literals/numerical_literals.txt', sep='\t', header=None, index=False)
            else:
                text_literals.append([s, p, o])
    pd.DataFrame(text_literals).to_csv(path+'literals/text_literals.txt', sep='\t', header=None, index=False)
    pd.DataFrame(numerical_literals).to_csv(path + 'literals/numerical_literals.txt', sep='\t', header=None, index=False)