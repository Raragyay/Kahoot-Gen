from functools import reduce
from typing import Any, Callable, Iterator, List

import pandas as pd
from sqlalchemy.orm import Query

from db import VocabularyTerm
from question_generators.question import Question
from question_generators.utilities import df_iterator, sample_n_rows_no_repeat, sample_n_rows_with_repeat


class QuestionGeneratorBase:
    default_answer_count = 4
    default_replace_questions = False

    def __init__(self):
        self.required_data_funcs: List[Callable[[Query], Any]] = []
        self.filter_funcs: List[Callable[[Query], Query]] = []

    def filter_df(self, query: Query) -> Query:
        return reduce(lambda query, func: func(query), self.filter_funcs, query)

    def obtain_required_data(self, query: Query) -> List[Any]:
        return [func(query) for func in self.required_data_funcs]

    def generate_n_questions(self, query: Query, num_of_questions: int, **kwargs) -> Iterator[Question]:
        filtered_query = self.filter_df(query)  # Used to sample rows
        data = self.obtain_required_data(query)  # Data from the category
        if kwargs.get('unique_questions', self.default_replace_questions):
            sampled_rows = sample_n_rows_no_repeat(filtered_query, num_of_questions)
        else:
            sampled_rows = sample_n_rows_with_repeat(filtered_query, num_of_questions)

        return (self.generate_a_question(row, *data, **kwargs) for row in sampled_rows)

    @staticmethod
    def generate_a_question(row: VocabularyTerm, *data, **kwargs) -> Question:
        raise NotImplementedError()
