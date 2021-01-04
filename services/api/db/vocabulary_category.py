from db.db import db


class VocabularyCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    terms = db.relationship("VocabularyTerm", backref="vocabulary_category", lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Category {self.name}>'
