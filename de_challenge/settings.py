from pathlib import Path
from decouple import config


class Config(object):
    INPUT_DATA_PATH = f'{Path(__file__).parent.absolute()}/input_data/xlsx'
    INPUT_DATA_FILE: str = config('INPUT_DATA_FILE', 'dummy_data.xlsx')

    OUTPUT_DATA_PATH = f'{Path(__file__).parent.absolute()}/output_data/xlsx'
    OUTPUT_DATA_FILE: str = config('OUTPUT_DATA_FILE', 'patient.csv')

    INPUT_CSV_DATA_PATH = f'{Path(__file__).parent.absolute()}/input_data/csv'
    MED_DATA_SAMPLE: str = config('MED_DATA_SAMPLE', 'medical_data_sample.csv')
    PHARM_DATA_SAMPLE: str = config('PHARM_DATA_SAMPLE', 'pharmacy_data_sample.csv')
    NDC_DATA: str = config('NDC_DATA', 'ndc.csv')
    DIAGNOSIS_DATA: str = config('DIAGNOSIS_DATA', 'diagnosis_code.csv')
    OUTPUT_CSV_DATA_PATH = f'{Path(__file__).parent.absolute()}/output_data/csv'

