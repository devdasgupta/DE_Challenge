from pathlib import Path
from decouple import config


class Config(object):

    INPUT_DATA_PATH = f'{Path(__file__).parent.absolute()}/input_data'
    INPUT_DATA :str = config('INPUT_DATA', 'dummy_data.xlsx')