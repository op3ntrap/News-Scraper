import json
import os

import pdfkit
from PyPDF2 import PdfFileMerger
from bs4 import BeautifulSoup
from tqdm import tqdm


def generate(limit):
    with open('stubs_list.json', 'r') as fp:  # import the stubs
        data = json.load(fp)
        data = data['List']
    news_list = []
    for val in data:
        if "Comprehensive News" in val:  # list of news analysis links
            news_list.extend(data[val])
    count = 0
    for val in tqdm(news_list):
        # content = parse_content_from_url_using_readability(val['url'])
        content = ""
        str2 = "news" + str(count) + ".html"
        with open(str2, 'w+') as fp:
            print "writing {}".format(val['title'])
            fp.write(content.encode('utf-8'))
            fp.flush()
            os.fsync(fp.fileno())
        count += 1
        if count == limit:
            for i in range(5):
                execute(i)
            break


def execute(index):
    with open('{}'.format(index), 'r') as fp:
        data = fp.read()
    soup = BeautifulSoup(data, "lxml")
    a = soup.findAll('div', 'paratitle1')  # Question Titles
    a += soup.findAll('button')  # Subscribe Button
    a += soup.findAll('img', {'title': 'Need Expert Guidance on how to prepare for Current Affairs'})  # Bulk Image
    a += soup.findAll('div',
                      'su-spoiler su-spoiler-style-default su-spoiler-icon-plus su-spoiler-closed')  # Answers and their explanation
    a += soup.findAll('span', 'su-dropcap su-dropcap-style-default')  # Junk "See"
    a += soup.findAll('p', {'id': 'Practice'})  # Title of the Question and Answer Sections
    a += soup.findAll('div', 'highlightbox')  # Advertisement
    test_series_ads = []
    malicious_strings = ["Also, check previous Daily News Analysis", "Click here", "Largest All-India Test Series"]
    for val in soup.findAll('p', 'p3'):
        d = val.findAll('span')
        for r in d:
            # print r.text
            e = r.findAll('a')
            if len(e) > 0 and any(malicious_string in r.text for malicious_string in malicious_strings):
                test_series_ads.append(val)
    for val in soup.findAll('pre'):
        d = val.findAll('span')
        for r in d:
            # print r.text
            e = r.findAll('a')
            if len(e) > 0 and any(malicious_string in r.text for malicious_string in malicious_strings):
                test_series_ads.append(val)
    a.extend(test_series_ads)
    delstr = [x.extract() for x in a]
    # type(soup.prettify())
    with open('modified_{}'.format(index), 'w+') as fp:
        fp.write(soup.prettify(encoding='utf-8'))


def make_pdf():
    files = os.listdir('.')
    options = {
        'quiet': True
    }
    merger = PdfFileMerger()
    content_pdfs = []
    for obj in files:
        if obj.startswith('modified') and obj.endswith('.html'):
            filename = obj[:-5] + ".pdf"
            pdfkit.from_file(obj, filename)
            content_pdfs.append(filename)
            merger.append(filename)
    merger.write("News_Analysis.pdf")


def make_pdf_pdfkit():
    files = os.listdir('.')
    options = {
        'minimum-font-size' : 30,
        'no-pdf-compression': None,
        'encoding'          : 'UTF-8'

    }
    # merger = PdfFileMerger()
    content_pdfs = []
    for obj in tqdm(range(190)):
        content_pdfs.append("modified_news{}.html".format(obj))
    pdfkit.from_file(input=content_pdfs, output_path="News Analysis(1).pdf", options=options)


make_pdf_pdfkit()
