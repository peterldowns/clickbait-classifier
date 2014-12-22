#!/usr/bin/env python
# coding: utf-8
# http://nbviewer.ipython.org/gist/rjweiss/7158866
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from operator import itemgetter
from sklearn.metrics import classification_report
import json
import numpy as np


dataset = []
with open('nytimes.json', 'rb') as nytimes_f:
  dataset.extend(json.load(nytimes_f))
with open('buzzfeed-crawl-2014-12-21.json', 'rb') as buzzfeed_f:
  dataset.extend(json.load(buzzfeed_f))

training_set_size = int(round(len(dataset) * 0.75))
training_data = dataset[0:training_set_size]
testing_data = dataset[(training_set_size + 1):]
print len(testing_data)

article_titles = map(itemgetter('article_title'), training_data)
clickbait_values = map(itemgetter('clickbait'), training_data)
X_train = np.array(article_titles)
Y_train = np.array(clickbait_values)

X_test = np.array(map(itemgetter('article_title'), testing_data))
Y_test = np.array(map(itemgetter('clickbait'), testing_data))

vectorizer = TfidfVectorizer(min_df=2,
                             ngram_range=(1, 2),
                             stop_words='english',
                             strip_accents='unicode',
                             norm='l2')

X_train = vectorizer.fit_transform(X_train) # Fit and then transform
nb_classifier = MultinomialNB().fit(X_train, Y_train)

X_test = vectorizer.transform(X_test)
Y_predicted = nb_classifier.predict(X_test)
print "MODEL: Multinomial Naive Bayes\n"
print 'The precision for this classifier is ' + str(metrics.precision_score(Y_test, Y_predicted))
print 'The recall for this classifier is ' + str(metrics.recall_score(Y_test, Y_predicted))
print 'The f1 for this classifier is ' + str(metrics.f1_score(Y_test, Y_predicted))
print 'The accuracy for this classifier is ' + str(metrics.accuracy_score(Y_test, Y_predicted))

print '\nHere is the classification report:'
print classification_report(Y_test, Y_predicted)

print '\nHere is the confusion matrix:'
print metrics.confusion_matrix(Y_test, Y_predicted, labels=[0, 1])

N = 10
print vectorizer.vocabulary_.items()
vocabulary = np.array([t for t, i in sorted(vectorizer.vocabulary_.iteritems(), key=itemgetter(1))])
for i, label in enumerate(clickbait_values):
  topN = np.argsort(nb_classifier.coef_[i])[-N:]
  print "\nThe top %d most informative features for topic code %s: \n%s" % (N, label, " ".join(vocabulary[topN]))

while 1:
  title = raw_input('\nArticle title: ').strip()
  print nb_classifier.predict(vectorizer.transform(np.array([title])))
