import os
import string
import json

from zemberek import TurkishMorphology


def pre_labels():
    # Perform morphology analysis to final labels
    morphology = TurkishMorphology.create_with_defaults()
    class_labels = dict()

    with open('final_labels.txt', 'r') as labels:
        lines = labels.readlines()
        for line in lines:
            # Remove punctuations and \n characters
            line = line.strip('\n').lower()
            new_line = line.translate(str.maketrans('', '', string.punctuation))
            words = new_line.split(' ')

            for word in words:
                if word == '':
                    continue
                analyze_result = morphology.analyze(word)
                try:
                    stemmed_word = analyze_result.analysis_results[0].item.root
                except:
                    stemmed_word = word

                # Add stemmed word to the dictionary
                try:
                    class_labels[line].append(stemmed_word)
                except:
                    class_labels[line] = list()
                    class_labels[line].append(stemmed_word)

    # Perform morphology analysis to crimes list
    crimes_dict = dict()
    with open('crimes_sorted.json', 'r') as json_file:
        crimes = json.load(json_file)

        for crime in crimes:
            # Remove punctuations
            new_crime = crime.translate(str.maketrans('', '', string.punctuation))

            words = new_crime.split(' ')
            for word in words:
                if word == '':
                    continue
                analyze_result = morphology.analyze(word)
                try:
                    stemmed_word = analyze_result.analysis_results[0].item.root
                except:
                    stemmed_word = word

                # Add stemmed word to the dictionary
                try:
                    crimes_dict[crime][0].append(stemmed_word)
                except:
                    crimes_dict[crime] = [[], [], 0, 0, 'final label']
                    crimes_dict[crime][0].append(stemmed_word)

    # Compare class labels and crimes list, compute similarity matrix
    for crime in crimes_dict:
        for label in class_labels:
            similarity_score = 0
            for crime_word in crimes_dict[crime][0]:
                for label_word in class_labels[label]:
                    if crime_word in label_word:
                        similarity_score += 1
            similarity_score = similarity_score / len(crimes_dict[crime][0])
            crimes_dict[crime][1].append(similarity_score)

    # Update max index in crimes dict
    for crime in crimes_dict:
        max_value = max(crimes_dict[crime][1])
        max_index = crimes_dict[crime][1].index(max_value)
        crimes_dict[crime][2] = max_value
        crimes_dict[crime][3] = max_index

    # Assign final labels to crimes
    for index, label in enumerate(class_labels):
        for crime in crimes_dict:
            if crimes_dict[crime][2] == 0:
                crimes_dict[crime][4] = 'other'
            elif crimes_dict[crime][3] == index:
                crimes_dict[crime][4] = label

    # Crate dict for pre final labels
    labels = dict()
    for crime in crimes_dict:
        labels[crime] = crimes_dict[crime][4]

    # Out the json file
    with open("pre_final_labels.json", "w") as outfile:
        json.dump(labels, outfile, indent=4, ensure_ascii=False)


def read_data():
    # Open folder and read unique .json files
    json_folder_path = os.path.join("2021-01")
    json_files = [x for x in os.listdir(json_folder_path) if
                  x.endswith("json") and not (x.__contains__("("))]

    # Dump .json files
    json_data = list()
    for json_file in json_files:
        json_file_path = os.path.join(json_folder_path, json_file)
        with open(json_file_path, "r", encoding="utf-8") as f:
            json_data.append(json.load(f))

    # Append data
    data = dict()
    index_count = 0
    for js in json_data:
        # Get crime label from document
        crime_label = js['Suç']
        crime_label = crime_label.lower()
        punc_index = crime_label.find(',')
        if punc_index != -1:
            crime_label = crime_label[:punc_index]

        if crime_label == "":
            crime_label = "undefined"

        # Determine the key which has longest content
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

        data[index_count] = [crime_label.strip(), word_list]
        print(f'{index_count} has finished.')
        index_count += 1

    return data


def assign_final_labels(raw_dict):
    with open('top15_labels_son.json') as json_file:
        labels = json.load(json_file)

    output = dict()
    for index in raw_dict:
        if raw_dict[index][0] == 'undefined':
            final_label = 'undefined'
        else:
            final_label = labels[raw_dict[index][0]]
        output[index] = [final_label, raw_dict[index][1]]

    return output


def top15_labels():
    with open('top15_labels.json') as json_file:
        labels = json.load(json_file)

    with open('pre_final_labels copy.json') as json_file:
        old_labels = json.load(json_file)

    for old_label in old_labels:
        for label in labels:
            for label_value in labels[label]:
                if label_value == old_labels[old_label]:
                    old_labels[old_label] = label
                    break

        # Out the json file
        with open("top15_labels_son.json", "w") as outfile:
            json.dump(old_labels, outfile, indent=4, ensure_ascii=False)


raw_dict = read_data()
output = assign_final_labels(raw_dict)

# Out the json file
with open("dataset.json", "w") as outfile:
    json.dump(output, outfile, indent=4, ensure_ascii=False)
