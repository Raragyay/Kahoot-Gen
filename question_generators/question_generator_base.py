from typing import Any, Callable, Iterator, List

import pandas as pd

from question_generators.question import Question
from question_generators.utilities import df_iterator


class QuestionGeneratorBase:
    default_answer_count = 4
    default_replace_questions = False

    def __init__(self):
        self.required_data_funcs: List[Callable[[pd.DataFrame], Any]] = []
        self.filter_funcs: List = []

    def filter_df(self, df: pd.DataFrame) -> pd.DataFrame:
        # We avoid using apply syntax because apply expects a function, while we are using async coroutines
        return df.loc[[all(func(row) for func in self.filter_funcs)
                       for row in df_iterator(df)]]

    def obtain_required_data(self, df: pd.DataFrame) -> List[Any]:
        return [func(df) for func in self.required_data_funcs]

    def generate_n_questions(self, df: pd.DataFrame, num_of_questions: int, **kwargs) -> Iterator[Question]:
        filtered_df = self.filter_df(df)  # Used to sample rows
        data = self.obtain_required_data(df)  # Data from the category
        sampled_rows = map(lambda tup: tup[1],  # Retrieve the series instead of the index
                           filtered_df.sample(num_of_questions,
                                              replace=kwargs.get('unique_questions', self.default_replace_questions))
                           .iterrows())

        return (self.generate_a_question(row, *data, **kwargs) for row in sampled_rows)

    @staticmethod
    def generate_a_question(row: pd.Series, *data, **kwargs) -> Question:
        raise NotImplementedError()
