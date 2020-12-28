import random

from question_generators.data_generators import syn_ant_set


async def en_fr(row, synonym_and_antonym_set, **kwargs):
    row_data = row[1]
    english_term = row_data['English']
    chosen_french_answer = random.sample(row_data['French'], 1)[0]
    incorrect_answers = random.sample(synonym_and_antonym_set - row_data['French'],
                                      kwargs.get('unique_answers', 4) - 1)
    return english_term, chosen_french_answer, incorrect_answers


en_fr.required_data = [syn_ant_set]
