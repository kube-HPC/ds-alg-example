import time
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

_input_file: str = None
_param_and_range = None
_params = None

################################################################
# algorithm:    titanicparams-alg
# input:    one model param with values list (param_and_range) and all rest params as a dict (params)
# process:  create list of params combinations (as dict) for batch of model training
# output:   list of dicts, each dict is model parameters in key/value style
################################################################


def init(args):
    print('titanic_params: init')
    global _param_and_range, _params
    # extract params
    _input = args["input"][0]
    _param_and_range = _input['param_and_range']
    _params = _input['params']

    print(f'param_and_range: {_param_and_range}, params={_params}')

def start(args):
    print('titanic_params: start')
    # time.sleep(5)
    global _param_and_range, _params

    # pure alg process
    key = _param_and_range[0]
    range = _param_and_range[1]
    params_combinations = list()
    for value in range:
        combination = dict(_params)
        combination[key] = value
        params_combinations.append(combination)
    print(f'params_combinations: {params_combinations}')


    return params_combinations

def stop(args):
    print('titanic_params: stop')


def exit(args):
    print('titanic_params: exit')
    code = args.get('exitCode', 0)
    print('Got exit command. Exiting with code', code)
    sys.exit(code)

