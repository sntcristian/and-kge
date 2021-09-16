from author_disambig import cluster_embeddings, evaluate_macro, evaluate_no_macro
import torch
import json

def threshold_study(low, high, step, model, eval_data, macro, path):
    current_study = 0
    best_study = 0
    best_f1 = 0
    threshold = low
    precision_values = []
    recall_values = []
    thresholds = []
    f1_values = []
    while threshold <= high:
        current_study += 1
        cluster_data = cluster_embeddings(model=model, blocks=eval_data, affinity_type="cosine", linkage="single",
                                             threshold=threshold)
        if macro:
            evaluation_results = evaluate_macro(cluster_data, eval_data)
        else:
            evaluation_results = evaluate_no_macro(cluster_data, eval_data)
        precision_values.append(evaluation_results["precision"])
        recall_values.append(evaluation_results["recall"])
        f1_values.append(evaluation_results["F1 score"])
        thresholds.append(threshold)
        if best_f1 < evaluation_results["F1 score"] and evaluation_results["precision"] >= evaluation_results["recall"]:
            best_f1 = evaluation_results["F1 score"]
            best_study = current_study
        threshold += step
        threshold = round(threshold, 2)

    with open(path+"threshold_study.txt", "w") as outp:
        for idx, (precision, recall, f1, threshold) in enumerate(zip(precision_values, recall_values, f1_values, thresholds)):
            outp.write("Study: "+ str(idx+1) + "\n")
            outp.write("Threshold: " + str(threshold) + "\n")
            outp.write("Precision: " + str(precision) + "\n")
            outp.write("Recall: " + str(recall) + "\n")
            outp.write("F1: " + str(f1) + "\n\n")
        outp.write("Best study is " + str(best_study) + " with F1 score: "+ str(best_f1)+"\n")
    outp.close()


model_path = "../models/aminer/DISTMULT/trained_model.pkl"
eval_data_path = "./aminer/blocks.json"
with open(eval_data_path, "r") as f:
     eval_data = json.load(f)

model = torch.load(model_path, map_location=torch.device('cpu'))

threshold_study(low=0.2, high=0.4, step=0.02, model=model, eval_data=eval_data, macro=True, path="./aminer/")

