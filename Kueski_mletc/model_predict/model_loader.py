from joblib import load
from sklearn.ensemble import RandomForestClassifier


def read_model(input_path) -> RandomForestClassifier:
    """
    Read the parquet that contain the features
    :param input_path: Path of the model
    :return model: Loaded model
    """
    try:
        return load(input_path)
    except FileNotFoundError:
        raise FileNotFoundError(f'Input file {input_path} not found')
