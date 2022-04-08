import logging
import string
import math
from DatasetHandler import DatasetHandler


class MeanAndVarianceMethod:
    def __init__(self, dataset_handler: DatasetHandler, morphology_mode):
        self.dataset_handler = dataset_handler

        self.morphology_mode = morphology_mode
        if self.morphology_mode:
            self.data = self.dataset_handler.stemmed_data
        else:
            self.data = self.dataset_handler.data
            self.data = [word.translate(str.maketrans('', '', string.punctuation)) for word in
                         self.data]  # remove punctuation
            self.data = [i for i in self.data if i != '']

        self.mean_and_variance_bigrams = dict()
        self.most_commons = list()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f'{self.__class__.__name__} object is initialized.')

    def run(self):
        self.logger.info('Mean and variance method is being run.')

        # Extract bigrams
        self.__extract_bigrams()
        self.logger.info('Bigrams are extracted.')

        # Compute mean and variance of each bigram
        self.__compute_mean_and_variance()
        self.logger.info('Mean and variance is computed for each bigram.')

        self.__convert_to_list()

        self.logger.info('Mean and variance method has done.')

        return self.most_commons

    def __extract_bigrams(self):
        for i, token in enumerate(self.data):
            if i < len(self.data) - 1:
                next_token = self.data[i + 1]
            else:
                continue

            if i < len(self.data) - 2:
                next_next_token = self.data[i + 2]
            else:
                continue

            try:
                self.mean_and_variance_bigrams[f'{token} {next_token}'][0] += 1
                self.mean_and_variance_bigrams[f'{token} {next_token}'][1].append(1)
            except:
                self.mean_and_variance_bigrams[f'{token} {next_token}'] = [1, [1], []]

            try:
                self.mean_and_variance_bigrams[f'{token} {next_next_token}'] += 1
                self.mean_and_variance_bigrams[f'{token} {next_next_token}'][1].append(2)
            except:
                self.mean_and_variance_bigrams[f'{token} {next_next_token}'] = [1, [2], []]

    def __compute_mean_and_variance(self):
        for bigram in self.mean_and_variance_bigrams:
            # Get offset list and count
            count = self.mean_and_variance_bigrams[bigram][0]
            offsets = self.mean_and_variance_bigrams[bigram][1]

            # Calculate mean and variance
            mean = (1 / count) * (sum(offsets))

            if count > 1:
                variance = math.sqrt((1 / (count - 1)) * sum([(mean - offset) ** 2 for offset in offsets]))
                self.mean_and_variance_bigrams[bigram][2] = variance
            else:
                # If bigram is only occurs once, variance is meaningless
                self.mean_and_variance_bigrams[bigram][2] = float('inf')

        # Sort bigrams with respect to their variances in ascending order
        self.mean_and_variance_bigrams = sorted(self.mean_and_variance_bigrams.items(),
                                                key=lambda kv: (kv[1][2], -kv[1][0]))

    def set_morphology_mode(self, morphology_mode):
        if morphology_mode:
            self.bigrams = self.dataset_handler.stemmed_data
        else:
            self.bigrams = self.dataset_handler.data

        self.morphology_mode = morphology_mode

        self.logger.info(f'morphology_mode is set to {self.morphology_mode}')
