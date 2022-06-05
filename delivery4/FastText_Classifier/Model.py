import numpy as np
import fasttext.util
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn import metrics
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, plot_confusion_matrix
from sklearn.model_selection import train_test_split
import keras
from keras import layers
from keras.preprocessing.text import Tokenizer
import tensorflow as tf

from delivery4.DataLoader import DatasetHandler


class FastTextClassifier:
    def __init__(self, dataset_handler: DatasetHandler):
        self.data = dataset_handler
        self.prepare_data()
        self.train_test()
        self.cmd_plot()

    def prepare_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data.sentences, self.data.tags,
                                                                                test_size=0.2, random_state=0)
        with open("train.txt", "w", encoding='UTF-8') as train:
            for i in range(len(self.X_train)):
                train.writelines(f"__label__{self.y_train[i].replace(' ', '_')} {self.X_train[i]}\n")

        self.sentences, self.real_tags = [], []
        with open("test.txt", "w", encoding='UTF-8') as test:
            for i in range(len(self.X_test)):
                self.sentences.append(self.X_test[i])
                self.real_tags.append(self.y_test[i])
                test.writelines(f"__label__{self.y_test[i].replace(' ', '_')} {self.X_test[i]}\n")

    def train_test(self):
        self.model = fasttext.train_supervised(input='train.txt', wordNgrams=2, lr=1.0, epoch=1,
                                               bucket=200000, dim=300, loss='hs', pretrainedVectors='../cc.tr.300.vec')

        self.predicted_tags = []
        for sentence in self.sentences:
            self.predicted_tags.append(self.model.predict(sentence)[0][0].replace("__label__", "").replace("_", " "))

        print(self.real_tags[:10])
        print(self.predicted_tags[:10])

        print(classification_report(y_true=self.real_tags, y_pred=self.predicted_tags, zero_division=0))

        with open("FastTextClassifier.txt", "w", encoding='UTF-8') as file:
            file.write(classification_report(y_pred=self.predicted_tags, y_true=self.real_tags, zero_division=False))
        file.close()

    def cmd_plot(self):
        self.onehot_encoder = OneHotEncoder(sparse=False)
        self.real_tags = self.onehot_encoder.fit_transform(np.reshape(self.real_tags, (-1, 1)))
        self.predicted_tags = self.onehot_encoder.fit_transform(np.reshape(self.predicted_tags, (-1, 1)))
        self.y_test = self.onehot_encoder.inverse_transform(self.real_tags)
        self.y_pred = self.onehot_encoder.inverse_transform(self.predicted_tags)
        ConfusionMatrixDisplay.from_predictions(self.y_test, self.y_pred)
        plt.show()

if __name__ == "__main__":
    ftc = FastTextClassifier(DatasetHandler("../dataset_mahkeme.json"))
