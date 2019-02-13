from ..params_entry import init, start

# TEST
init({'input': [{
    'param_and_range': ['criterion', ['entropy', 'gini']],
    'params': {
        'n_estimators': 10,
        'max_depth': 3
    }
}]})
params_combinations = start({})
print(params_combinations)