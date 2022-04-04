from nltk.tokenize import word_tokenize
import json
import os
from nltk import FreqDist
from nltk.util import ngrams
import math
from zemberek import TurkishMorphology
import string

def read():
    json_folder_path = os.path.join("2021-01")
    json_files = [x for x in os.listdir(json_folder_path) if
                  x.endswith("json") and not (x.__contains__("("))]  # tekrarlayan dosya kontrolu
    json_data = list()
    for json_file in json_files[:10]:
        json_file_path = os.path.join(json_folder_path, json_file)
        with open(json_file_path, "r", encoding="utf-8") as f:
            json_data.append(json.load(f))

    all_json = []

    for js in json_data:
        all_json.append(js["ictihat"])

    # with open("corpus.txt", "w", encoding="utf-8") as outfile:
    #     for tt in all_json:
    #         outfile.write(str(str.lower(tt)))
    # outfile.close()

    return all_json

def extract_bigrams(bigrams):

    all_json = read()
    morphology = TurkishMorphology.create_with_defaults()
    for line in all_json:
        if len(line) > 1:
            tokens = line.strip().split(' ')
            for i, token in enumerate(tokens):
                token = token.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
                if len(token) == 0:
                    continue

                if i + 1 < len(tokens):
                    next_token = tokens[i+1].translate(str.maketrans('', '', string.punctuation))  # remove punctuation
                    try:
                        analysis_results = morphology.analyze(next_token).analysis_results
                        if len(analysis_results) != 0:
                            next_token = analysis_results[0].item.root
                    except:
                        continue
                if i + 2 < len(tokens):
                    next_next_token = tokens[i+2].translate(str.maketrans('', '', string.punctuation))  # remove punctuation
                    try:
                        analysis_results = morphology.analyze(next_next_token).analysis_results
                        if len(analysis_results) != 0:
                            next_next_token = analysis_results[0].item.root
                    except:
                        continue

                try:
                    bigrams[f'{token} {next_token}'][0] += 1
                    bigrams[f'{token} {next_token}'][1].append(1)
                except:
                    bigrams[f'{token} {next_token}'] = [1, [1], []]

                try:
                    bigrams[f'{token} {next_next_token}'] += 1
                    bigrams[f'{token} {next_next_token}'][1].append(2)
                except:
                    bigrams[f'{token} {next_next_token}'] = [1, [2], []]

def compute_mean_and_variance(bigrams):
    for bigram in bigrams:
        # Get offset list and count
        count = bigrams[bigram][0]
        offsets = bigrams[bigram][1]

        # Calculate mean and variance
        mean = (1 / count) * (sum(offsets))

        if count > 1:
            variance = math.sqrt((1 / (count - 1)) * sum([(mean - offset)**2 for offset in offsets]))
            bigrams[bigram][2] = variance
        else:
            bigrams[bigram][2] = 99


def result(bigrams):
    variances = dict()
    for key in bigrams.keys():
        variances[key] = bigrams[key][2]

    v = dict(sorted(variances.items(), key=lambda item: item[1]))

    print(v)

if __name__ == "__main__":
    bigrams = dict()
    extract_bigrams(bigrams)
    compute_mean_and_variance(bigrams)
    result(bigrams)





