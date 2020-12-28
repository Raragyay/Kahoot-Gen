import random

from question_generators.data_generators import english_set


async def fr_en(row, english_set, **kwargs):
    row_data = row[1]
    french_term = random.sample(row_data['French'], 1)[0]
    correct_english_answer = row_data['English']
    incorrect_answers = random.sample(english_set - {correct_english_answer},
                                      kwargs.get('unique_answers', 4) - 1)
    return french_term, correct_english_answer, incorrect_answers


fr_en.required_data = [english_set]
