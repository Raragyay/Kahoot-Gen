from app import create_app
from constants import base_folder_path
from db import db, VocabularyCategory, VocabularyTerm
from vocab_dataframe import VocabDataframe
import pandas as pd

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    df: pd.DataFrame = VocabDataframe().df
    for category in df['Category'].cat.categories:
        category: str
        filtered_df = df[df['Category'] == category]
        cleaned_category_name = category.replace("_", " ").title()
        category_entry = VocabularyCategory(cleaned_category_name)
        db.session.add(category_entry)
        for row in filtered_df.iterrows():
            data = row[1]
            english = data['English']
            french = list(data['French'])
            antonym = list(data['Antonym'])
            term_entry = VocabularyTerm(english, french, antonym, category_entry)
            db.session.add(term_entry)

    db.session.commit()
