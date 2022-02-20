import pandas as pd


class DataLoaderFeatures:

    @staticmethod
    def read_features(input_path):
        """
        Read the csv input using a schema
        :return df: Dataframe with risk information
        """
        pd.set_option("display.max_columns", None)
        df = pd.read_parquet(input_path, engine='pyarrow')
        df.fillna(0, inplace=True)
        return df
