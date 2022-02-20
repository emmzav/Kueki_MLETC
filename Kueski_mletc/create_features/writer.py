
class DataFrameWriter:

    def __init__(self, spark, df, path_output):
        """
        Constructor.
        """
        self.__spark = spark
        self.__df = df
        self.__path_output = path_output

    def write_features(self):
        """
        Write the ABT dataframe
        :param df: Dataframe ABT
        :param output_path: Path to write
        :param partition_by: Column of partition
        :param date: end date from extraction
        """
        self.__df.write.mode("overwrite").parquet(self.__path_output)
        return 0
