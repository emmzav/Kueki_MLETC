from pyspark.sql.window import Window
from pyspark.sql.functions import col, row_number, avg, datediff, current_date, when, lit


class DataFrameBuilder:

    def __init__(self, spark, df):
        """
        Constructor
        """
        self.__spark = spark
        self.df = df
        self.df1 = None
        self.df2 = None
        self.df3 = None
        self.df4 = None

    def calc_nb_previous_loans(self):
        """
        Filter dataframe 813 with the only necessary accounts
        :param df_813: Dataframe 813 with only the necessary columns and dates
        :return: Filter dataframe 813
        """
        window_spec = Window.partitionBy("id").orderBy("loan_date")
        self.df1 = self.df.withColumn("nb_previous_loans", row_number().over(window_spec)-1)

    def calc_avg_amount_loans_prev(self):
        """
        Filter dataframe 813 with the only necessary accounts
        :param df_813: Dataframe 813 with only the necessary columns and dates
        :return: Filter dataframe 813
        """
        self.df2 = self.df1.withColumn("avg_amount_loans_previous",
                                       avg("loan_amount").over(Window.partitionBy(col('id'))
                                                               .orderBy(col("nb_previous_loans"))
                                                               .rangeBetween(Window.unboundedPreceding, -1)))

    def calc_age(self):
        """
        Filter dataframe 813 with the only necessary accounts
        :param df_813: Dataframe 813 with only the necessary columns and dates
        :return: Filter dataframe 813
        """
        self.df3 = self.df2.select(col('*'), ((datediff(current_date(), col('birthday')))/365).cast('int').alias('age'))

    def calc_years_on_the_job(self):
        """
        Filter dataframe 813 with the only necessary accounts
        :param df_813: Dataframe 813 with only the necessary columns and dates
        :return: Filter dataframe 813
        """
        df = self.df3.select(col('*'),
                             ((datediff(current_date(), col('job_start_date')))/365).cast('int').alias('yearsjob'))

        self.df4 = df.select(col('*'),
                       (when(col('yearsjob') <= 0, lit(None))
                        .otherwise(col('yearsjob'))).alias('years_on_the_job')).drop('yearsjob')

    def calc_flag_own_car(self):
        """
        Filter dataframe 813 with the only necessary accounts
        :param df_813: Dataframe 813 with only the necessary columns and dates
        :return: Filter dataframe 813
        """
        df = self.df4.withColumn('flag_own_car', (when(col('flag_own_car') == 'N', lit(0)).otherwise(lit(1))))
        return df
