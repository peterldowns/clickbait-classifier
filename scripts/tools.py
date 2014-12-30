# coding: utf-8
import json
import sys
from itertools import imap
from itertools import izip
from operator import itemgetter


def unique_articles(data):
  return dict(izip(imap(itemgetter('article_title'), data), data)).values()

def merge_files(data_filenames):
  data = []
  for name in data_filenames:
    with open(name, 'rb') as f:
      data.extend(json.load(f))
  return unique_articles(data)

def convert_to_parts_of_speech(headline):
  import nltk
  return ' '.join(
      map(itemgetter(1), # Parts of speech
          nltk.pos_tag(nltk.word_tokenize(headline.lower()))))

def convert_file_to_parts_of_speech(filename):
  with open(filename, 'rb') as fin:
    article_data = json.load(fin)

  outfilename = '.pos.'.join(filename.rsplit('.', 1))
  with open(outfilename, 'w') as fout:
    for article in article_data:
      article['article_title'] = convert_to_parts_of_speech(
          article['article_title'])
    json.dump(article_data, fout, indent=2)
