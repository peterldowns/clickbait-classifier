#!/usr/bin/env python
# coding: utf-8
import json
import requests
import sys
from lxml import html
from tools import unique_articles

def parse_dose_item(html_element):
  title_wrapper = html_element.xpath('h4')[0]
  title_tag = title_wrapper.find('a')
  article_title = title_tag.text_content()
  article_url = title_tag.get('href')
  data = {
      'article_title': article_title,
      'article_url': article_url,
      'clickbait': 1,
    }
  return data


def scrape_dose_titles(num_pages, start_page=1):
  url_template = ('http://www.dose.com/primaryResponsiveFeed?'
                  'limit={num_items}'
                  '&page={page}'
                  '&infinite=1')
  data = []
  for p in xrange(start_page, start_page + num_pages):
    url = url_template.format(page=p, num_items=100)
    page_request = requests.get(url)
    if page_request.status_code != 200:
      sys.stderr.write(
          'Received status code %d: %s\n' % (page_request.status_code, url))
      break
    root = html.fromstring(page_request.content)
    data.extend(map(parse_dose_item, root.find_class('feed-item')))
    sys.stderr.write('Parsed %s\n' % url)
  return unique_articles(data)


  # url_template = (
  #     'http://www.dose.com/primaryResponsiveFeed?limit={num_items}&infinite=1')
  # data = []
  # url = url_template.format(num_items=num_items)
  # page_request = requests.get(url)
  # if page_request.status_code == 200:
  #   root = html.fromstring(page_request.content)
  #   data.extend(map(parse_dose_item, root.find_class('feed-item')))
  #   sys.stderr.write('Parsed %s\n' % url)
  # else:
  #   sys.stderr.write(
  #       'Received status code %d: %s\n' % (page_request.status_code, url))
  # return data


if __name__ == '__main__':
  sys.stdout.write(json.dumps(scrape_dose_titles(40), indent=2))
