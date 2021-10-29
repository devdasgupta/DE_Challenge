from pytest import fixture
from de_challenge.settings import Config
import pandas as pd


class StringConverter(dict):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return str

    def get(self, default=None):
        return str


@fixture
def test_data_df():
    file_path = f'{Config.OUTPUT_DATA_PATH}/{Config.OUTPUT_DATA_FILE}'
    df = pd.read_csv(file_path, converters=StringConverter())

    return df
