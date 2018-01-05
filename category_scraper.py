"""
@author=op3ntrap@gmail.com
"""

import json

import requests
from bs4 import BeautifulSoup

from scraper import save_output

with open('day_wise_links.json', 'r') as fp:
    data = json.load(fp=fp)


def date_wise_category_scraper(url):
    dump = []
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "lxml")
    entry_titles = soup.findAll('h2', 'entry-title')
    for html_element in entry_titles:
        anchor_element = html_element.find('a')
        payload = {'title': anchor_element.get('title'), 'url': anchor_element.get('href')}
        dump.append(payload)
    return dump


# data is of format {"List": list(list)}
results = []
data = data['List']
for url_list in data:
    for url in url_list:
        dump = date_wise_category_scraper(url)
        results.extend(dump)
save_output(results, 'categorical_links.json')
