#!/usr/bin/env python
# coding: utf-8
import json
import requests
import sys
from lxml import html


def parse_buzzfeed_item(html_element):
  author_marker = html_element.find_class('fa-user')[0]
  author_meta_node = author_marker.getparent()
  author_node = author_meta_node.find('a')
  author_name = author_node.text_content()
  author_url = author_node.get('href')

  article_node = html_element.find_class('lede__link')[1]
  article_title = article_node.text_content().strip()
  article_url = article_node.get('href')

  response_node = html_element.find_class('lede__meta__item')[3].find('a')
  response_count = int(response_node.text_content().split(' ')[0])

  return {
      'author': {
        'name': author_name,
        'url': author_url,
      },
      'article_title': article_title,
      'article_url': article_url,
      'response_count': response_count,
      'clickbait': 1,
    }


def scrape_buzzfeed_titles(url_template, num_pages, start_page):
  data = []
  for p in xrange(start_page, start_page + num_pages):
    url = url_template.format(page=p)
    page_request = requests.get(url)
    if page_request.status_code != 200:
      sys.stderr.write(
          'Received status code %d: %s\n' % (page_request.status_code, url))
      break
    root = html.fromstring(page_request.content)
    data.extend(map(parse_buzzfeed_item, root.find_class('lede')))
    sys.stderr.write('Parsed %s\n' % url)
  return data


def scrape_buzzfeed_buzz(pages, start_page=2):
  return scrape_buzzfeed_titles('http://www.buzzfeed.com/buzz?p={page}',
                                pages,
                                start_page)


def scrape_buzzfeed_news(pages, start_page=2):
  return scrape_buzzfeed_titles('http://www.buzzfeed.com/news?p={page}',
                                pages,
                                start_page)


def scrape_buzzfeed_life(pages, start_page=2):
  return scrape_buzzfeed_titles('http://www.buzzfeed.com/life/all?p={page}',
                                pages,
                                start_page)


if __name__ == '__main__':
  data = []
  #data.extend(scrape_buzzfeed_life(50, 2))
  data.extend(scrape_buzzfeed_buzz(100, 2))
  #data.extend(scrape_buzzfeed_news(30, 2))
  sys.stdout.write(json.dumps(data, indent=2))
