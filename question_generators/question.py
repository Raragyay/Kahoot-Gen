from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    """A question with a prompt, correct answer, and list of incorrect answers"""
    prompt: str
    correct_answer: str
    incorrect_answers: List[str]
