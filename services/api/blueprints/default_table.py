from flask import Blueprint
from db import VocabularyCategory, db

default_table_blueprint = Blueprint('default_table_blueprint', __name__)


@default_table_blueprint.route('', methods=['GET'])
def default_setup():
    categories = db.session.query(VocabularyCategory.name).all()
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
        'categories'   : categories
    }
