from nltk.tokenize import word_tokenize
import json
import os
from nltk import FreqDist
from nltk.util import ngrams


def compute_freq():
    textfile = open('corpus.txt', 'r', encoding="utf-8")

    bigramfdist = FreqDist()
    threeramfdist = FreqDist()

    for line in textfile:
        if len(line) > 1:
            tokens = line.strip().split(' ')

            bigrams = ngrams(tokens, 2)
            bigramfdist.update(bigrams)

    return bigramfdist.most_common()

    # with open("all_out.txt", "w", encoding="utf-8") as outfile:
    #     outfile.write(str(bigramfdist.most_common()))
    # outfile.close()


def tokenize(all_json):
    tokenized_list = []
    for word in all_json:
        tokenized = word_tokenize(word)
        tokenized_list.append(tokenized)

    return tokenized_list


def read():
    json_folder_path = os.path.join("2021-01")
    json_files = [x for x in os.listdir(json_folder_path) if
                  x.endswith("json") and not (x.__contains__("("))]  # tekrarlayan dosya kontrolu
    json_data = list()
    for json_file in json_files:
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


if __name__ == "__main__":
    json_data = read()
    tokenized_list = tokenize(json_data)
    #compute_freq()
