#!/usr/bin/env python
# coding: utf-8

# Sources for machine learning information / examples:
#   http://nbviewer.ipython.org/gist/rjweiss/7158866
#   http://scikit-learn.org/stable/modules/feature_extraction.html
#   http://www.datarobot.com/blog/classification-with-scikit-learn/
#   http://scikit-learn.org/stable/auto_examples/document_classification_20newsgroups.html
#   http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

# TODO(peter):
#   - Use NLTK to map (sentence of words) -> (list of parts of speech)
#   - Store trained state
#   - Flask frontend / API
#   - Incremental training tool (show a title to N people, get consensus on
#     'is-clickbait')

import json
import numpy
import signal
import sys
import nltk
from itertools import imap
from operator import itemgetter
from random import shuffle
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


with open('./data/nytimes.json', 'rb') as nytimes_f:
  nyt_dataset = json.load(nytimes_f)
with open('./data/buzzfeed.json', 'rb') as buzzfeed_f:
  buzzfeed_dataset = json.load(buzzfeed_f)
with open('./data/clickhole.json', 'rb') as clickhole_f:
  clickhole_dataset = json.load(clickhole_f)

training_proportion = 0.75

nyt_cutoff = int(round(len(nyt_dataset) * training_proportion))
training_nyt = nyt_dataset[0:nyt_cutoff]
testing_nyt = nyt_dataset[nyt_cutoff:]

buzzfeed_cutoff = int(round(len(buzzfeed_dataset) * training_proportion))
training_buzzfeed = buzzfeed_dataset[0:buzzfeed_cutoff]
testing_buzzfeed = buzzfeed_dataset[buzzfeed_cutoff:]

clickhole_cutoff = int(round(len(clickhole_dataset) * training_proportion))
training_clickhole = clickhole_dataset[0:clickhole_cutoff]
testing_clickhole = clickhole_dataset[clickhole_cutoff:]

training_data = training_nyt + training_buzzfeed + training_clickhole
testing_data = testing_nyt + testing_buzzfeed + testing_clickhole

assert (len(training_data) + len(testing_data)) == (
        len(nyt_dataset) + len(buzzfeed_dataset) + len(clickhole_dataset))

def title_cleaner(title):
  # Comment out the following line to train on parts of speech instead of the
  # actual words.
  return title
  return ' '.join(
      map(itemgetter(1), # Parts of speech
      nltk.pos_tag(nltk.word_tokenize(title.lower()))))

def category_cleaner(category):
  return 'clickbait' if category else 'news'

article_titles = map(title_cleaner,
                     imap(itemgetter('article_title'), training_data))
clickbait_values = map(category_cleaner,
                       imap(itemgetter('clickbait'), training_data))
X_train = numpy.array(article_titles)
Y_train = numpy.array(clickbait_values)
assert len(X_train) == len(Y_train) > 0

test_article_titles = map(title_cleaner,
                          imap(itemgetter('article_title'), testing_data))
test_clickbait_values = map(category_cleaner,
                            imap(itemgetter('clickbait'), testing_data))
X_test = numpy.array(test_article_titles)
Y_test = numpy.array(test_clickbait_values)
assert len(X_test) == len(Y_test) > 0

vectorizer = TfidfVectorizer(ngram_range=(1, 3),
                             lowercase=True,
                             stop_words='english',
                             strip_accents='unicode',
                             min_df=2,
                             norm='l2')

X_train = vectorizer.fit_transform(X_train) # Fit and then transform
nb_classifier = MultinomialNB()
nb_classifier.fit(X_train, Y_train)

X_test = vectorizer.transform(X_test)
Y_predicted = nb_classifier.predict(X_test)

print 'Classification report:'
print metrics.classification_report(Y_test, Y_predicted)
print ''

def show_most_informative_features(vectorizer, clf, n=20):
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
    for (coef_1, fn_1), (coef_2, fn_2) in top:
        print "\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2)

print show_most_informative_features(vectorizer, nb_classifier, 50)

# Set up a loop to test article titles against the trained classifier.
signal.signal(signal.SIGINT,
              lambda signal, frame: sys.stdout.write('\n') or sys.exit(0))
while 1:
  title = raw_input('\nArticle title: ').strip()
  predictions = nb_classifier.predict_proba(
      vectorizer.transform(numpy.array([title_cleaner(title)])))[0]
  probabilities = dict(zip(nb_classifier.classes_, predictions))
  print '{0:.2f}% chance of clickbait'.format(probabilities['clickbait'] * 100)
