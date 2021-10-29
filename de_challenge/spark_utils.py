from abc import ABC, abstractmethod
from typing import NoReturn, Optional

from pyspark.sql import DataFrame
from pyspark.sql.utils import AnalysisException
from de_challenge.settings import Config


class AbstractReadWriteUtils(ABC):
    """ Defines a contract that ReadWriteUtils should follow for using DataFrameReader and DataFrameWriter classes """

    @abstractmethod
    def read_parquet(self, table_name: str) -> DataFrame:
        pass

    @abstractmethod
    def write_parquet(self, dataframe: DataFrame, resource: str) -> NoReturn:
        pass

    @abstractmethod
    def read_csv(self, file_name: str) -> DataFrame:
        pass

    @abstractmethod
    def write_csv(self, df: DataFrame, output_location: str, mode: str) -> NoReturn:
        pass


class ReadWriteUtils(AbstractReadWriteUtils):
    """ Utility class used to read and write data to different data sources, mainly JDBC and Amazon S3 """

    def __init__(self, spark_session):
        self.spark = spark_session

    def read_csv(self, file_name: str) -> Optional[DataFrame]:
        """ Read a comma separated file into a DataFrame

        :param file_name: The name of the file being read into a DataFrame
        :return: A DataFrame if the file was found, otherwise, None
        """
        read_location = f'{Config.INPUT_DATA_PATH}/{file_name}'
        try:
            return self.spark.read.csv(read_location, header=True)
        except AnalysisException:
            return None

    def write_csv(self, df: DataFrame, output_location: str, mode: str = 'overwrite') -> NoReturn:
        """ Serialize a DataFrame in a comma separated format

        :param df: The DataFrame to be serialized
        :param output_location: The location to which we're serializing the DataFrame
        :param mode: The mode to use when serializing the DataFrame. Default is overwrite
        """
        df.write.csv(output_location, mode=mode, header="true")

    def read_parquet(self, table_name: str, fpath: str = None) -> Optional[DataFrame]:
        """ Retrieve a table stored in parquet format

        :param table_name: Which table the application is retrieving
        :return: A DataFrame containing the table retrieved

        Args:
            fpath:
        """
        fpath = fpath if fpath else Config.OUTPUT_DATA_PATH
        read_location = f"{fpath}/{table_name}"
        try:
            return self.spark.read.parquet(read_location)
        except AnalysisException:
            return None

    def write_parquet(self, dataframe: DataFrame, output_location: str) -> NoReturn:
        """ Write a DataFrame to a given output location in parquet format.

        For example if we were writing to S3 output with resource clinical_lab
        we would get the following output location:

        s3://example_bucket/clinical_lab

        :param dataframe: The DataFrame to be written as output
        :param output_location: The resource being written
        """
        spark_conf = self.spark.sparkContext.getConf()
        num_instances = spark_conf.get('spark.executor.instances') or 1
        cores_per_instance = spark_conf.get('spark.executor.cores') or 2

        # "2 partitions per core" is a good rule of thumb when writing dataframes
        num_partitions = 2 * int(num_instances) * int(cores_per_instance)

        dataframe.repartition(num_partitions).write.parquet(output_location, mode="overwrite")
