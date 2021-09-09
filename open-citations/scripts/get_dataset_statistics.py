import csv
import json

dataset_directory = "./"

output_data = dict()
resources = set()
journals = set()
authors = set()
entities = set()

def get_dataset_statistics(directory):
    f1 = open(directory+"kg.txt")
    obj_triples = list(csv.reader(f1, delimiter="\t"))

    f2 = open(directory+"textual_literals.txt")
    text_triples = list(csv.reader(f2, delimiter="\t"))

    f3 = open(directory+"numeric_literals.txt")
    numeric_triples = list(csv.reader(f3, delimiter="\t"))


    for s, p, o in obj_triples:
        entities.add(s)
        entities.add(o)
        if p in output_data:
            output_data[p] += 1
        else:
            output_data[p] = 1
        
        if p == "http://purl.org/dc/terms/creator":
            resources.add(s)
            authors.add(o)

        elif p == "http://purl.org/vocab/frbr/core#partOf":
            resources.add(s)
            journals.add(o)
        
    output_data["number_of_obj_triples"] = len(obj_triples)
    output_data["number_of_textual_triples"] = len(text_triples)
    output_data["number_of_numeric_triples"] = len(numeric_triples)
    output_data["number_of_entities"] = len(entities)
    output_data["number_of_authors"] = len(authors)
    output_data["number_of_resources"] = len(resources)
    output_data["number_of_journals"] = len(journals)

    with open(directory+'dataset_statistics.json', 'w') as output_file:
        json.dump(output_data, output_file, indent=4, sort_keys=True)


get_dataset_statistics(dataset_directory)