#!/usr/bin/env python
# coding: utf-8
import signal
import sys

print 'Loading classifier (may take time to train.)'
import classifier
print 'Done.'

# Set up a loop to test article titles against the trained classifier.
# Quit cleanly when encoutering c-C.

signal.signal(signal.SIGINT,
              lambda signal, frame: sys.stdout.write('\n') or sys.exit(0))

while True:
  try:
    title = raw_input('\nArticle title: ').strip().decode('utf-8')
  except:
    break
  probabilities = classifier.classify(title)
  print '({0:.2f}% clickbait, {1:.2f}% news) -> {2}'.format(
      probabilities['clickbait'] * 100,
      probabilities['news'] * 100,
      'news' if probabilities['news'] >= 0.5 else 'clickbait')
