from dataclasses import dataclass, field
from typing import List


@dataclass
class Question:
    """A question with a prompt, correct answer, and list of incorrect answers"""
    prompt: str
    correct_answers: List[str] = field(default_factory=list, init=False)
    incorrect_answers: List[str]


@dataclass
class SingleAnswerQuestion(Question):
    single_answer: str

    def __post_init__(self):
        self.correct_answers = [self.single_answer]


@dataclass
class MultiAnswerQuestion(Question):
    multiple_answers: List[str]

    def __post_init__(self):
        self.correct_answers = self.multiple_answers
