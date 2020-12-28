from functools import reduce

import pandas as pd
import numpy as np
import os


class KahootDataframeLoader:
    def __init__(self):
        self.df: pd.DataFrame = self.create_raw_df()
        self.drop_missing_antonyms()
        # self.reset_index()
        self.convert_vocab_to_sets()
        self.fix_dtypes()
        self.set_index_to_english()
        # We will avoid merging duplicate keys because some terms might fit in multiple categories. However,
        # it is important to ensure that the synonyms/antonyms are standard across different datasets.
        # self.merge_duplicate_keys(self.df)

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
        return pd.concat(KahootDataframeLoader.get_csv_dfs())

    def drop_missing_antonyms(self):
        self.df['Antonym'].replace(np.nan, "", inplace=True)

    def reset_index(self):
        self.df.reset_index(drop=True, inplace=True)

    def convert_vocab_to_sets(self):
        self.df['French'] = self.df['French'].apply(lambda string: set(string.split('; ')) - {''}, convert_dtype=True)
        self.df['Antonym'] = self.df['Antonym'].apply(lambda string: set(string.split('; ')) - {''}, convert_dtype=True)

    def merge_duplicate_keys(self):
        duplicate_keys = self.df[self.df.duplicated('English')]['English']
        for i, s in duplicate_keys.iteritems():
            print(f"Found duplicate key: {s}")
            sli = self.df[self.df['English'] == s]
            print(sli.iloc[0]['French'], sli.iloc[0]['Antonym'], sli.iloc[0]['Category'])
            for idx, row in list(sli.tail(len(sli) - 1).iterrows()):
                print(row['French'], row['Antonym'], row['Category'])
                sli.iloc[0]['French'] |= row['French']
                sli.iloc[0]['Antonym'] |= row['Antonym']
            self.df.drop(index=sli.tail(len(sli) - 1).index, inplace=True)

    def fix_dtypes(self):
        self.df = self.df.astype({
            'English' : 'string',
            'French'  : 'object',
            'Antonym' : 'object',
            'Category': 'category'})

    def set_index_to_english(self):
        self.df.set_index('English', inplace=True)

