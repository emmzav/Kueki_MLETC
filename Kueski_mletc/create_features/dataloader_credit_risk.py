from pyspark.sql.types import StructType, StructField, IntegerType, DateType, StringType, DoubleType


class DataLoaderRisk:

    def __init__(self, spark, input_path):
        """
        Constructor
        """
        self.spark = spark
        self.input_path = input_path

    def read(self):
        """
        Read the csv input using a schema
        :return df: Dataframe with risk information
        """
        schema = StructType([
            StructField("loan_id", IntegerType()),
            StructField("id", IntegerType()),
            StructField("code_gender", StringType()),
            StructField("flag_own_car", StringType()),
            StructField("flag_own_realty", StringType()),
            StructField("cnt_children", IntegerType()),
            StructField("amt_income_total", DoubleType()),
            StructField("name_income_type", StringType()),
            StructField("name_education_type", StringType()),
            StructField("name_family_status", StringType()),
            StructField("name_housing_type", StringType()),
            StructField("days_birth", IntegerType()),
            StructField("days_employed", IntegerType()),
            StructField("flag_mobil", IntegerType()),
            StructField("flag_work_phone", IntegerType()),
            StructField("flag_phone", IntegerType()),
            StructField("flag_email", IntegerType()),
            StructField("occupation_type", StringType()),
            StructField("cnt_fam_members", DoubleType()),
            StructField("status", IntegerType()),
            StructField("birthday", DateType()),
            StructField("job_start_date", DateType()),
            StructField("loan_date", DateType()),
            StructField("loan_amount", DoubleType()),
        ])
        df = self.spark.read.csv(self.input_path, header=True, nullValue='NA', schema=schema)
        return df
