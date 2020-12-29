from typing import Dict, Iterator, List, Set

import pandas as pd


async def all_french_vocab_set(df) -> Set[str]:
    return set.union(*df['French'], *df['Antonym'])


async def english_set(df) -> Set[str]:
    return set(df['English'])


async def list_of_french_sets(df) -> List[Set[str]]:
    return [row[1]['French'] for row in df.iterrows()]


async def df_iterator(df) -> Iterator:
    return (row[1] for row in df.iterrows())


async def has_synonyms(row: pd.Series):
    return len(row['French']) > 1


async def has_antonym(row: pd.Series):
    return len(row['Antonym']) > 0
