import copy
from typing import Dict, List

import slugify

from constants import DEFAULT_KAHOOT
from kahoot_question_generator import KahootQuestionGenerator
from vocab_dataframe import VocabDataframe


class KahootCreator:
    def __init__(self, kahoot=DEFAULT_KAHOOT):
        self.db = VocabDataframe()
        self.question_generator = KahootQuestionGenerator(self.db.df)
        self.kahoot = copy.deepcopy(kahoot)

    def generate_questions(self, question_section_list: List[Dict]):
        """
        :param question_section_list: A list of different sets of parameters for generating questions
        :return:
        """
        questions = [await self.question_generator.generate_questions(**params) for params in question_section_list]
        self.kahoot['kahoot']['questions'] = questions

    @property
    def title(self):
        return self.kahoot['kahoot']['title']

    @title.setter
    def title(self, new_title):
        self.kahoot['kahoot']['title'] = new_title
        self.kahoot['kahoot']['slug'] = slugify.slugify(new_title)
