# French Teaching

A Jupyter Notebook that generates [Kahoot](kahoot.com) questions for French vocabulary and conjugation.

Most vocabulary was sourced from [Lawless French](lawlessfrench.com). 
In addition, [Dictionnaire-Synonyme](dictionanaire-synonyme.com) and
[Google Translate](translate.google.com) were used as sources for synonyms and antonyms for certain words. 

To use, edit the question_entries variable with the type of question and the category you wish to test.

I have also scraped and pickled the top 10000 and top 2000 most popular French words from 
[Wikitionary](https://en.wiktionary.org/wiki/Wiktionary:French_frequency_lists/1-2000). To extract them, you can use 
a script similar to the following:
```python
import pickle
with open('top10kwords.pkl', 'rb') as f:
    words_list10k = pickle.load(f)
```

### Todo List
- [ ] Add configuration file for question types
- [ ] Extract Notebook into separate script, package as exe
- [ ] Support other kahoot-like websites. 