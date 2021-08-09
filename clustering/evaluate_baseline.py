import json
from tqdm import tqdm
import re



def compare_titles(author1, author2):
    titles1 = set(re.sub(r'[^\w\s]', '', author1["article"]).split())
    titles2 = set(re.sub(r'[^\w\s]', '', author2["article"]).split())
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
    journal1 = author1["journal"].strip()
    journal2 = author2["journal"].strip()
    if len(journal1) == 0 or len(journal2) == 0:
        return 0
    elif journal1 == journal2:
        return 1
    else:
        return 0

def common_references(author1, author2):
    references1 = set(author1["references"])
    references2 = set(author2["references"])
    if len(references1) == 0 or len(references2) == 0:
        return 0
    else:
        return len(references1.intersection(references2))

def compare_authors(author1, author2):
    score_coauthors = 0
    score_titles = 0
    score_journals = 0
    score_references = 0
    score = 0
    if compare_coauthors(author1, author2) == 1:
        score_coauthors += 3
    elif compare_coauthors(author1, author2) == 2:
        score_coauthors += 5
    elif compare_coauthors(author1, author2) > 2:
        score_coauthors += 8

    if compare_titles(author1, author2) == 1:
        score_titles += 3
    elif compare_titles(author1, author2) == 2:
        score_titles += 5
    elif compare_titles(author1, author2) >= 3:
        score_titles += 8

    if compare_journals(author1, author2) >= 1:
        score_journals += 4

    if common_references(author1, author2) == 1:
        score_references += 2
    elif common_references(author1, author2) == 2:
        score_references += 3
    elif common_references(author1, author2) >= 3:
        score_references += 5

    if score_coauthors+score_journals+score_titles+score_references>=5:
        score = 1
    return score


def evaluate(blocks):

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    pbar = tqdm(total=len(blocks))
    for authors in blocks:
        for idx1 in range(1, len(authors)):
            for idx2 in range(0, idx1):
                if compare_authors(authors[idx1], authors[idx2]) == 1 and authors[idx1]["label"] == authors[idx2]["label"]:
                    true_positive += 1
                elif compare_authors(authors[idx1], authors[idx2]) == 1 and authors[idx1]["label"] != authors[idx2]["label"]:
                    false_positive += 1
                elif compare_authors(authors[idx1], authors[idx2]) == 0  and authors[idx1]["label"] == authors[idx2][
                    "label"]:
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
    with open("baseline_evaluation.txt", "w") as outp:
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
    blocks = json.load(f)
    evaluate(blocks)