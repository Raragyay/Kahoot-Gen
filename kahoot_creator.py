import copy
from typing import Dict, List

import slugify

from kahoot_question_generator import KahootQuestionGenerator
from vocab_dataframe import VocabDataframe


class KahootCreator:
    def __init__(self, kahoot):
        self.db = VocabDataframe()
        self.question_generator = KahootQuestionGenerator(self.db.df)
        self.kahoot: Dict = copy.deepcopy(kahoot)

    def generate_questions(self, question_section_list: List[Dict]):
        """
        :param question_section_list: A list of different sets of parameters for generating questions
        :return:
        """
        questions = [question for params in question_section_list
                     for question in self.question_generator.generate_questions(**params)]
        self.kahoot['kahoot']['questions'] = questions

    @property
    def title(self):
        return self.kahoot['kahoot']['title']

    @title.setter
    def title(self, new_title: str):
        self.kahoot['kahoot']['title'] = new_title
        self.kahoot['kahoot']['slug'] = slugify.slugify(new_title)

    @property
    def uuid(self):
        return self.kahoot['kahoot']['uuid']

    @uuid.setter
    def uuid(self, new_uuid: str):
        self.kahoot['kahoot']['uuid'] = new_uuid
        self.kahoot['id'] = new_uuid
