import pandas as pd
from configparser import ConfigParser
from flask import Flask, request, jsonify
from Kueski_mletc.model_predict.model_loader import read_model
from Kueski_mletc.model_train.dataloader_features import DataLoaderFeatures


app = Flask(__name__)


@app.route('/get_cient_info', methods=["POST"])
def get_client_info():
    p = ConfigParser()
    p.read('Kueski_mletc/conf/api.conf')
    dict_params = {s: dict(p.items(s)) for s in p.sections()}
    pd.set_option("display.max_columns", None)
    client_id = int(request.data.decode('utf-8'))
    dataloader = DataLoaderFeatures()
    df_pd = dataloader.read_features(dict_params['config']['path_features_input'])
    df_feat = df_pd[df_pd['id'] == client_id][['age', 'years_on_the_job', 'nb_previous_loans',
                                              'avg_amount_loans_previous', 'flag_own_car']]
    list_features = df_feat[df_feat['nb_previous_loans'] == df_feat['nb_previous_loans'].max()].values.tolist()
    info = dict()
    info[client_id] = list_features
    return jsonify(info)


@app.route('/model_predict', methods=['POST'])
def model_predict():
    p = ConfigParser()
    p.read('Kueski_mletc/conf/api.conf')
    dict_params = {s: dict(p.items(s)) for s in p.sections()}
    pd.set_option("display.max_columns", None)
    client_id = int(request.data.decode('utf-8'))
    dataloader = DataLoaderFeatures()
    df_pd = dataloader.read_features(dict_params['config']['path_features_input'])
    df_feat = df_pd[df_pd['id'] == client_id][['age', 'years_on_the_job', 'nb_previous_loans',
                                               'avg_amount_loans_previous', 'flag_own_car']]
    df_filter = df_feat[df_feat['nb_previous_loans'] == df_feat['nb_previous_loans'].max()]
    model = read_model(dict_params['config']['path_model_input'])
    predict = model.predict(df_filter).tolist()
    print(df_filter)
    info = dict()
    info['prediction'] = predict
    return jsonify(info)


if __name__ == "__main__":
    app.run(debug=True)
