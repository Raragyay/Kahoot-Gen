import asyncio
import copy
import random
from functools import reduce
from typing import Callable, Dict, List, Set, Tuple

import pandas as pd

from constants import DEFAULT_QUESTION
from question_generators.en_fr import en_fr
from question_generators.fr_en import fr_en
from vocab_dataframe import VocabDataframe


class KahootQuestionGenerator:
    question_generators: Dict[str, Callable] = {
        'en-fr': en_fr,
        'fr-en': fr_en
    }

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    async def generate_questions(self,
                                 question_type: str,
                                 categories: List[str],
                                 num_of_questions: int,
                                 **kwargs):
        """
            options for kwargs:
                unique_answers: one of 2,3,4 -> how many answers are there for the question?
                unique_questions: bool -> is the term used unique for each question?
                duration: int > 0 -> how much time is given for the question, in milliseconds
                points: bool -> is the question worth points?
                pointsMultiplier: int -> point multiplier (base 1000)
        """
        if not categories:
            raise ValueError("Please specify at least one category from which to pick vocabulary.")
        filtered_df = self.df[self.df['Category'].isin(categories)]
        question_func = self.question_generators[question_type]
        question_func_required_data = question_func.required_data
        created_data = [await func(filtered_df) for func in question_func_required_data]
        return [await KahootQuestionGenerator.create_question(*(await question_func(row, *created_data, **kwargs)),
                                                              **kwargs)
                for row in
                filtered_df.sample(num_of_questions, replace=kwargs.get('unique_questions', False)).iterrows()]

    @staticmethod
    async def create_question(question, correct_answer, wrong_answers, **kwargs):
        question_template = copy.deepcopy(DEFAULT_QUESTION)
        question_template['question'] = question
        answer_array = [{
            'answer' : answer,
            'correct': answer == correct_answer}
            for answer in [correct_answer] + wrong_answers]
        random.shuffle(answer_array)
        question_template['choices'] = answer_array
        for option in ['time', 'points', 'pointsMultiplier']:
            if option in kwargs:
                question_template[option] = kwargs[option]
        return question_template


async def main():
    vd = VocabDataframe()
    kqg = KahootQuestionGenerator(vd.df)
    print(await kqg.generate_questions('fr-en', ["food"], 3))


if __name__ == '__main__':
    asyncio.run(main())
