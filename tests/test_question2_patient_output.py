import pytest


def test_ndc_format(test_data_df):
    df = test_data_df[test_data_df['NDC'].str.len() != 11]

    # Assert the NDC are 11 characters in length
    assert df.NDC.count() == 0

    # Assert there are no - in NDC
    dash_count = test_data_df['NDC'].str.contains('-').sum()
    assert dash_count == 0
