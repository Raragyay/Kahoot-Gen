import asyncio
from typing import Any, AsyncIterator, Callable, Coroutine, List

import pandas as pd

from question_generators.question import Question


class QuestionGeneratorBase:
    default_answer_count = 4
    default_replace_questions = False

    def __init__(self):
        self.required_data_funcs: List[Callable[[pd.DataFrame], Any]] = []
        self.filter_funcs: List[Coroutine] = []

    async def filter_df(self, df: pd.DataFrame) -> pd.DataFrame:
        # We avoid using apply syntax because apply expects a function, while we are using async coroutines
        return df.loc[[all(await asyncio.gather(*map(lambda func: func(row[1]), self.filter_funcs))) for row in
                       df.iterrows()]]

    async def obtain_required_data(self, df: pd.DataFrame) -> List[Any]:
        return [await func(df) for func in self.required_data_funcs]

    async def generate_n_questions(self, df: pd.DataFrame, num_of_questions: int, **kwargs) -> AsyncIterator[Question]:
        filtered_df = await self.filter_df(df)  # Used to sample rows
        data = await self.obtain_required_data(df)  # Data from the category
        sampled_rows = map(lambda tup: tup[1],  # Retrieve the series instead of the index
                           filtered_df.sample(num_of_questions,
                                              replace=kwargs.get('unique_questions', self.default_replace_questions))
                           .iterrows())

        return (await self.generate_a_question(row, *data, **kwargs) for row in sampled_rows)

    @staticmethod
    async def generate_a_question(row: pd.Series, *data, **kwargs) -> Question:
        raise NotImplementedError()
