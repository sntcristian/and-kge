import pandas as pd
from re import match

df = pd.read_csv(filepath_or_buffer="OC-888K/kg.txt", sep="\t", header=None)

authors_lst = [ent for ent in df[2].values if match('https://github.com/arcangelo7/time_agnostic/ra/', ent)]
authors_set = set(authors_lst)
with open('OC-888K/authors_lst.txt', 'w') as f:
    f.writelines("%s\n" % author for author in authors_set)