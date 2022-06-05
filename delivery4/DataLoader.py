import json

class DatasetHandler():
    def __init__(self, path):
        self.sentences, self.tags = [], []
        self.read_data(path)
        self.analyze_data()

    def read_data(self, path):
        with open(path, "r", encoding="UTF-8") as json_file:
            self.dataset = json.load(json_file)
            for item in self.dataset:
                self.tags.append(self.dataset[str(item)][0].lower().strip())
                self.sentences.append(self.dataset[str(item)][1].lower().strip())

    def analyze_data(self):
        self.set_of_tags = list(set(self.tags))

    def read_test_data(self):
        with open("dataset/test_dataset.json", "r", encoding="UTF-8") as test_file:
            self.test_dataset = json.load(test_file)
            self.test_sentences = []
            for sentence in self.test_dataset:
                self.test_sentences.append(self.test_dataset[sentence])

if __name__ == "__main__":
    dh = DatasetHandler("../../EmbeddingWithBilstm/dataset_mahkeme.json")