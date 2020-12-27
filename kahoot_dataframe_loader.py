from functools import reduce

import pandas as pd
import numpy as np
import os


class KahootDataframeLoader:
    def __init__(self):
        self.df = self.create_raw_df()
        self.clean_df(self.df)

    @staticmethod
    def get_csv_dfs():
        file_dir = os.path.dirname(os.path.realpath(__file__))
        for file in sorted(os.listdir(os.path.join(file_dir, 'vocab_database'))):
            temp_df = pd.read_csv(os.path.join(file_dir, 'vocab_database', file),
                                  names=['English', 'French', 'Antonym'], dtype=str)
            temp_df['Category'] = file.replace('.csv', '')
            yield temp_df

    @staticmethod
    def create_raw_df():
        return reduce(lambda x, y: x.append(y), KahootDataframeLoader.get_csv_dfs(), pd.DataFrame())

    @staticmethod
    def clean_df(df):
        df['Antonym'].replace(np.nan, "", inplace=True)


if __name__ == '__main__':
    kdl = KahootDataframeLoader()
    print(kdl.df)
