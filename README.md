# Kahoot-Gen

A website that generates [Kahoot](https://kahoot.com) questions for French vocabulary and conjugation. It's up
now [here](kahootgen.me)!

Most vocabulary was sourced from [Lawless French](https://lawlessfrench.com). In
addition, [Dictionnaire-Synonyme](https://dictionnaire-synonyme.com) and
[Google Translate](https://translate.google.com) were used as sources for synonyms and antonyms for certain words.

Other than the web server, you can use the jupyter notebook located
in [the api folder](https://github.com/Raragyay/Kahoot-Gen/blob/master/services/api/French.ipynb). To use, edit the
question_entries variable with the type of question and the category you wish to test.

I have also scraped and pickled the top 10000 and top 2000 most popular French words from
[Wikitionary](https://en.wiktionary.org/wiki/Wiktionary:French_frequency_lists/1-2000). To extract them, you can use a
script similar to the following:

```python
import pickle
with open('top10kwords.pkl', 'rb') as f:
    words_list10k = pickle.load(f)
```

I also have a list of unique vocabulary in `Master Pronunciation.csv` that you may find useful. All words there were
hand-picked, with the latter ones mostly coming from `top10kwords.pkl`.

### Todo List

- [x] Add parameterized creation of questions
- [x] Convert API into a Docker Container
- [x] Build front-end
- [x] [Deploy](kahootgen.me)
- [ ] Provide stats on vocabulary categories
- [ ] Add conjugation support for website
- [ ] Support other kahoot-like websites. 