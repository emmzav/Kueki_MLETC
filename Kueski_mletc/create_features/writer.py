class DataFrameWriter:

    @staticmethod
    def write_features(df, output_path):
        """
        Write the features dataframe
        :param df: Dataframe with feature columns
        :param output_path: Path to write
        """
        df.write.mode("overwrite").parquet(output_path)
        print(df.show(10))
        return 0
