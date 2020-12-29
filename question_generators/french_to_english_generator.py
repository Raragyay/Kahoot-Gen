import random

from question_generators.utilities import english_set
from question_generators.question import Question
from question_generators.question_generator_base import QuestionGeneratorBase


class FrenchToEnglishGenerator(QuestionGeneratorBase):
    def __init__(self):
        super().__init__()
        self.required_data_funcs = [english_set]

    @staticmethod
    async def generate_a_question(row, *data, **kwargs):
        english_set = data[0]
        french_term = random.sample(row['French'], 1)[0]
        correct_english_answer = row['English']
        incorrect_answers = random.sample(
            english_set - {correct_english_answer},
            kwargs.get('unique_answers', FrenchToEnglishGenerator.default_answer_count) - 1
        )
        return Question(french_term, correct_english_answer, incorrect_answers)
