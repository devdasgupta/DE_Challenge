from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType

from de_challenge.question1 import normalize_ndc_data
from de_challenge.settings import Config
from de_challenge.spark_utils import ReadWriteUtils

udf_normalize_ndc = udf(lambda x: normalize_ndc_data(x), StringType())


class ProcessPatientRecords(ReadWriteUtils):
    def __init__(self, spark: SparkSession):
        super().__init__(spark)

    def normalize_med_data(self, df: DataFrame) -> DataFrame:
        """
        : TODO
        This function normalizes the medical data records by un-nesting the
        diagnosis records into one column and return the resultant records

        Args:
            df (DataFrame): Input dataframe from the data input

        Returns:
            DataFrame: Normalized dataframe with the required records

        Input Dataframe:
        Patient_ID	Diagnosis_Code_1	Diagnosis_Code_2	Diagnosis_Code_3	Diagnosis_Code_4	Service_Date	Amount_Paid	Amount_Billed
        1	        32723	        	        	        	                                    4/19/16	        5.39	    12.32
        2	        69274	            70909	            70400	            70219	            5/10/16	        6.76	    60

        Output Dataframe:
        Patient_ID  Diagnosis_Code  Service_Date
        1           32723           4/19/16
        2           69274           5/10/16
        2           70909           5/10/16
        2           70400           5/10/16
        2           70219           5/10/16
        """
        pass

    def main(self):
        # 1. The first step of the algorithm is to read the data into pandas dataframe and normalize it.
        # 1.a. Read records for medical_data_sample and remove duplicate
        medical_data_sample_df = self.read_csv(Config.MED_DATA_SAMPLE).df.dropDuplicates()

        # 1.b. Normalize the data for medical_data_sample
        medical_data_sample_df = self.normalize_med_data(medical_data_sample_df)

        # 1.c. Read records for pharmacy data sample and remove duplicate
        pharmacy_data_sample_df = self.read_csv(Config.PHARM_DATA_SAMPLE).df.dropDuplicates()

        # 1.d. Normalize the ndc data in pharmacy to the acceptable format
        pharmacy_data_sample_df = pharmacy_data_sample_df.withColumn('NDC', udf_normalize_ndc(col('NDC')))

        # 1.e. Read records for NDC and remove duplicates
        ndc_df = self.read_csv(Config.NDC_DATA).df.dropDuplicates()

        # 1.f. Normalize the data for NDC records
        ndc_df = ndc_df.withColumn('ndc', udf_normalize_ndc(col('ndc')))

        # 1.g. Read the records for diagnosis code
        diagnosis_code_df = self.read_csv(Config.DIAGNOSIS_DATA).df.dropDuplicates()

        # 2. Merge medical records with diagnosis code to get all the
        # relevant patients with diagnosis code to Get patient with Condition Y
        cond_y_df = medical_data_sample_df.join(
            diagnosis_code_df,
            medical_data_sample_df.Diagnosis_Code == diagnosis_code_df.diagnosis_code,
            'inner'
        )

        # 3. Merge pharmacy records with NDC to get all patients who were given Drug X
        drug_x_df = pharmacy_data_sample_df.join(
            ndc_df,
            pharmacy_data_sample_df.NDC == ndc_df.ndc,
            'inner'
        )

        # 4. Finally merge the #2 and #3 to get the list of all such patients
        res_df = cond_y_df.join(
            drug_x_df,
            cond_y_df.Patient_ID == drug_x_df.Patient_ID,
            'inner'
        )

        # 5. Finally writing the results into a parquet file
        self.write_parquet(res_df, Config.OUTPUT_CSV_DATA_PATH)


def main(args=None):
    """ Main function to call and initialize the De_identification process.
    """

    spark = SparkSession \
        .builder \
        .appName('SchemaUpConversion') \
        .getOrCreate()
    ProcessPatientRecords(spark).main()


if __name__ == '__main__':
    main()
