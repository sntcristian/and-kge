import pykeen
from pykeen.triples import TriplesFactory, TriplesLiteralsFactory
import numpy as np
import pandas as pd
import json

folder = "./OC-new/"

tf = TriplesLiteralsFactory(path=folder+"kg.txt", path_to_numeric_triples=folder+"numeric_literals.txt",
                            path_to_textual_triples=folder+"textual_literals.txt", save_literals=True)

with open(folder+'pykeen/entity_to_id.json', 'w') as f1:
    json.dump(tf.entity_to_id, f1)
f1.close()


with open(folder+'pykeen/relation_to_id.json', 'w') as f2:
    json.dump(tf.relation_to_id, f2)
f2.close()

training, testing = tf.split([.8, .2])
training, validation = training.split([.8, .2])

training_np = training.triples
testing_np = testing.triples
validation_np = validation.triples

training_df = pd.DataFrame(training_np)
validation_df = pd.DataFrame(validation_np)
testing_df = pd.DataFrame(testing_np)
training_df.to_csv(folder+"pykeen/training.txt", sep="\t", header=False, index=False)
validation_df.to_csv(folder+"pykeen/validation.txt", sep="\t", header=False, index=False)
testing_df.to_csv(folder+"pykeen/testing.txt", sep="\t", header=False, index=False)


with open(folder+'pykeen/entity_to_id.json', 'w') as f1:
    json.dump(training.entity_to_id, f1)
f1.close()


with open(folder+'pykeen/relation_to_id.json', 'w') as f2:
    json.dump(training.relation_to_id, f2)
f2.close()
