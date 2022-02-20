
# -*- coding: utf-8 -*-
import sys
from configparser import ConfigParser
from Kueski_mletc.controller import ControllerProcess


def get_config(param):
    p = ConfigParser()

    if param == 'create_features':
        p.read('mletc_risk/conf/create_features.conf')
    elif param == 'model_train':
        p.read('mletc_risk/conf/model_train.conf')
    elif param == 'model_predict':
        p.read('mletc_risk/conf/model_predict.conf')
    else:
        raise ValueError("--input-file must be one of the following phases: "
                         "create_features, model_train or model_predict")
    my_config_parser_dict = {s: dict(p.items(s)) for s in p.sections()}
    return my_config_parser_dict


def run():
    config_dict = get_config(sys.argv[1])
    controller = ControllerProcess(config_dict)
    controller.main()
