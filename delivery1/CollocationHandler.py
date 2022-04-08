import logging
from DatasetHandler import DatasetHandler
from TTestMethod import TTestMethod
from MeanAndVarianceMethod import MeanAndVarianceMethod
from FrequencyMethod import FrequencyMethod


class CollocationHandler:
    def __init__(self, dataset_handler: DatasetHandler, morphology_mode, n):
        self.frequency_method = FrequencyMethod(dataset_handler, n, morphology_mode)
        self.mean_and_variance_method = MeanAndVarianceMethod(dataset_handler, morphology_mode)
        self.t_test = TTestMethod(dataset_handler, morphology_mode)

        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.logger.info(f'{self.__class__.__name__} is initialized.')








