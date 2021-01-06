import copy
import itertools
from typing import Dict, List

import slugify

from kahoot_question_generator import KahootQuestionGenerator


class KahootCreator:
    def __init__(self, kahoot):
        self.question_generator = KahootQuestionGenerator()
        self.kahoot: Dict = copy.deepcopy(kahoot)

    def generate_questions(self, section_list: List[Dict]):
        """
        :param section_list: A list of different sets of parameters for generating questions
        :return:
        """
        questions = [question
                     for section in section_list
                     for question in
                     itertools.chain(self.question_generator.create_section_question(**section),
                                     itertools.chain.from_iterable(
                                         self.question_generator.generate_questions(**questionGenerator)
                                         for questionGenerator in section['questionGenerators']))
                     ]
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
