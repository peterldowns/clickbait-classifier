#!/usr/bin/env python
# coding: utf-8

# Sources for machine learning information / examples:
#   http://nbviewer.ipython.org/gist/rjweiss/7158866
#   http://scikit-learn.org/stable/modules/feature_extraction.html
#   http://www.datarobot.com/blog/classification-with-scikit-learn/
#   http://scikit-learn.org/stable/auto_examples/document_classification_20newsgroups.html
#   http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

# TODO(peter):
#   - Store trained state
#   - Flask frontend / API
#   - Incremental training tool (show a title to N people, get consensus on
#     'is-clickbait')

import glob
import json
import numpy
import sys
import nltk
from itertools import imap
from operator import itemgetter
from random import shuffle
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


# Make this `True` to train on parts of speech instead of words.
TRAIN_ON_PARTS_OF_SPEECH = False
if TRAIN_ON_PARTS_OF_SPEECH:
  data_files = glob.glob('./data/pos/*.json')
  def title_cleaner(title):
    import nltk
    return ' '.join(
        map(itemgetter(1), # Parts of speech
            nltk.pos_tag(nltk.word_tokenize(title.lower()))))
else:
  data_files = glob.glob('./data/*.json')
  def title_cleaner(title):
    return title


# All of these complicated splits are used to ensure that there are both types
# of article titles (clickbait and news) in the training set.
training_proportion = 0.8
training_data = []
testing_data = []
for filename in data_files:
  with open(filename, 'rb') as in_f:
    dataset = json.load(in_f)
    cutoff = int(round(len(dataset) * training_proportion))
    training_data.extend(dataset[0:cutoff])
    testing_data.extend(dataset[cutoff:])
    print 'Loaded %d headlines from %s' % (len(dataset), filename)

def category_cleaner(category):
  return 'clickbait' if category else 'news'

article_titles = map(itemgetter('article_title'), training_data)
clickbait_values = map(category_cleaner,
                       imap(itemgetter('clickbait'), training_data))
test_article_titles = map(itemgetter('article_title'), testing_data)
test_clickbait_values = map(category_cleaner,
                            imap(itemgetter('clickbait'), testing_data))

X_train = numpy.array(article_titles)
Y_train = numpy.array(clickbait_values)
X_test = numpy.array(test_article_titles)
Y_test = numpy.array(test_clickbait_values)
assert len(X_train) == len(Y_train) > 0
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

show_most_informative_features(vectorizer, nb_classifier, 20)

def classify(title):
  predictions = nb_classifier.predict_proba(
      vectorizer.transform(numpy.array([title_cleaner(title)])))[0]
  probabilities = dict(zip(nb_classifier.classes_, predictions))
  return probabilities
