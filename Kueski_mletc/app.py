import sys
from configparser import ConfigParser
from Kueski_mletc.controller import ControllerProcess


def get_config(phase):
    """
    Get parameters from configuration file and load them into a dictionary
    :param phase: Name of the phase to be executed.
    It can be one of the following values: create_features, model_train or model_predict
    :return my_config_parser_dict: Dictionary that contains that params to be used
    """
    p = ConfigParser()

    if phase == 'create_features':
        p.read('Kueski_mletc/conf/create_features.conf')
    elif phase == 'model_train':
        p.read('Kueski_mletc/conf/model_train.conf')
    elif phase == 'model_predict':
        p.read('Kueski_mletc/conf/model_predict.conf')
    elif phase == 'api':
        p.read('Kueski_mletc/conf/api.conf')
    else:
        raise ValueError("--input-file must be one of the following phases: "
                         "create_features, model_train or model_predict")
    my_config_parser_dict = {s: dict(p.items(s)) for s in p.sections()}
    return my_config_parser_dict


def run():
    config_dict = get_config(sys.argv[1])
    controller = ControllerProcess(config_dict)
    controller.main()
