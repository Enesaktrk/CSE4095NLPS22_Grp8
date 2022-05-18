import numpy as np
import fasttext.util
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
import keras
from keras import layers
from keras.preprocessing.text import Tokenizer
import tensorflow as tf

from DataLoader import DatasetHandler

# region FastText PARAMETERS
MAX_NB_WORDS = 100000
MAX_SEQ_LEN = 300
#training params
BATCH_SIZE = 256
NUM_EPOCHS = 30
#model parameters
EMBED_DIM_FASTTEXT = 300
EMBED_DIM_BERT = 768
WEIGHT_DECAY = 1e-4
# endregion

class Model:
    def __init__(self, dataset_handler: DatasetHandler):
        self.data = dataset_handler
        self.data_preparation()
        # fasttext.util.download_model('tr', if_exists='ignore')
        self.tokenizer = Tokenizer(num_words=MAX_NB_WORDS, lower=True, char_level=False)
        self.ft = fasttext.load_model("cc.tr.300.bin")
        self.create_embedding_matrix()
        self.create_model()
        self.train()
        self.cmd_plot()
        self.print_cfr()

    def data_preparation(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data.sentences, self.data.tags,
                                                                                test_size=0.2, random_state=0)
        self.label_names = self.data.set_of_tags
        self.num_classes = len(self.label_names)
        print(f"Labels : {self.label_names}")
        self.tokenizer.fit_on_texts(self.X_train)

        self.word_train = self.tokenizer.texts_to_sequences(self.X_train)
        self.word_test = self.tokenizer.texts_to_sequences(self.X_test)

        self.onehot_encoder = OneHotEncoder(sparse=False)

        self.word_index = self.tokenizer.word_index

        self.X_train = tf.keras.preprocessing.sequence.pad_sequences(self.word_train, maxlen=MAX_SEQ_LEN)
        self.X_test = tf.keras.preprocessing.sequence.pad_sequences(self.word_test, maxlen=MAX_SEQ_LEN)

        self.y_train = self.onehot_encoder.fit_transform(np.reshape(self.y_train, (-1, 1)))
        self.y_test = self.onehot_encoder.fit_transform(np.reshape(self.y_test, (-1, 1)))

    def create_embedding_matrix(self):
        # embedding matrix
        print('preparing embedding matrix...')

        self.embeddings_index = {}
        self.words_not_found = []
        self.nb_words = min(MAX_NB_WORDS, len(self.word_index))
        self.fasttext_embedding_matrix = np.zeros((self.nb_words+1, EMBED_DIM_FASTTEXT))
        for word, i in self.word_index.items():
            if i >= self.nb_words:
                continue
            embedding_vector = self.ft[word]
            if (embedding_vector is not None) and len(embedding_vector) > 0:
                # words not found in embedding index will be all-zeros.
                self.fasttext_embedding_matrix[i] = embedding_vector
            else:
                self.words_not_found.append(word)
        print('number of null word embeddings: %d' % np.sum(np.sum(self.fasttext_embedding_matrix, axis=1) == 0))

    def create_model(self):
        # Input for variable-length sequences of integers
        self.inputs = keras.Input(shape=(None,), dtype="int32")
        # Embed each integer in a 128-dimensional vector
        self.model = layers.Embedding(self.nb_words+1, EMBED_DIM_FASTTEXT, weights=[self.fasttext_embedding_matrix], input_length=MAX_SEQ_LEN,trainable=False)(self.inputs)
        # Add 2 bidirectional LSTMs
        self.model = layers.Bidirectional(layers.LSTM(64, return_sequences=True))(self.model)
        self.model = layers.Bidirectional(layers.LSTM(64))(self.model)
        # Add a classifier
        self.outputs = layers.Dense(self.num_classes, activation="sigmoid")(self.model)
        self.model = keras.Model(self.inputs, self.outputs)
        self.model.summary()

    def train(self):
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.hist = self.model.fit(self.X_train, self.y_train, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS,
                         shuffle=True, verbose=1)
        self.y_pred = self.model.predict(self.X_test)

    def cmd_plot(self):
        self.y_test = self.onehot_encoder.inverse_transform(self.y_test)
        self.y_pred = self.onehot_encoder.inverse_transform(self.y_pred)
        ConfusionMatrixDisplay.from_predictions(self.y_test, self.y_pred)
        plt.show()

    def print_cfr(self):
        print(classification_report(self.y_test, self.y_pred))

if __name__ == "__main__":
    model = Model(DatasetHandler())