import itertools
import random
from functools import reduce

import pandas as pd

from question_generators.question import Question, SingleAnswerQuestion
from question_generators.question_generator_base import QuestionGeneratorBase
from question_generators.utilities import all_french_vocab_set, df_iterator, has_antonym


class FrenchAntonymGenerator(QuestionGeneratorBase):
    def __init__(self):
        super().__init__()
        self.required_data_funcs.extend([df_iterator, all_french_vocab_set])
        self.filter_funcs.extend([has_antonym])

    @staticmethod
    def generate_a_question(row, *data, **kwargs) -> Question:
        df_iterator = data[0]
        all_vocab_set = data[1]
        chosen_french_word = random.choice(row.french)
        chosen_antonym = random.choice(row.antonym)
        invalid_answers = set(itertools.chain.from_iterable(
            r[1] for r in df_iterator if chosen_french_word in r[0]))
        incorrect_answers = random.sample(
            all_vocab_set - invalid_answers,
            kwargs.get('unique_answers', FrenchAntonymGenerator.default_answer_count) - 1
        )
        return SingleAnswerQuestion(chosen_french_word, incorrect_answers, chosen_antonym)
