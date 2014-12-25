#!/usr/bin/env python
# coding: utf-8
import json
import sys
from itertools import imap
from itertools import izip
from operator import itemgetter

def combine_data(data_filenames):
  data = []
  for name in data_filenames:
    with open(name, 'rb') as f:
      data.extend(json.load(f))
  data_dict = dict(izip(imap(itemgetter('article_title'), data), data))
  return data_dict.values()
