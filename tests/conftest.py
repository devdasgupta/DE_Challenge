from pytest import fixture
from de_challenge.settings import Config
import pandas as pd


@fixture
def test_data_df():
    file_path = f'{Config.OUTPUT_DATA_PATH}/{Config.OUTPUT_DATA_FILE}'
    df = pd.read_csv(file_path)

    return df
