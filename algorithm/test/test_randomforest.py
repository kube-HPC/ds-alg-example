from ..randomforest_entry import init, start

# TEST
init({'input': [{
    'params_combinations': {
        'criterion': 'entropy',
        'n_estimators': 10,
        'max_depth': 3
    },
    'x_train': 'x_train.csv',
    'y_train': 'y_train.csv',
    'x_test': 'x_test.csv',
    'y_test': 'y_test.csv',
}]})
metrics = start({})
print(metrics)