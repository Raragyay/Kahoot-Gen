from db.db import db


class VocabularyTerm(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    english = db.Column(
        db.VARCHAR(255),
        nullable=False
    )
    french = db.Column(
        db.ARRAY(db.VARCHAR(255),
                 dimensions=1,
                 zero_indexes=True),
        nullable=False,
        default=[]
    )
    antonym = db.Column(
        db.ARRAY(db.VARCHAR(255),
                 dimensions=1,
                 zero_indexes=True),
        nullable=False,
        default=True
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('vocabulary_category.id'),
        nullable=False
    )
    category = db.relationship('VocabularyCategory')

    def __init__(self, english, french, antonym, category):
        self.english = english
        self.french = french
        self.antonym = antonym
        self.category = category

    def __repr__(self):
        return f'<VocabTerm {self.english}>'
