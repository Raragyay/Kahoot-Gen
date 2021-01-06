import pandas as pd

from question_generators.question import MultiAnswerQuestion, Question
from question_generators.question_generator_base import QuestionGeneratorBase


class SectionPromptGenerator(QuestionGeneratorBase):
    """
    Alerts the players that a new section is coming up
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def generate_a_question(row=None, *data, **kwargs) -> Question:
        """
        Must include "section_prompt" in kwargs. This will become the prompt that the players see
        Optional argument "section_answers" is a list of up to 4 correct answers
        :param row:
        :param data:
        :param kwargs:
        :return:
        """
        if "sectionPrompt" not in kwargs:
            raise AttributeError("Section Prompt was not found in kwargs")
        if "section_answers" in kwargs:
            section_answers = kwargs['section_answers']
        else:
            section_answers = ['ok'] * 4
        return MultiAnswerQuestion(kwargs['sectionPrompt'], [], section_answers)
