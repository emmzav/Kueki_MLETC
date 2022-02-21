from pyspark.sql import SparkSession

from Kueski_mletc.model_train.train import ModelTrain
from Kueski_mletc.model_train.persist_model import ModelWriter
from Kueski_mletc.create_features.build import DataFrameBuilder
from Kueski_mletc.create_features.writer import DataFrameWriter
from Kueski_mletc.model_train.dataloader_features import DataLoaderFeatures
from Kueski_mletc.create_features.dataloader_credit_risk import DataLoaderRisk


class ControllerProcess:

    def __init__(self, config_dict):
        """
        Constructor
        """
        self.config_dict = config_dict
        self.spark = SparkSession.builder.getOrCreate()

    def main(self):
        """
        Run all de process according to the phase selected by the param
        """
        if self.config_dict['config']['stage_name'] == 'create_features':
            dataloader = DataLoaderRisk(self.spark, self.config_dict['config']['path_credit_risk_input'])
            df_csv = dataloader.read()
            builder = DataFrameBuilder(self.spark, df_csv)
            builder.calc_nb_previous_loans()
            builder.calc_avg_amount_loans_prev()
            builder.calc_age()
            builder.calc_years_on_the_job()
            df_features = builder.calc_flag_own_car()
            writer = DataFrameWriter()
            writer.write_features(df_features, self.config_dict['config']['path_features_output'])

        elif self.config_dict['config']['stage_name'] == 'model_tain':
            dataloader = DataLoaderFeatures()
            df_feat = dataloader.read_features(self.config_dict['config']['path_features_input'])
            model_train = ModelTrain(df_feat)
            model_train.data_smote()
            model_train.data_split()
            rf_model = model_train.random_forest_train()
            model_train.model_metrics()
            model_writer = ModelWriter()
            model_writer.write_model(rf_model, self.config_dict['config']['path_model_output'])

        return 0
