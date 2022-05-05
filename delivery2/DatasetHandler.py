import json

class DatasetHandler():
    def __init__(self):
        self.read_data()
        self.read_test_data()

    def read_data(self):
        with open("dataset/dataset.json", "r", encoding="UTF-8") as json_file:
            self.dataset = json.load(json_file)
            self.sentences = []
            self.tags = []
            for item in self.dataset:
                self.tags.append(self.dataset[str(item)][0].lower().strip())
                self.sentences.append(self.dataset[str(item)][1].lower().strip())

    def read_test_data(self):
        with open("dataset/test_dataset.json", "r", encoding="UTF-8") as test_file:
            self.test_dataset = json.load(test_file)
            self.test_sentences = []
            for sentence in self.test_dataset:
                self.test_sentences.append(self.test_dataset[sentence])