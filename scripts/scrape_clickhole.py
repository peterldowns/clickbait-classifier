#!/usr/bin/env python
# coding: utf-8
import json
import requests
import sys
from lxml import html


def parse_clickhole_item(html_element):
  link = html_element.find('a')
  article_title = link.get('title').strip()
  article_url = link.get('href')
  data = {
      'article_title': article_title,
      'article_url': article_url,
      'clickbait': 1,
    }
  return data


def scrape_clickhole_titles(num_pages, start_page=1):
  url_template = 'http://www.clickhole.com/features/articles/?page={page}'
  data = []
  for p in xrange(start_page, start_page + num_pages):
    url = url_template.format(page=p)
    page_request = requests.get(url)
    if page_request.status_code != 200:
      sys.stderr.write(
          'Received status code %d: %s\n' % (page_request.status_code, url))
      break
    root = html.fromstring(page_request.content)
    data.extend(map(parse_clickhole_item, root.xpath('//article')))
    sys.stderr.write('Parsed %s\n' % url)
  return data


if __name__ == '__main__':
  sys.stdout.write(json.dumps(scrape_clickhole_titles(28), indent=2))
