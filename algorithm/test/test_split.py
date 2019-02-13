from ..split_entry import init, start

# TEST
init({'input': [{
    'df_key': 'train_pp.csv',
    'test_size': 0.2,
    # 'random_state': 46
}]})
key_list = start({})
print(key_list)