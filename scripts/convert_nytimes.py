#!/usr/bin/env python
# coding: utf-8
import csv
import json
import sys


def parse_nyt_row(row):
  return {
      'article_id': row[0],
      'date': row[1],
      'article_title': row[2],
      'article_subject': row[3],
      'topic_code': row[4],
      'clickbait': 0,
    }


def load_nyt_csv(filename):
  data = []
  with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    reader.next() # Skip the header file
    for row in reader:
      row = map(lambda s: unicode(s, 'latin-1'), row)
      data.append(parse_nyt_row(row))
  return data


if __name__ == '__main__':
  nyt_data = load_nyt_csv('./data/rtexttools-nytimes.csv')
  sys.stdout.write(json.dumps(nyt_data, indent=2))
