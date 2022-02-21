# Kueski_mletc


## About
This application consist of 3 modules: 

###  Module 1: create_features

This module builds a features parquet for the input in the model to be trained. A table that contain all the necessary variables in all the process. 
An example of command line used for launching this module is:

```
python worker.py create_features
```

The create_features.conf file contents should have the following structure:

```
[config]
path_credit_risk_input = resources/dataset_credit_risk.csv
path_features_output = resources/train_model.parquet
stage_name = create_features
```
Replace the values of the parameters according to the actual paths

###  Module 2: model_train

This module trains and persists a Random Forest model using the features generated in the first module.
An example of command line used for launching this module is:
```
python worker.py model_train
```

The model_train.conf file contents should have the following structure:

```
[config]
path_features_input = resources/train_model.parquet
path_model_output = resources/model_risk.joblib
stage_name = model_tain
```
Replace the values of the parameters according to the actual paths


###  Module 3: model_predict

This module exetutes the prediction of the machine learning model trained in the last module. 
An example of command line used for launching this module is:
```
python worker.py model_predict
```

The model_predictt.conf file contents should have the following structure:

```
[config]
path_model_input = resources/model_risk.joblib
path_features_input = resources/train_model.parquet
path_predict_output = resources/predictions.csv
stage_name = model_predict
```
Replace the values of the parameters according to the actual paths


## Configuration
1.- Clone the repository: https://github.com/emmzav/Kueki_MLETC.git

2.- Install all the dependencies and requirements:
```
pip install -r requirements.txt
```

3.- Create a directory and upload into the.csv file that contains the input data

4.- Edit the parameters of the configuration files according to the path to be used.


##Docker


##API
