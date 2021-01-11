from flask import Blueprint
from sqlalchemy import case, func, text

from db import VocabularyCategory, VocabularyTerm, db

default_table_blueprint = Blueprint('default_table_blueprint', __name__)


@default_table_blueprint.route('', methods=['GET'])
def default_setup():
    category_data = db.session.query(VocabularyTerm).join(VocabularyCategory) \
        .group_by(VocabularyCategory.name) \
        .with_entities(
        VocabularyCategory.name.label('categoryName'),
        func.count(VocabularyTerm.id).label('rowCount'),
        func.count(case([(func.array_length(VocabularyTerm.french, 1) > 1, 1)])).label('synonymRowCount'),
        func.count(case([(func.array_length(VocabularyTerm.antonym, 1) > 0, 1)])).label('antonymRowCount')
    ) \
        .order_by(text('"rowCount" DESC'))
    return {
        'tableData'    : [
            {
                'key'               : 1,
                'sectionPrompt'     : 'English to French. Try your best!',
                'numOfQuestions'    : 5,
                'questionGenerators': [
                    {
                        'key'           : 1,
                        'questionType'  : 'en-fr',
                        'categories'    : ['Food', 'Personalities'],
                        'numOfQuestions': 5,
                    }
                ]
            },
        ],
        'questionTypes': {
            'en-fr' : 'English to French',
            'fr-en' : 'French to English',
            'fr_syn': 'French Synonym',
            'fr_ant': 'French Antonym',
        },
        'categories'   : [result._asdict() for result in category_data]
    }
