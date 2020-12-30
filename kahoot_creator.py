from kahoot_question_generator import KahootQuestionGenerator
from vocab_dataframe import VocabDataframe


class KahootCreator:
    def __init__(self):
        self.db = VocabDataframe()
        self.question_generator = KahootQuestionGenerator(self.db.df)
