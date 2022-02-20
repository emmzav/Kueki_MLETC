import traceback
from pyspark.sql import SparkSession

from Kueski_mletc.create_features.build import DataFrameBuilder
from Kueski_mletc.create_features.writer import DataFrameWriter
from Kueski_mletc.create_features.dataloader_credit_risk import DataLoader


class ControllerProcess:

    def __init__(self, config_dict):
        """
        Constructor
        """
        self.config_dict = config_dict
        self.spark = SparkSession.builder.getOrCreate()

    def main(self):
        """
        Run all de process.
        """
        print(self.config_dict)
        dataloader = DataLoader(self.spark, self.config_dict['config']['path_credit_risk_input'])
        df = dataloader.read()
        df.show(5)

        builder = DataFrameBuilder(self.spark, df)
        builder.calc_nb_previous_loans()
        builder.calc_avg_amount_loans_prev()
        builder.calc_age()
        builder.calc_years_on_the_job()
        df1 = builder.calc_flag_own_car()
        df2 = df1.select(df1.id, df1.age, df1.years_on_the_job, df1.nb_previous_loans,
                         df1.avg_amount_loans_previous, df1.flag_own_car, df1.status)
        df2.show(5)

        writer = DataFrameWriter(self.spark, df2, self.config_dict['config']['path_features_output'])
        writer.write_features()
        return 0
