import json
import os
import string
from zemberek import TurkishMorphology
import logging


class DatasetHandler:
    def __init__(self, dataset_path):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        logging.info(f'{self.__class__.__name__} is initialized.')

        self.dataset_path = dataset_path
        self.json_files = list()
        self.json_data = list()

        try:
            with open('corpus.txt', 'r', encoding="utf-8") as corpus:
                self.data = corpus.read()
                self.data = self.data.split(' ')
            self.logger.info('corpus.txt found, data loaded.')
        except:
            self.logger.info('corpus.txt not found, data is reading.')
            self.data = ''
            self.read_data()
            self.logger.info('data is read.')

        try:
            with open('stemmed_data.txt', 'r', encoding="utf-8") as data:
                self.stemmed_data = data.read()
                self.stemmed_data = self.stemmed_data.split(' ')
            self.logger.info('stemmed_data.txt found, stemmed data loaded.')
        except:
            self.logger.info('stemmed_data.txt not found, stemmed data is reading.')
            self.stemmed_data = list()
            self.tokenize_data_stemmed()
            self.logger.info('Stemmed data is read.')

    def read_data(self):
        # Open folder and read unique .json files
        json_folder_path = os.path.join(self.dataset_path)
        self.json_files = [x for x in os.listdir(json_folder_path) if
                           x.endswith("json") and not (x.__contains__("("))]

        # Dump .json files
        for json_file in self.json_files:
            json_file_path = os.path.join(json_folder_path, json_file)
            with open(json_file_path, "r", encoding="utf-8") as f:
                self.json_data.append(json.load(f))

        # Append data
        for js in self.json_data:
            # Determine the key which has longest content
            max_key = max(js, key=lambda x: len(set(js[x])))
            for word in js:
                word = word.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
                if len(word) == 0:
                    continue
                self.data.append(js[max_key])

    def save_data(self):
        self.logger.info('data is saving into corpus.txt.')
        with open("corpus.txt", "w", encoding="utf-8") as outfile:
            for tt in self.data:
                outfile.write(str(str.lower(tt)))
        outfile.close()
        self.logger.info('corpus.txt created.')

    def tokenize_data_stemmed(self):
        # Create morphology object
        morphology = TurkishMorphology.create_with_defaults()

        # Tokenize data
        self.logger.info('words are tokenizing.')
        words = self.data.split(' ')

        for word in words:
            word = word.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
            if len(word) == 0:
                continue

            try:
                analysis_results = morphology.analyze(word).analysis_results
                if len(analysis_results) != 0:
                    word = analysis_results[0].item.root
            except:
                continue
            print(word, 'tokenized.')
            self.stemmed_data.append(f'{word} ')

        self.logger.info('words are tokenized.')

    def save_tokenized_data_stemmed(self):
        self.logger.info('Stemmed data is saving into stemmed_data.txt.')
        with open("stemmed_data.txt", "w", encoding="utf-8") as outfile:
            for tt in self.stemmed_data:
                outfile.write(str(str.lower(tt)))
        outfile.close()
        self.logger.info('stemmed_data.txt created.')
