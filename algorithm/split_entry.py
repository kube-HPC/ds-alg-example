import time
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from .s3 import S3Session

_input_file: str = None
_s3: S3Session = None
_test_size = None
_random_state = None

BUCKET = 'dstest'
DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 57

################################################################
# algorithm:    titanicsplit-alg
# input:    titanic preprocessed train dataset filename in storage and relevant splitting parameters
# process:  split dataset into train and test, separately for x and y
# output:   storage filenames for x_train, x_test, y_train, y_test
################################################################

def init(args):
    print('titanic_split: init')
    global _input_file, _test_size, _random_state, _s3
    # extract params
    _input = args["input"][0]
    _input_file = _input['df_key']
    _test_size = _input['test_size'] if 'test_size' in _input else DEFAULT_TEST_SIZE
    _random_state = _input['random_state'] if 'random_state' in _input else DEFAULT_RANDOM_STATE

    print(f'input file: {_input_file}, test_size={_test_size}, random_state={_random_state}')
    _s3 = S3Session(BUCKET)

def start(args):
    print('titanic_split: start')
    # time.sleep(5)
    global _input_file, _test_size, _random_state
    global _s3
    # get input
    filename = _s3.download(_input_file)
    df = pd.read_csv(filename, index_col=0)

    # pure alg process
    y = df['Survived']
    x = df.drop(['Survived'], axis=1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=_test_size, random_state=_random_state)

    # prepare output
    output_list = [('x_train', x_train), ('x_test', x_test), ('y_train', y_train), ('y_test', y_test)]
    output_dict = dict()
    for df_info in output_list:
        name = df_info[0] + '.csv'
        odf = df_info[1]
        print(f'{name} -> s3')
        odf.to_csv(name)
        key = _s3.upload(name)
        output_dict[df_info[0]] = name
    print(output_dict)
    
    return output_dict

def stop(args):
    print('titanic_split: stop')


def exit(args):
    print('titanic_split: exit')
    code = args.get('exitCode', 0)
    print('Got exit command. Exiting with code', code)
    sys.exit(code)

