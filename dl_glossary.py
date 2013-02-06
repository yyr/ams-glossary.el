#!/usr/bin/env python
'''
Download all pages from AMS glossary site.
'''

DATE = "Saturday, February  2 2013"
AUTHOR = "Yagnesh Raghava Yakkala"
WEBSITE = "http://"
LICENSE ="GPL v3 or later"


import sys
from os import path
PY3 = (sys.version_info[0] >= 3 )

import string
import re
import urllib2
import urlparse


GL_URL_PREFIX = "http://glossary.ametsoc.org/w"
GL_INDEX_URL = "http://glossary.ametsoc.org/wiki/Special:AllPages"
DATA_DIR = path.join(path.dirname(path.abspath(__file__)),"data")

def get_save_page(url):
    pass

def get_index_list(index_url):
    index_urls = []

    print("Fetching.. " + GL_INDEX_URL)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    r = urllib2.Request(url=GL_INDEX_URL,headers={'User-Agent' : user_agent})

    try:
        page = urllib2.urlopen(r).read()
    except URLError as e:
        print(e.reason)
        sys.exit()

    return None

def get_titles(index_urls):
    pass

def fetch_all_pages():
    pass

def main():
    print(DATA_DIR)
    # index_urls = get_index_list(GL_INDEX_URL)
    pass

if __name__ == '__main__':
    main()
