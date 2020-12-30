import random

from pandas import Series

from question_generators.question import Question, SingleAnswerQuestion
from question_generators.question_generator_base import QuestionGeneratorBase
from question_generators.utilities import all_french_vocab_set, has_synonyms, list_of_french_sets


class FrenchSynonymGenerator(QuestionGeneratorBase):
    def __init__(self):
        super().__init__()
        self.required_data_funcs.extend([list_of_french_sets, all_french_vocab_set])
        self.filter_funcs.extend([has_synonyms])

    @staticmethod
    async def generate_a_question(row: Series, *data, **kwargs) -> Question:
        list_of_french_sets = data[0]
        all_french_vocab_set = data[1]
        chosen_french_term, chosen_answer = random.sample(row['French'], 2)
        sets_containing_chosen_french_term = set.union(*filter(lambda s: chosen_french_term in s,
                                                               list_of_french_sets))
        incorrect_answers = random.sample(
            all_french_vocab_set - sets_containing_chosen_french_term,
            kwargs.get('unique_answers', FrenchSynonymGenerator.default_answer_count) - 1
        )
        return SingleAnswerQuestion(chosen_french_term, incorrect_answers, chosen_answer)
