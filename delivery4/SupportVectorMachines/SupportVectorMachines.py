from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import *
from sklearn.pipeline import make_pipeline
from delivery4.DataLoader import DatasetHandler
import matplotlib.pyplot as plt

class SupportVectorMachines:
    def __init__(self, dataset_handler: DatasetHandler, isTrue):
        self.data = dataset_handler
        if isTrue:
            self.train()
            self.test()

    def train(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data.sentences, self.data.tags,
                                                                                test_size=0.2, random_state=0)
        self.model = make_pipeline(TfidfVectorizer(), LinearSVC())
        self.model.fit(self.X_train, self.y_train)

    def test(self):
        self.pred = self.model.predict(self.X_test)

        with open("LinearSVC.txt", "w", encoding='UTF-8') as file:
            file.write(classification_report(y_pred=self.pred, y_true=self.y_test, zero_division=False))
        file.close()

        plot_confusion_matrix(self.model, self.X_test, y_true=self.y_test, xticks_rotation='vertical')
        plt.show()

if __name__ == "__main__":
    svc = SupportVectorMachines(DatasetHandler("../dataset_mahkeme.json"), True)