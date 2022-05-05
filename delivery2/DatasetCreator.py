
import os
import json
import string

from collections import OrderedDict

FOLDER_NAME = "2021-01"

def read_data():
    # Open folder and read unique .json files
    json_folder_path = os.path.join(FOLDER_NAME)
    json_files = [x for x in os.listdir(json_folder_path) if
                  x.endswith("json") and not (x.__contains__("("))]

    json_data = {}
    for json_file in json_files:
        json_file_path = os.path.join(json_folder_path, json_file)
        with open(json_file_path, "r", encoding="utf-8") as f:
            json_data[json_file] = getText(f)  # {filename : text}

    return json_data

def getText(file):
    js = json.load(file)

    # Determine the key which has the longest content
    max_key = max(js, key=lambda x: len(set(js[x])))
    max_content = js[max_key].split(" ")
    # remove punctuations
    word_list = ""

    for index, word in enumerate(max_content):
        word = word.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
        if len(word) == 0:
            continue
        if index == len(max_content) - 1:
            word_list += word.lower()
        else:
            word_list += f'{word.lower()} '

    return word_list

output = read_data()

# Out the json file
with open("dataset.json", "w",encoding="utf-8") as outfile:
    json.dump(output, outfile, indent=4, ensure_ascii=False)