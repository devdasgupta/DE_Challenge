'''
Problem Statement
The claims data comes with duplicates and NDCs are messy.
Please write a script to de- deduplicate the data (Note:rows identical to each other
in every single column is considered duplicate) and clean the NDC into standard
format (11 digits and matchable to the format in tab ndc)
'''

import pandas as pd
from pandas import DataFrame
from de_challenge.settings import Config


def get_dataframe_from_xlsx(sheet_name: str, **kwargs) -> DataFrame:
    """
    This functions reads all the data from the input excel sheet and provided sheet name
    This function also drops all the duplicate items from the data set.

    Args:
        sheet_name (str): The name of the sheet which has the data

    Returns:
        DataFrame: The data imported as a pandas dataframe
    """
    input_data_file = f'{Config.INPUT_DATA_PATH}/{Config.INPUT_DATA}'

    # Create an empty dataframe
    df = pd.DataFrame()

    try:
        if kwargs.get('header'):
           df = pd.read_excel(open(input_data_file, 'rb'), sheet_name=sheet_name, index_col=None, header=None, names=[sheet_name])
        else:
            df = pd.read_excel(open(input_data_file, 'rb'), sheet_name=sheet_name)
    except ValueError:
        print(f'The Worksheet named {sheet_name} not found')

    # Returns all unique records from the data set. Dropping all duplicates
    return df.astype(str).drop_duplicates().reset_index(drop=True)


def get_normalize_med_data(df: DataFrame) -> DataFrame:
    """
    This function normalizes the medical data records by unnesting the
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
    _columns= {'Patient_ID': 'str', 'Diagnosis_Code': 'str', 'Service_Date': 'str'}
    norm_df = pd.DataFrame({c: pd.Series(dtype=t) for c, t in _columns.items()})

    for dc in ['Diagnosis_Code_1', 'Diagnosis_Code_2', 'Diagnosis_Code_3', 'Diagnosis_Code_4']:
        bf = df[['Patient_ID', dc, 'Service_Date']]
        bf.columns = _columns.keys()
        norm_df = norm_df.append(bf)

    # Remove all duplicate rows
    return norm_df.sort_values(by=['Patient_ID']).drop_duplicates().reset_index(drop=True)


def normalize_ndc_data(ndc: str) -> str:
    """
    This functions normalized the NDC column by replacing all - to ''
    and appending 0 to all NDC whose length < 11

    Args:
        ndc (str): The NDC input string

    returns:
        str: Normalized NDC input string
    """
    return ndc.replace('-', '').zfill(11)


def main():
    # 1. The first step of the algorith is to read the data into pandas dataframe and normalize it.
    # 1.a. Read records for medical_data_sample and remove duplicate
    medical_data_sample_df = get_dataframe_from_xlsx('medical_data_sample')

    # 1.b. Normalize the data for medical_data_sample
    medical_data_sample_df = get_normalize_med_data(medical_data_sample_df)

    # 1.c. Read records for pharmacy data sample and remove duplicate
    pharmacy_data_sample_df = get_dataframe_from_xlsx('pharmacy_data_sample')

    # 1.d. Normalize the ndc data in pharmacy to the acceptable format
    pharmacy_data_sample_df['NDC'] = pharmacy_data_sample_df['NDC'].apply(normalize_ndc_data)

    # 1.e. Read records for NDC and remove dupllicates
    ndc_df = get_dataframe_from_xlsx('ndc', header=True)

    # 1.f. Normalize the data for NDC records
    ndc_df['ndc'] = ndc_df['ndc'].apply(normalize_ndc_data)

    # 1.g. Read the records for diagnosis code
    diagnosis_code_df = get_dataframe_from_xlsx('diagnosis_code', header=True)

    # 2. Merge medical records with diagnosis code to get all the
    # relevant patients with diagnosis code to Get patient with Condition Y
    cond_y_df = pd.merge(medical_data_sample_df, diagnosis_code_df, left_on='Diagnosis_Code', right_on='diagnosis_code')

    # 3. Merge pharmacy records with NDC to get all patients who were given Drug X
    drug_x_df = pd.merge(pharmacy_data_sample_df, ndc_df, left_on='NDC', right_on='ndc')

    # 4. Finally merge the #2 and #3 to get the list of all such patients
    res_df = pd.merge(cond_y_df, drug_x_df, left_on='Patient_ID', right_on='Patient_ID')

    # 5. Get final patient list
    patient_list = res_df.Patient_ID.drop_duplicates().values.tolist()

    print(patient_list)


if __name__ == '__main__':
    main()
