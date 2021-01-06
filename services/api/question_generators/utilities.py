import itertools
import math
import random
from typing import Iterable, Iterator, List, Set, Tuple

import pandas as pd
from sqlalchemy import VARCHAR, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Query

from db import VocabularyTerm


def all_french_vocab_set(query: Query) -> Set[str]:
    done_query = query.with_entities(VocabularyTerm.french, VocabularyTerm.antonym)
    return set(itertools.chain.from_iterable(itertools.chain.from_iterable(done_query)))


def english_set(query: Query) -> Set[str]:
    done_query = query.with_entities(VocabularyTerm.english)
    return set(itertools.chain.from_iterable(done_query))


def list_of_french_sets(query: Query) -> List[Set[str]]:
    done_query = query.with_entities(VocabularyTerm.french)
    return [set(l) for l in itertools.chain.from_iterable(done_query)]


def df_iterator(query: Query) -> Iterable[Tuple[List, List]]:
    done_query = query.with_entities(VocabularyTerm.french, VocabularyTerm.antonym)
    return done_query


def has_synonyms(query: Query) -> Query:
    return query.filter(func.array_length(VocabularyTerm.french, 1) > 1)


def has_antonym(query: Query) -> Query:
    return query.filter(VocabularyTerm.antonym.__ne__('{}'))


def sample_n_rows_no_repeat(query: Query, num_of_rows: int) -> Iterable[VocabularyTerm]:  # Assumption: primary key
    out = {}
    count = query.count()
    pct = num_of_rows / count
    while len(out) < num_of_rows:
        sample = query.filter(func.random() < pct)
        for row in sample:
            out[row.id] = row
            if len(out) >= num_of_rows:
                break
    return out.values()


def sample_n_rows_with_repeat(query: Query, num_of_rows: int) -> Iterator[VocabularyTerm]:
    out = []
    count = query.count()
    for _ in range(num_of_rows):
        row = query.offset(math.floor(random.random() * count)).first()
        out.append(row)
    return out
