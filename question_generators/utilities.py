from typing import Iterator, List, Set

import pandas as pd


def all_french_vocab_set(df) -> Set[str]:
    return set.union(*df['French'], *df['Antonym'])


def english_set(df) -> Set[str]:
    return set(df['English'])


def list_of_french_sets(df) -> List[Set[str]]:
    return [row[1]['French'] for row in df.iterrows()]


def df_iterator(df) -> Iterator:
    return (row[1] for row in df.iterrows())


def has_synonyms(row: pd.Series):
    return len(row['French']) > 1


def has_antonym(row: pd.Series):
    return len(row['Antonym']) > 0
