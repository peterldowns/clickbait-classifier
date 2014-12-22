#!/usr/bin/env python
# coding: utf-8
# http://nbviewer.ipython.org/gist/rjweiss/7158866
import json
import numpy
from operator import itemgetter
from random import shuffle
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


dataset = []
with open('nytimes.json', 'rb') as nytimes_f:
  dataset.extend(json.load(nytimes_f))
with open('buzzfeed-crawl.json', 'rb') as buzzfeed_f:
  dataset.extend(json.load(buzzfeed_f))
shuffle(dataset)

training_set_size = int(round(len(dataset) * 0.90))
training_data = dataset[0:training_set_size]
testing_data = dataset[(training_set_size + 1):]


article_titles = map(itemgetter('article_title'), training_data)
clickbait_values = map(itemgetter('clickbait'), training_data)
X_train = numpy.array(article_titles)
Y_train = numpy.array(clickbait_values)
assert len(X_train) == len(Y_train) > 0

X_test = numpy.array(map(itemgetter('article_title'), testing_data))
Y_test = numpy.array(map(itemgetter('clickbait'), testing_data))
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

print "MODEL: Multinomial Naive Bayes\n"
print 'The precision for this classifier is ' + str(metrics.precision_score(Y_test, Y_predicted))
print 'The recall for this classifier is ' + str(metrics.recall_score(Y_test, Y_predicted))
print 'The f1 for this classifier is ' + str(metrics.f1_score(Y_test, Y_predicted))
print 'The accuracy for this classifier is ' + str(metrics.accuracy_score(Y_test, Y_predicted))

print '\nHere is the classification report:'
print metrics.classification_report(Y_test, Y_predicted)

print '\nHere is the confusion matrix:'
print metrics.confusion_matrix(Y_test, Y_predicted, labels=[0, 1])

while 1:
  title = raw_input('\nArticle title: ').strip()
  probabilities = nb_classifier.predict_proba(
      vectorizer.transform(numpy.array([title])))[0]
  clickbait_probability = probabilities[1]
  print '{0:.2f}% chance of clickbait'.format(clickbait_probability * 100)
