"""
@author=op3ntrap@gmail.com
"""
import json

import requests
from bs4 import BeautifulSoup


def scrape_urls_day_wise(url):
    soup = BeautifulSoup(requests.get(url).content, "html5lib")

    # Need to look for the table rows in the calendar widget
    # In the table rows scrape elements which have links
    div_table_element = soup.findAll('div', 'widget widget_calendar')

    # find all the cells in the table with a link in it
    links = []
    table_cells = div_table_element[0].findAll('td')
    for td in table_cells:
        r = td.find('a')
        try:
            # href in the anchor element has the link value. Using attributes of the BeautifulSoup endpoint get the link value
            link = r.attrs['href']
            links.append(link)
        except AttributeError:
            continue
    return links


def scrape_month_wise_urls():
    # All month urls are of the below format
    monthly_base_url = 'https://byjus.com/free-ias-prep/2017/{MM}'
    monthly_urls = ['https://byjus.com/free-ias-prep/2017/0{}'.format(str(n)) for n in range(6, 10)]
    monthly_urls.extend(['https://byjus.com/free-ias-prep/2017/10', 'https://byjus.com/free-ias-prep/2017/11'])

    # Finally visit every month's url and get the links for the news date analysis
    master_dir = []  # All results will be appended to this list
    for month in monthly_urls:
        links = scrape_urls_day_wise(month)
        master_dir.append(links)

    return master_dir


# Execute the function here!
master_dir = scrape_month_wise_urls()


def save_output(data, filename):
    """
    Method to save script results to a JSON object
    :param data: Data that is to be written to a file
    :return: 0 (void)
    """
    results = {"List": data}
    with open(filename, "w+") as fp:
        json.dump(results, fp)
    return 0


# Subroutine to save the results.
save_output(master_dir, filename='day_wise_links.json')
