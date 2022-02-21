import pandas as pd


class DataLoaderFeatures:

    @staticmethod
    def read_features(input_path):
        """
        Read the parquet that contain the features
        :param input_path: Path of the parquet input file
        :return df: Dataframe with the features information
        """
        pd.set_option("display.max_columns", None)
        df = pd.read_parquet(input_path, engine='pyarrow')
        df.fillna(0, inplace=True)
        return df
