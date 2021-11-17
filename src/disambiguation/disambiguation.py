import json
import pykeen
import torch
import csv
from sklearn.cluster import AgglomerativeClustering
from sentence_transformers import SentenceTransformer
import time
import numpy as np
from tqdm import tqdm


def LN_FI(dictionary):
    ln_fi = dictionary["family_name"].strip() + " " + dictionary["given_name"].strip()[0]
    return ln_fi


def do_blocking(csv_path):
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        list_of_dicts = list(reader)
        sorted_lst = sorted(list_of_dicts, key=lambda k: k['family_name'].strip()+" "+k["given_name"].strip())
        blocks = dict()
        while len(sorted_lst) > 1:
            key_name = LN_FI(sorted_lst[0])
            key_author = sorted_lst[0]
            block = list()
            block.append(key_author)
            idx = 1
            for item in sorted_lst[idx:]:
                if LN_FI(key_author) == LN_FI(item):
                    idx += 1
                    block.append(item)
                    if idx == len(sorted_lst) and len(block) > 1:
                        blocks[key_name] = block
                else:
                    if len(block) > 1:
                        blocks[key_name] = block
                    sorted_lst = sorted_lst[idx:]
                    break
        return blocks


def cluster_KGEs(model, blocks, affinity_type, linkage, threshold):
    entity_representation_modules = model.entity_embeddings
    entity_to_id = model.triples_factory.entity_to_id
    output_data = dict()
    print("clustering blocks")
    pbar = tqdm(total=len(blocks))
    start_time = time.time()
    n = 0
    for name in blocks.keys():
        block = blocks[name]
        n += 1
        output_data[name] = list()
        works_idx = torch.tensor([entity_to_id[pub["work"]] for pub in block],
                                  dtype=torch.long)
        works_embeddings = entity_representation_modules.forward(indices=works_idx).detach().numpy()

        authors_idx = torch.tensor([entity_to_id[pub["author"]] for pub in block],
                                 dtype=torch.long)
        authors_embeddings = entity_representation_modules.forward(indices=authors_idx).detach().numpy()

        concat_embeddings = np.hstack((works_embeddings, authors_embeddings))

        result = AgglomerativeClustering(n_clusters=None, affinity=affinity_type, linkage=linkage, compute_full_tree=True,
                                        distance_threshold=threshold).fit(concat_embeddings)

        for entry, cluster_label in zip(block, result.labels_):
            new_d = dict()
            new_d["author"] = entry["author"]
            new_d["work"] = entry["work"]
            new_d["label"] = "disambiguated-"+str(n)+"#"+str(cluster_label)
            output_data[name].append(new_d)
        pbar.update(1)
    pbar.close()
    print("process took %s seconds" % (time.time() - start_time))
    return output_data


def cluster_titles(blocks, affinity_type, linkage, threshold):
    model = SentenceTransformer('allenai-specter')
    output_data = dict()
    print("clustering blocks")
    pbar = tqdm(total=len(blocks))
    start_time = time.time()
    for name in blocks.keys():
        block = blocks[name]
        output_data[name] = list()
        titles = [pub["title"] for pub in block]
        embeddings = model.encode(titles)
        result = AgglomerativeClustering(n_clusters=None, affinity=affinity_type, linkage=linkage, compute_full_tree=True,
                                        distance_threshold=threshold).fit(embeddings)
        for entry, cluster_label in zip(block, result.labels_):
            new_d = dict()
            new_d["author"] = entry["author"]
            new_d["work"] = entry["work"]
            new_d["label"] = str(cluster_label)
            output_data[name].append(new_d)
        pbar.update(1)
    pbar.close()
    print("process took %s seconds" % (time.time() - start_time))
    return output_data


def evaluate_no_macro(x_blocks, y_blocks):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    pbar = tqdm(total=len(x_blocks.keys()))
    for name in x_blocks.keys():
        cluster_block = x_blocks[name]
        true_block = y_blocks[name]
        for idx1 in range(1, len(cluster_block)):
            cluster_label1 = cluster_block[idx1]["label"]
            true_label1 = true_block[idx1]["label"]
            for idx2 in range(0, idx1):
                cluster_label2 = cluster_block[idx2]["label"]
                true_label2 = true_block[idx2]["label"]
                if cluster_label1 == cluster_label2 and true_label1 == true_label2:
                    true_positive += 1
                elif cluster_label1 == cluster_label2 and true_label1 != true_label2:
                    false_positive += 1
                elif cluster_label1 != cluster_label2 and true_label1 == true_label2:
                    false_negative += 1
                else:
                    true_negative += 1
        pbar.update(1)
    pbar.close()

    total_comparisons = true_positive + false_positive + true_negative + false_negative
    total_positives = true_positive + false_negative
    total_negatives = true_negative + false_positive
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    f1_score = 2 * ((precision*recall)/(precision+recall))

    output_dict = {
        "total_comparisons": total_comparisons,
        "total_positives": total_positives,
        "total_negatives": total_negatives,
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": precision,
        "recall": recall,
        "F1 score": f1_score
    }
    return output_dict


def evaluate_macro(x_blocks, y_blocks):
    pbar = tqdm(total=len(x_blocks.keys()))
    precision_values = []
    recall_values = []
    f1_values = []
    for name in x_blocks.keys():
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0
        cluster_block = x_blocks[name]
        true_block = y_blocks[name]
        for idx1 in range(1, len(cluster_block)):
            cluster_label1 = cluster_block[idx1]["label"]
            true_label1 = true_block[idx1]["label"]
            for idx2 in range(0, idx1):
                cluster_label2 = cluster_block[idx2]["label"]
                true_label2 = true_block[idx2]["label"]
                if cluster_label1 == cluster_label2 and true_label1 == true_label2:
                    true_positive += 1
                elif cluster_label1 == cluster_label2 and true_label1 != true_label2:
                    false_positive += 1
                elif cluster_label1 != cluster_label2 and true_label1 == true_label2:
                    false_negative += 1
                else:
                    true_negative += 1
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        f1_score = 2 * ((precision * recall) / (precision + recall))
        precision_values.append(precision)
        recall_values.append(recall)
        f1_values.append(f1_score)
        pbar.update(1)
    pbar.close()

    precision = sum(precision_values) / len(precision_values)
    recall = sum(recall_values) / len(recall_values)
    f1_score = sum(f1_values) / len(f1_values)

    output_dict = {
        "precision": precision,
        "recall": recall,
        "F1 score": f1_score
    }
    return output_dict


# model_path = "../models/aminer/DISTMULTTEXT/trained_model.pkl"
# eval_data_path = "./ami_blocks.json"
# with open(eval_data_path, "r") as f:
#     eval_data = json.load(f)
#
# model = torch.load(model_path, map_location=torch.device('cpu'))
# cluster_data = cluster_embeddings(model=model, blocks=eval_data, affinity_type="cosine", linkage="single", threshold=0.26)
# evaluation_results = evaluate_macro(cluster_data, eval_data)
#
# with open("./aminer/distmulttext_results.json", "w") as output_file:
#     json.dump(evaluation_results, output_file, indent=4, sort_keys=True)
# output_file.close()
