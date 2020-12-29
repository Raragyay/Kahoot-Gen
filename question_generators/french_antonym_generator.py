import random
from functools import reduce

import pandas as pd

from question_generators.question import Question
from question_generators.question_generator_base import QuestionGeneratorBase
from question_generators.utilities import all_french_vocab_set, df_iterator, has_antonym


class FrenchAntonymGenerator(QuestionGeneratorBase):
    def __init__(self):
        super().__init__()
        self.required_data_funcs = [df_iterator, all_french_vocab_set]
        self.filter_funcs = [has_antonym]

    @staticmethod
    async def generate_a_question(row: pd.Series, *data, **kwargs) -> Question:
        df_iterator = data[0]
        all_vocab_set = data[1]
        chosen_french_word = random.sample(row['French'], 1)[0]
        chosen_antonym = random.sample(row['Antonym'], 1)[0]
        invalid_answers = reduce(
            set.union,
            (r['Antonym'] for r in df_iterator if chosen_french_word in r['French']),
            set()
        )
        incorrect_answers = random.sample(
            all_vocab_set - invalid_answers,
            kwargs.get('unique_answers', FrenchAntonymGenerator.default_answer_count) - 1
        )
        return Question(chosen_french_word, chosen_antonym, incorrect_answers)
