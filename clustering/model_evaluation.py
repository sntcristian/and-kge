import json
import pykeen
import torch
from sklearn.cluster import AgglomerativeClustering
import time
from tqdm import tqdm


model = torch.load("../model/trained_model.pkl", map_location=torch.device('cpu'))


def do_authors_clustering(model, blocks, affinity_type, linkage, threshold):
    entity_representation_modules = model.entity_embeddings
    entity_to_id = model.triples_factory.entity_to_id
    output_lst = []
    print("clustering blocks")
    pbar = tqdm(total=len(blocks))
    start_time = time.time()
    for block in blocks:
        lst_of_dicts = []
        entity_idx = torch.tensor([entity_to_id[author["author"]] for author in block],
                                  dtype=torch.long)
        entity_embeddings = entity_representation_modules.forward(indices=entity_idx).detach().numpy()
        result = AgglomerativeClustering(n_clusters=None, affinity=affinity_type, linkage=linkage, compute_full_tree=True,
                                        distance_threshold=threshold).fit(entity_embeddings)
        for x, y in zip(block, result.labels_):
          d = {"id": str(x["author"]), "label": int(y)}
          lst_of_dicts.append(d)
        output_lst.append(lst_of_dicts)
        pbar.update(1)
    pbar.close()
    print("process took %s seconds" % (time.time() - start_time))
    return output_lst


def evaluate(clustered_blocks, true_blocks):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    pbar = tqdm(total=len(clustered_blocks))
    for block1, block2 in zip(clustered_blocks, true_blocks):
        for idx1 in range(1, len(block1)):
            for idx2 in range(0, idx1):
                if block1[idx1]["label"] == block1[idx2]["label"] and block2[idx1]["label"] == block2[idx2]["label"]:
                    true_positive += 1
                elif block1[idx1]["label"] == block1[idx2]["label"] and block2[idx1]["label"] != block2[idx2]["label"]:
                    false_positive += 1
                elif block1[idx1]["label"] != block1[idx2]["label"] and block2[idx1]["label"] == block2[idx2]["label"]:
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
    accuracy = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)
    with open("model_evaluation.txt", "w") as outp:
        outp.write("Total comparisons: " + str(total_comparisons) + "\n")
        outp.write("Total positives: " + str(total_positives) + "\n")
        outp.write("Total negatives: " + str(total_negatives) + "\n\n")
        outp.write("True positives: " + str(true_positive) + "\n")
        outp.write("False positives: " + str(false_positive) + "\n")
        outp.write("True negatives: " + str(true_negative) + "\n")
        outp.write("False negatives: " + str(false_negative) + "\n\n")
        outp.write("Precision: " + str(precision) + "\n")
        outp.write("Recall: " + str(recall) + "\n")
        outp.write("Accuracy: " + str(accuracy) + "\n\n")



with open("./lnfi_blocks.json", "r") as f:
    eval_data = json.load(f)
f.close()


cluster_data = do_authors_clustering(model=model, blocks=eval_data, affinity_type="cosine", linkage="average", threshold=0.715) 


with open("model_labels.json", "w") as output_file:
      json.dump(cluster_data, output_file, indent=4)
output_file.close()

evaluate(cluster_data, eval_data)