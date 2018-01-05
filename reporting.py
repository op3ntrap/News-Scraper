"""
@author=op3ntrap@gmail.com
"""
# -*- coding:utf-8 -*-

import json

import pdfkit
import requests
from readability import Document
from requests.exceptions import ConnectionError

from mercury_api import KEY
from scraper import save_output

"""
Sample HTTP GET request for using the mercury reader API
https://mercury.postlight.com/parser?url=https://trackchanges.postlight.com/building-awesome-cms-f034344d8ed
    Content-Type: application/json
    x-api-key: 37dsyrDmyOwXwplLsPgWraLTSpKQKnCIVLR3B1R0
"""


def parse_content_from_url_using_mercury(url):
    # Dict Containing the headers for the HTTP request.
    header_dict = {
        'content-type': 'application/json',
        'x-api-key'   : KEY
    }
    # Process the request
    data = requests.get(
            'https://mercury.postlight.com/parser?url=' + url,
            headers=header_dict)
    data_content = json.loads(data.content)
    return data_content['content'].encode(encoding='utf-8')


def snippet():
    test_url = 'https://byjus.com/free-ias-prep/upsc-2017-comprehensive-news-analysis-dec05'
    content = parse_content_from_url_using_mercury(test_url)
    with open('test.html', "w+") as fp:
        fp.write('<HTML><BODY>')
        fp.write(content)
        fp.write('\n</HTML></BODY>')


def parse_content_from_url_using_readability(url):
    try:
        response = requests.get(url)
    except ConnectionError as e:
        response = requests.get(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/220px-Emblem_of_India.svg.png")
    doc = Document(response.text)
    return doc.summary()


def execute(test_url):
    content = parse_content_from_url_using_readability(test_url)
    pdfkit.from_string(content, 'out.pdf')


def generate_stubs():
    with open('categorical_links.json', 'r') as fp:
        data = json.load(fp)
    # All the category titles are of the form <string>:<string>-Topic or <string>:<string> or <string>

    data = data['List']
    # All string parts are going to be addressed as stubs
    stubs = {}
    for val in data:
        title = val['title']
        if ':' in title:  # check whether the title is of the first or second type
            if '-' in title:
                stub_list = title.split('-')  # split the title around the hyphen and add the 1st one to the dict
                if stub_list[0] in stubs:  # add key if it is not there
                    stubs[stub_list[0]].append(val)
                else:
                    stubs[stub_list[0]] = [val]  # increase count if the key is present
            else:
                stub_list = title.split(':')
                if stub_list[0] in stubs:
                    stubs[stub_list[0]].append(val)
                else:
                    stubs[stub_list[0]] = [val]

        else:
            if title not in stubs:  # if the title is of the third type
                # then add it to the dictionary if it doesn't exists or increase its count
                stubs[title] = [val]
            else:
                stubs[title].append(val)
    save_output(stubs, 'stubs_list.json')

# if __name__ == '__main__':
#	# generate_stubs()
#	with open('stubs_list.json', 'r') as fp:
#		data = json.load(fp)
#	data = data['List']
#	# print type(data)
#	for key in data:
#		if "Comprehensive" in key:  # Check whether that stub is popular
#			content = ""
#			for url_dict in tqdm(data[key]):
#				try:
#					payload = parse_content_from_url_using_readability(url_dict['url'])
#				except:
#					continue
#				content += payload + "\n\n\n\n"
#			try:
#				pdfkit.from_string(content.encode(encoding='utf-8'), "{}.pdf".format(key))
#			except:
#				print "hello"
#			with open('{}.html'.format(key), 'w+') as fp:
#				fp.write(content.encode(encoding='utf-8'))
