# ds-example - Data Sciense Example Algorithms for Hkube
This python3 project is an example for Data Sciense related algorithms for hkube.
Algorithms are meants to work on titanic dataset. 
They should be combined in an hkube pipeline for having the whole process on the titanic dataset with a predicting model as a result.
It contains 5 algorithms, each has its own entry script:
- **preprocess_entry.py:** titanic preprocess dataset
- **split_entry.py:** split dataset into train and test, separately for x and y
- **params_entry.py:** prepare a list of model parameters combination, aimed for batch processing
- **randomforest_entry.py:** train and evaluate a RandomForest model on dataset (built to work in batch)
- **bestmodel_entry.py:** build the best model from prev. batch, fit whole dataset and dump the model as output.

Algorithms use S3 storage to store input and output datasets, models, etc. (algorithm input may be a key for a file in the storage). You can set env variables for storage parameters.
You should use **hkube_notebook** python3 library and pass algorithm folder to define the algorithm in hkube and build its docker image.
I've made a single python project for all 5, but in practice you've better create a different project for each algorithm.
# Algorithm Notes
- Algorithm entry script should include implementations of the API functions (at least **init** and **start**)
- You should create an up-to-date requirements.txt file:
```sh
pip3 freeze > algorithm/requirements.txt
```
- Pass algorithm root path to **AlgorithmManager.create_algfile_by_folder()**, in this case: **<location>/ds-alg-example/algorithm**
