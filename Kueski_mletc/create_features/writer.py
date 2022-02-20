class DataFrameWriter:

    @staticmethod
    def write_features(df, output_path):
        """
        Write the features dataframe
        :param df: Dataframe with feature columns
        :param output_path: Path to write
        """
        df.select(df.id, df.age, df.years_on_the_job, df.nb_previous_loans, df.avg_amount_loans_previous,
                  df.flag_own_car, df.status).write.mode("overwrite").parquet(output_path)
        return 0
