import time
import sys
import pandas as pd
import numpy as np
from .s3 import S3Session
from .consts import BUCKET

_input_file: str = None
_s3: S3Session = None

################################################################
# algorithm:    titanicpp-alg
# input:    titanic train dataset filename in storage
# process:  pre-process dataset to fit it to model training
# output:   titanic pre-processed train filename in storage
################################################################


def init(args):
    print('titanic_pp: init')
    global _input_file
    global _s3
    # extract params
    _input = args["input"]
    _input_file = _input[0]
    print(f'input file: {_input_file}')
    _s3 = S3Session(BUCKET)

def start(args):
    print('titanic_pp: start')
    # time.sleep(5)
    global _input_file
    global _s3
    # get input
    filename = _s3.download(_input_file)
    df = pd.read_csv(filename)

    # pure alg process
    df.dropna(inplace=True, subset=['PassengerId', 'Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked'])
    df.drop(['Name', 'Ticket', 'Cabin'], axis=1, inplace=True)
    df['Survived'].astype('category')
    df['Sex'] = df['Sex'].map({'female': 1, 'male': 0})
    df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2}).astype(int)
    print(f'Shape: {df.shape}')

    # prepare output
    _output_file = _input_file[0:-4] + '_pp.csv'
    print(f'output file: {_output_file}')
    df.to_csv(_output_file)
    key = _s3.upload(_output_file)
    return { "df_key": key }

def stop(args):
    print('titanic_pp: stop')


def exit(args):
    print('titanic_pp: exit')
    code = args.get('exitCode', 0)
    print('Got exit command. Exiting with code', code)
    sys.exit(code)

