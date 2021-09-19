import json
from tqdm import tqdm
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


stop_words = set(stopwords.words('english'))

def check_self_citation(author1, author2):
    references1 = set(author1.get("references", ""))
    references2 = set(author2.get("references", ""))
    if len(references1) == 0 or len(references2) == 0:
        return None
    elif author1["work"] in references2 or author2["work"] in references1:
        return True
    else:
        return None

def compare_affiliation(author1, author2):
    affiliation1 = author1.get("affiliation", "")
    affiliation2 = author2.get("affiliation", "")
    if len(affiliation1) == 0 or len(affiliation2) == 0:
        return 0
    elif affiliation1 == affiliation2:
        return 1
    else:
        return 0

def compare_titles(author1, author2):
    title1_tokens = word_tokenize(author1["title"])
    title2_tokens = word_tokenize(author2["title"])
    titles1 = set([w for w in title1_tokens if not w.lower in stop_words])
    titles2 = set([w for w in title2_tokens if not w.lower in stop_words])
    if len(titles1) == 0 or len(titles2) == 0:
        return 0
    else:
        return len(titles1.intersection(titles2))


def compare_coauthors(author1, author2):
    coauthors1 = set(author1["coauthors"])
    coauthors2 = set(author2["coauthors"])
    if len(coauthors1) == 0 or len(coauthors2) == 0:
        return 0
    else:
        return len(coauthors1.intersection(coauthors2))


def compare_journals(author1, author2):
    journal1 = author1["venue"].strip()
    journal2 = author2["venue"].strip()
    if len(journal1) == 0 or len(journal2) == 0:
        return 0
    elif journal1 == journal2:
        return 1
    else:
        return 0


def common_references(author1, author2):
    references1 = set(author1.get("references", ""))
    references2 = set(author2.get("references", ""))
    if len(references1) == 0 or len(references2) == 0:
        return 0
    else:
        return len(references1.intersection(references2))


def compare_authors(author1, author2):
    score_coauthors = 0
    score_titles = 0
    score_journals = 0
    score_references = 0
    score_affiliation = 0
    score = 0
    if compare_coauthors(author1, author2) == 1:
        score_coauthors += 4
    elif compare_coauthors(author1, author2) == 2:
        score_coauthors += 7
    elif compare_coauthors(author1, author2) > 2:
        score_coauthors += 10

    if compare_titles(author1, author2) == 1:
        score_titles += 3
    elif compare_titles(author1, author2) == 2:
        score_titles += 5
    elif compare_titles(author1, author2) >= 3:
        score_titles += 8

    if compare_journals(author1, author2) >= 1:
        score_journals += 6

    if common_references(author1, author2) == 1:
        score_references += 2
    elif common_references(author1, author2) == 2:
        score_references += 3
    elif common_references(author1, author2) == 3:
        score_references += 6
    elif common_references(author1, author2) == 4:
        score_references += 8
    elif common_references(author1, author2) > 4:
        score_references += 10

    if compare_affiliation(author1, author2) == 1:
        score_affiliation += 6

    if check_self_citation(author1, author2):
        score_references += 10

    if score_coauthors + score_journals + score_titles + score_references + score_affiliation >= 10:
        score = 1
    return score


def evaluate_no_macro(blocks):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    pbar = tqdm(total=len(blocks))
    for name in blocks.keys():
        block = blocks[name]
        for idx1 in range(1, len(block)):
            true_label1 = block[idx1]["label"]
            for idx2 in range(0, idx1):
                true_label2 = block[idx2]["label"]
                if compare_authors(block[idx1], block[idx2]) == 1 and true_label1 == true_label2:
                    true_positive += 1
                elif compare_authors(block[idx1], block[idx2]) == 1 and true_label1 != true_label2:
                    false_positive += 1
                elif compare_authors(block[idx1], block[idx2]) == 0 and true_label1 == true_label2:
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
    f1_score = 2 * ((precision * recall) / (precision + recall))
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

def evaluate_macro(blocks):
    precision_values = []
    recall_values = []
    f1_values = []
    pbar = tqdm(total=len(blocks))
    for name in blocks.keys():
        block = blocks[name]
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0
        for idx1 in range(1, len(block)):
            true_label1 = block[idx1]["label"]
            for idx2 in range(0, idx1):
                true_label2 = block[idx2]["label"]
                if compare_authors(block[idx1], block[idx2]) == 1 and true_label1 == true_label2:
                    true_positive += 1
                elif compare_authors(block[idx1], block[idx2]) == 1 and true_label1 != true_label2:
                    false_positive += 1
                elif compare_authors(block[idx1], block[idx2]) == 0 and true_label1 == true_label2:
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

# eval_data_path = "./aminer_blocks.json"

# with open(eval_data_path, "r") as f:
#     eval_data = json.load(f)

# evaluation_results = evaluate_macro(eval_data)
# with open("./aminer_baseline2.json", "w") as output_file:
#     json.dump(evaluation_results, output_file, indent=4, sort_keys=True)
# output_file.close()