from ..bestmodel_entry import init, start

# TEST
init({'input': [{
    'models_results': [
        {
            'modelParams': { 'criterion': 'entropy', 'n_estimators': 10, 'max_depth': 3 },
            'accuricy': 0.7,
            'f1': 0.8,
            'precision': 0.9,
            'recall': 0.8
        },
        {
            'modelParams': { 'criterion': 'gini', 'n_estimators': 10, 'max_depth': 3 },
            'accuricy': 0.75,
            'f1': 0.8,
            'precision': 0.9,
            'recall': 0.79
        },
    ],
    'df_key': 'train_pp.csv',
}]})
metrics = start({})
print(metrics)