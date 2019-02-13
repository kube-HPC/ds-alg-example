import time
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from .s3 import S3Session
from .consts import BUCKET

_input_file: str = None
_s3: S3Session = None
_models_results = None

################################################################
# algorithm:    titanicbestmodel-alg
# input:    storage train dataset filename (df_key) and a list of models params & metrics
# process:  create RandomForest model for the best one according to metrics, fit whole dataset and dump the model
# output:   best model dump filename in storage
################################################################

def init(args):
    print('titanic_bestmodel: init')
    global _input_file, _models_results, _s3
    # extract params
    _input = args["input"][0]
    _input_file = _input['df_key']
    _models_results = _input['models_results']
    print(f'input_file: {_input_file}')
    print(f'models_results: {_models_results}')
    _s3 = S3Session(BUCKET)

def calculate_score(accuricy, f1, precision, recall):
    # implement here by average
    return (accuricy + f1 + precision + recall)/4

def start(args):
    print('titanic_bestmodel: start')
    # time.sleep(5)
    global _input_file, _models_results, _s3

    # read DFs
    try:
        df_file = _s3.download(_input_file)
        df = pd.read_csv(df_file, index_col=0)
    except Exception as error:
        raise Exception(f'Error during download DFs: {error.__str__()}')

    # find best model by models training metrics
    best_params = None
    best_score = 0
    for model_result in _models_results:
        print(f'Model: {model_result}')
        accuricy = model_result['accuricy']
        f1 = model_result['f1']
        precision = model_result['precision']
        recall = model_result['recall']
        score = calculate_score(accuricy, f1, precision, recall)
        if score > best_score:
            best_score = score
            best_params = model_result['modelParams']

    print(f'Best score: {best_score} for modelParams: {best_params}')

    # build best RF model
    try:
        y = df['Survived']
        x = df.drop(['Survived'], axis=1)
        clf = RandomForestClassifier(**best_params)
        clf.fit(x, y)
    except Exception as error:
        raise Exception(f'Error during model creation/fit: {error.__str__()}')

    # serialize best model
    timestr = time.strftime('%d-%m-%Y_%H-%M-%S', time.gmtime())
    modelfile = f'randomforest-{timestr}.pkl.z'
    try:
        joblib.dump(clf, modelfile)
    except Exception as error:
        raise Exception(f'Error during model dump: {error.__str__()}')

    model_key = None
    try:
        model_key = _s3.upload(modelfile)
    except Exception as error:
        raise Exception(f'Error during model S3 upload: {error.__str__()}')

    # prepare output
    output = {
        'modelKey': model_key
    }
    return output

def stop(args):
    print('titanic_bestmodel: stop')


def exit(args):
    print('titanic_bestmodel: exit')
    code = args.get('exitCode', 0)
    print('Got exit command. Exiting with code', code)
    sys.exit(code)
