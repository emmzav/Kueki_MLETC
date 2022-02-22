# Kueski_mletc


## About
This application consist of 3 modules and API: 

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

This module executes the prediction of the machine learning model trained in the last module. 
An example of command line used for launching this module is:
```
python worker.py model_predict
```

The model_predict.conf file contents should have the following structure:

```
[config]
path_model_input = resources/model_risk.joblib
path_features_input = resources/train_model.parquet
path_predict_output = resources/predictions.csv
stage_name = model_predict
```
Replace the values of the parameters according to the actual paths


###  Flask API: api

**WARNING**: It is necessary to execute before the modules: *create_features* and *model_predict*

Flask API with to functions:
a) Get the information of a specific client
b) Get the prediction of a specific client

Steps:
1.- Execute the command:
```
python worker.py api
```

2.- Open abother terminal, you can choose between:
    2.1.- Open Jupyter-Lab and open the notebook: API_notebook.ipynb
    3.- Execute the following steps:
```
import requests

client_id = <id_client>
#Example: client_id = 5009033

url = '<URL_fask>:<port>/'
#Example: url = 'http://127.0.0.1:5000/'

#Get information of a client
requests.post(url+'get_cient_info', json=client_id).json()

#Get prediction of a client
requests.post(url+'model_predict', json=client_id).json()
```

The api.conf file contents should have the following structure:

```
[config]
path_features_input = resources/train_model.parquet
path_model_input = resources/model_risk.joblib
stage_name = api
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


## Docker

You can also execute this project using Docker.

Follow the next steps:

1.- Build image
```
 docker build -t <image_name> .
```

2.- Run container using the stage that you want to execute
```
docker run  -p 5000:5000 -v $(pwd):/app kueski_ubuntu create features
docker run  -p 5000:5000 -v $(pwd):/app kueski_ubuntu model_train
docker run  -p 5000:5000 -v $(pwd):/app kueski_ubuntu model_predict
docker run  -p 5000:5000 -v $(pwd):/app kueski_ubuntu api
```
You also can run an interactive container, and in its terminal, you can execute the python3 worker.py <phase> command:
```
docker run  -p 5000:5000 -v $(pwd):/app -it --entrypoint /bin/bash kueski_ubuntu 
```

There is also the possibility to run all the stages using docker-compose:
```
docker-compose run task <phase_name>
```