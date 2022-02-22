from pyspark.sql import SparkSession

from Kueski_mletc.model_train.train import ModelTrain
from Kueski_mletc.model_predict.predict import model_predict
from Kueski_mletc.model_predict.model_loader import read_model
from Kueski_mletc.model_train.persist_model import ModelWriter
from Kueski_mletc.create_features.build import DataFrameBuilder
from Kueski_mletc.create_features.writer import DataFrameWriter
from Kueski_mletc.model_train.dataloader_features import DataLoaderFeatures
from Kueski_mletc.create_features.dataloader_credit_risk import DataLoaderRisk
from Kueski_mletc.model_predict.writer import write_predicts
from Kueski_mletc.api import app


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
            df = builder.calc_flag_own_car()
            writer = DataFrameWriter()
            df_features = df.select(df.id, df.age, df.years_on_the_job, df.nb_previous_loans,
                                    df.avg_amount_loans_previous, df.flag_own_car, df.status)
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

        elif self.config_dict['config']['stage_name'] == 'model_predict':
            dataloader = DataLoaderFeatures()
            df_feat = dataloader.read_features(self.config_dict['config']['path_features_input'])
            rf_model = read_model(self.config_dict['config']['path_model_input'])
            df_predict = model_predict(rf_model, df_feat)
            write_predicts(df_predict, self.config_dict['config']['path_predict_output'])

        elif self.config_dict['config']['stage_name'] == 'api':
            app.run(debug=True)
        return 0
