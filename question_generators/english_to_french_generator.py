import random

from question_generators.utilities import all_french_vocab_set
from question_generators.question import Question, SingleAnswerQuestion
from question_generators.question_generator_base import QuestionGeneratorBase


class EnglishToFrenchGenerator(QuestionGeneratorBase):
    def __init__(self):
        super().__init__()
        self.required_data_funcs.extend([all_french_vocab_set])

    @staticmethod
    async def generate_a_question(row, *data, **kwargs):
        all_vocab_set = data[0]
        english_term = row['English']
        chosen_french_answer = random.sample(row['French'], 1)[0]
        incorrect_answers = random.sample(
            all_vocab_set - row['French'],
            kwargs.get('unique_answers', EnglishToFrenchGenerator.default_answer_count) - 1
        )
        return SingleAnswerQuestion(english_term, incorrect_answers, chosen_french_answer)
