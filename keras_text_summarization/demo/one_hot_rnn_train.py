from __future__ import print_function

import pandas as pd
from sklearn.model_selection import train_test_split
from keras_text_summarization.utility.plot_utils import plot_and_save_history
from keras_text_summarization.library.rnn import OneShotRNN
from keras_text_summarization.utility.fake_news_loader import fit_text
import numpy as np

LOAD_EXISTING_WEIGHTS = False


def main():
    np.random.seed(42)
    data_dir_path = './data'
    report_dir_path = './reports'
    model_dir_path = './models'

    print('loading csv file ...')
    df = pd.read_csv(data_dir_path + "/fake_or_real_news.csv")

    print('extract configuration from input texts ...')
    # df = df.loc[df.index < 1000]
    Y = df.title
    X = df['text']
    config = fit_text(X, Y)

    print('configuration extracted from input texts ...')

    summarizer = OneShotRNN(config)

    if LOAD_EXISTING_WEIGHTS:
        weight_file_path = OneShotRNN.get_weight_file_path(model_dir_path=model_dir_path)
        summarizer.load_weights(weight_file_path=weight_file_path)

    Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.2, random_state=42)

    print('training size: ', len(Xtrain))
    print('testing size: ', len(Xtest))

    print('start fitting ...')
    history = summarizer.fit(Xtrain, Ytrain, Xtest, Ytest, epochs=100, batch_size=20)

    history_plot_file_path = report_dir_path + '/' + OneShotRNN.model_name + '-history.png'
    if LOAD_EXISTING_WEIGHTS:
        history_plot_file_path = report_dir_path + '/' + OneShotRNN.model_name + '-history-v' + str(summarizer.version) + '.png'
    plot_and_save_history(history, summarizer.model_name, history_plot_file_path, metrics={'loss', 'acc'})


if __name__ == '__main__':
    main()