import copy
import random
from typing import Dict, List

import pandas as pd

from db import VocabularyCategory, VocabularyTerm, db
from constants import DEFAULT_QUESTION
from question_generators import SectionPromptGenerator
from question_generators.english_to_french_generator import EnglishToFrenchGenerator
from question_generators.french_antonym_generator import FrenchAntonymGenerator
from question_generators.french_synonym_generator import FrenchSynonymGenerator
from question_generators.french_to_english_generator import FrenchToEnglishGenerator
from question_generators.question import Question
from question_generators.question_generator_base import QuestionGeneratorBase


class KahootQuestionGenerator:
    question_generators: Dict[str, QuestionGeneratorBase] = {
        'en-fr' : EnglishToFrenchGenerator(),
        'fr-en' : FrenchToEnglishGenerator(),
        'fr_syn': FrenchSynonymGenerator(),
        'fr_ant': FrenchAntonymGenerator(),
    }

    def __init__(self):
        pass

    def generate_questions(self,
                           questionType: str,
                           categories: List[str],
                           numOfQuestions: int,
                           **kwargs):
        """
            questionType: one of the keys of question_generators
            numOfQuestions: int > 0: how many questions are you making?
            options for kwargs:
                unique_answers: one of 2,3,4 -> how many answers are there for the question?
                unique_questions: bool -> is the term used unique for each question?
                duration: int > 0 -> how much time is given for the question, in milliseconds
                points: bool -> is the question worth points?
                pointsMultiplier: one of 1,2 -> point multiplier (base 1000)
        """
        if not categories and questionType != 'section_prompt':
            raise ValueError("Please specify at least one category from which to pick vocabulary.")
        base_query = db.session.query(VocabularyTerm).join(VocabularyTerm.category)
        category_filtered_query = base_query.filter(VocabularyCategory.name.in_(categories))
        question_generator_obj = self.question_generators[questionType]
        question_generator = question_generator_obj.generate_n_questions(category_filtered_query, numOfQuestions,
                                                                         **kwargs)
        return [KahootQuestionGenerator.create_question(question, **kwargs)
                for question in question_generator]

    @staticmethod
    def create_section_question(**kwargs):
        return [KahootQuestionGenerator.create_question(SectionPromptGenerator.generate_a_question(**kwargs))]

    @staticmethod
    def create_question(question: Question, **kwargs):
        question_template = copy.deepcopy(DEFAULT_QUESTION)
        question_template['question'] = question.prompt
        answer_array = [{
            'answer' : answer,
            'correct': answer in question.correct_answers}
            for answer in question.all_answers()]
        random.shuffle(answer_array)
        question_template['choices'] = answer_array
        for option in ['time', 'points', 'pointsMultiplier']:
            if option in kwargs:
                question_template[option] = kwargs[option]
        return question_template
