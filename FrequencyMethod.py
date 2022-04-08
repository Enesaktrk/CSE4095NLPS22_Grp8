import logging
import string

from nltk import FreqDist
from nltk.util import ngrams
from DatasetHandler import DatasetHandler
from zemberek import TurkishMorphology

class FrequencyMethod:
    def __init__(self, dataset_handler: DatasetHandler, n, morphology_mode):
        self.dataset_handler = dataset_handler
        self.n = n

        self.morphology_mode = morphology_mode
        if self.morphology_mode:
            self.data = self.dataset_handler.stemmed_data
        else:
            self.data = self.dataset_handler.data
            self.data = [word.translate(str.maketrans('', '', string.punctuation)) for word in
                         self.data]  # remove punctuation
            self.data = [i for i in self.data if i != '']

        self.frequency_ngram_dist = FreqDist()
        self.most_commons = list()

        self.pos_tagger = TurkishMorphology.create_with_defaults()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f'{self.__class__.__name__} object is initialized.')

    def run(self):
        if self.morphology_mode:
            self.logger.info('Collocations are being extracted by frequency method with using data which is '
                             'preprocessed with morphology analysis.')
            n_grams = ngrams(self.data, self.n)
        else:
            self.logger.info('Collocations are being extracted by frequency method.')
            n_grams = ngrams(self.data, self.n)

        self.frequency_ngram_dist.update(n_grams)

        #self.__convert_to_list()

        self.logger.info('Frequency method has done.')

        return self.most_commons


    def set_morphology_mode(self, morphology_mode):
        if morphology_mode:
            self.data = self.dataset_handler.stemmed_data
        else:
            self.data = self.dataset_handler.data

        self.morphology_mode = morphology_mode

        self.logger.info(f'morphology_mode is set to {self.morphology_mode}')


    def get_pos_tags(self,word):
        r_tags = []
        tags = self.pos_tagger.analyze(word.strip())
        tags_str = str(tags)

        if ":Adj" in tags_str:
            r_tags.append("A")

        if ":Noun" in tags_str:
            r_tags.append("N")

        if len(r_tags) > 0:
            return r_tags[0]
        return ''



