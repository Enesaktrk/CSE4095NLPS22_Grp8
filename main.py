from DatasetHandler import DatasetHandler
from CollocationHandler import CollocationHandler
import matplotlib.pyplot as plt


def plot_frequency_result(results):
    plt.figure(figsize=(15, 10))
    plt.barh([item[0] for item in results], [item[1] for item in results])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Frequency')
    plt.ylabel('Top 20')
    plt.savefig('plots/frequency_method_stemmed.png')
    plt.show()


def plot_mean_and_variance_result(results):
    plt.figure(figsize=(15, 10))
    plt.barh([item[0] for item in results], [item[1] for item in results])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Frequency')
    plt.ylabel('Top 20')
    plt.savefig('plots/mean_and_variance_method_stemmed.png')
    plt.show()


def plot_ttest_result(results):
    plt.figure(figsize=(15, 10))
    plt.barh([item[0] for item in results], [item[1] for item in results])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('T Scores')
    plt.ylabel('Top 20')
    plt.savefig('plots/ttest_method_stemmed.png')
    plt.show()


dataset_handler = DatasetHandler(dataset_path='dataset')
collocation_handler = CollocationHandler(dataset_handler, morphology_mode=True, n=2)
collocations_frequency = collocation_handler.frequency_method.run()
collocations_mean_and_variance = collocation_handler.mean_and_variance_method.run()
collocations_ttest = collocation_handler.t_test.run()

plot_frequency_result(collocations_frequency)
plot_mean_and_variance_result(collocations_mean_and_variance)
plot_ttest_result(collocations_ttest)