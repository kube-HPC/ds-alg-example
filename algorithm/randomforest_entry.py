import time
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from .s3 import S3Session
from .consts import BUCKET

_input_file: str = None
_s3: S3Session = None
_x_train = None
_x_test = None
_y_train = None
_y_test = None

################################################################
# algorithm:    titanicrf-alg
# input:    x_train, x_test, y_train, y_test datasets filenames in storage and model params dict
# process:  create RandomForest classifier, fit on train part and evaluate on test part
# output:   model params dict (modelParams) and model metrics: accuricy, f1, precision, recall
################################################################


def init(args):
    print('titanic_rf: init')
    global _params_combinations, _x_train, _x_test, _y_train, _y_test, _s3
    # extract params TODO
    _input = args["input"][0]
    _params_combinations = _input['params_combinations']
    _x_train = _input['x_train']
    _x_test = _input['x_test']
    _y_train = _input['y_train']
    _y_test = _input['y_test']

    print(f'params_combinations: {_params_combinations}')
    print(f'x_train: {_x_train}, x_test={_x_test}, y_train={_y_train}, y_test={_y_test}')
    _s3 = S3Session(BUCKET)

def start(args):
    print('titanic_rf: start')
    # time.sleep(5)
    global _params_combinations, _x_train, _x_test, _y_train, _y_test, _s3

    # read DFs
    try:
        x_train_file = _s3.download(_x_train)
        x_train_df = pd.read_csv(x_train_file, index_col=0)
        y_train_file = _s3.download(_y_train)
        y_train_df = pd.read_csv(y_train_file, header=None, squeeze=True, index_col=0)
        x_test_file = _s3.download(_x_test)
        x_test_df = pd.read_csv(x_test_file, index_col=0)
        y_test_file = _s3.download(_y_test)
        y_test_df = pd.read_csv(y_test_file, header=None, squeeze=True, index_col=0)
    except Exception as error:
        raise Exception(f'Error during download DFs: {error.__str__()}')

    y_train_df = y_train_df.astype('category')
    y_test_df = y_test_df.astype('category')

    # pure alg process: train model and evaluate it
    try:
        clf = RandomForestClassifier(**_params_combinations)
        clf.fit(x_train_df, y_train_df)
    except Exception as error:
        raise Exception(f'Error during model creation/fit: {error.__str__()}')

    accuricy = None
    f1 = None
    precision = None
    recall = None
    try:
        y_predict_df = clf.predict(x_test_df)
        accuricy = accuracy_score(y_test_df, y_predict_df)
        f1 = f1_score(y_test_df, y_predict_df)
        precision = precision_score(y_test_df, y_predict_df)
        recall = recall_score(y_test_df, y_predict_df)
    except Exception as error:
        raise Exception(f'Error during model evaluation: {error.__str__()}')

    # prepare output
    output = {
        'modelParams': _params_combinations,
        'accuricy': accuricy,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }
    return output

def stop(args):
    print('titanic_rf: stop')


def exit(args):
    print('titanic_rf: exit')
    code = args.get('exitCode', 0)
    print('Got exit command. Exiting with code', code)
    sys.exit(code)
