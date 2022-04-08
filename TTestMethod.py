import logging
import math
import string
from nltk import FreqDist
from nltk.util import ngrams
from DatasetHandler import DatasetHandler


class TTestMethod:
    def __init__(self, dataset_handler: DatasetHandler, morphology_mode):
        self.dataset_handler = dataset_handler
        self.morphology_mode = morphology_mode

        if self.morphology_mode:
            self.data = dataset_handler.stemmed_data
        else:
            self.data = dataset_handler.data
            self.data = [word.translate(str.maketrans('', '', string.punctuation)) for word in
                         self.data]  # remove punctuation
            self.data = [i for i in self.data if i != '']

        self.bigrams = dict()
        self.unigram_freq_dist = FreqDist()
        self.t_values = dict()
        self.rejected_hypothesis = dict()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f'{self.__class__.__name__} object is initialized.')

    def run(self):
        self.logger.info('T test is being run.')

        # Extract word frequencies
        self.__extract_word_frequencies()
        self.logger.info('Word frequencies are extracted.')

        # Extract bigrams
        self.__extract_bigrams()
        self.logger.info('Bigrams are extracted.')

        # Compute mean of each bigram
        self.__compute_mean()
        self.logger.info('Means are calculated.')

        # Calculate t-values
        self.__calculate_t()
        self.logger.info('T values are calculated.')

        # Check null hypothesis
        self.__check_null_hypothesis(2.576)
        self.logger.info('Null hypothesis are checked.')

        self.logger.info('T test has done.')
        return self.rejected_hypothesis[:19]

    def __extract_word_frequencies(self):
        unigrams = ngrams(self.data, 1)
        self.unigram_freq_dist.update(unigrams)

    def __extract_bigrams(self):
        for i, token in enumerate(self.data):
            if i < len(self.data) - 1:
                next_token = self.data[i + 1]
            else:
                continue

            try:
                self.bigrams[f'{token} {next_token}'][0] += 1
            except:
                self.bigrams[f'{token} {next_token}'] = [1, 0]

    def __compute_mean(self):
        # Compute mean of each bigram
        for bigram in self.bigrams.keys():
            count = self.bigrams[bigram][0]
            self.bigrams[bigram][1] = count / self.unigram_freq_dist.N()

    def __calculate_t(self):
        n = self.unigram_freq_dist.N()
        for key in self.bigrams.keys():
            bigram_string = key.split(' ')
            w1 = bigram_string[0]
            w2 = bigram_string[1]
            w1_freq = self.unigram_freq_dist.get((w1,))
            w2_freq = self.unigram_freq_dist.get((w2,))

            t_value = (self.bigrams[key][1] - ((w1_freq / n) * (w2_freq / n))) / math.sqrt((self.bigrams[key][1] / n))
            self.t_values[key] = t_value

    def __check_null_hypothesis(self, critical_value):
        # Check hypothesis
        for t_value in self.t_values:
            if self.t_values[t_value] > critical_value:
                self.rejected_hypothesis[t_value] = self.t_values[t_value]

        # Sort rejected bigram hypothesis in descending order
        self.rejected_hypothesis = sorted(self.rejected_hypothesis.items(), key=lambda kv: kv[1], reverse=True)

    def set_morphology_mode(self, morphology_mode):
        if morphology_mode:
            self.bigrams = self.dataset_handler.stemmed_data
        else:
            self.bigrams = self.dataset_handler.data

        self.morphology_mode = morphology_mode

        self.logger.info(f'morphology_mode is set to {self.morphology_mode}')
