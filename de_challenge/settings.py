from pathlib import Path
from decouple import config


class Config(object):

    INPUT_DATA_PATH = f'{Path(__file__).parent.absolute()}/input_data'
    INPUT_DATA_FILE :str = config('INPUT_DATA_FILE', 'dummy_data.xlsx')

    OUTPUT_DATA_PATH = f'{Path(__file__).parent.absolute()}/output_data'
    OUTPUT_DATA_FILE: str = config('OUTPUT_DATA_FILE', 'patient.csv')
