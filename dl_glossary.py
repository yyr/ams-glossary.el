#!/usr/bin/env python
'''
Download all pages from AMS glossary site.
'''

DATE = "Saturday, February  2 2013"
AUTHOR = "Yagnesh Raghava Yakkala"
WEBSITE = "http://github.com/yyr/ams-glossary.el"
LICENSE ="GPL v3 or later"

import sys
PY3 = (sys.version_info[0] >= 3 )

import pickle
import inspect

import os
import string
import re
import urllib2

GL_URL_PREFIX = "http://glossary.ametsoc.org"
file_path = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
DATA_DIR = os.path.join(file_path,'data')

def get_save_page(url,local_file = ''):
    """fetch given url and save it to data directory.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    local_file = os.path.join(DATA_DIR , url.split('/')[-1] + ".html")
    print("Fetching.. " + url)

    if os.path.exists(local_file):
        fh = open(local_file, "rb")
        print(local_file + " is already exists, skipping ..")
        page = fh.read()
        return page

    else:
        fh = open(local_file, "wb")
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        r = urllib2.Request(url=url,headers={'User-Agent' : user_agent})
        try:
            oh = urllib2.urlopen(r)
            page = oh.read()
            fh.write(page)
            return page
        except urllib2.URLError, e:
            print("URLError: %s" % e)
            sys.exit()
        except Exception:
            import traceback
            print('Generic exception: ' + traceback.format_exc())
            sys.exit()


def get_index_list(index_url = "http://glossary.ametsoc.org/wiki/Special:AllPages"):
    """ Get list of index files.
    """
    index_urls = []
    page = get_save_page(index_url)

    reg = re.compile('<td class="mw-allpages-alphaindexline"><a href="([^"]*)">')
    index_urls = re.findall(reg,page)
    index_urls = [ re.sub("&amp;", "&", l) for l in index_urls] #  decode ampersand
    re.findall("&amp;","&")
    return index_urls


def parse_titles(index_urls):
    """ Get titles list.
    """
    titles = {}
    from bs4 import BeautifulSoup

    for u  in index_urls:
        url = GL_URL_PREFIX + u
        page = get_save_page(url)
        # reg = re.compile('<a href="([^"]*)" title="([^"]*)">.*</a></td>')
        # matches = re.findall(reg,page)
        soup = BeautifulSoup(page)
        pages_chunk = soup.find('table', attrs={'class':"mw-allpages-table-chunk"})
        links = pages_chunk.findAll('a')
        for link in links:
            titles[link.get('title')] = link.get('href')

    return titles

def get_titles():
    titles_p = os.path.join(DATA_DIR,"titles.p")

    if not os.path.exists(titles_p):
        l = get_index_list()
        titles = parse_titles(l)
        pickle.dump(titles, open(titles_p,"wb"))

    titles = pickle.load(open(titles_p,"rb"))
    return titles

def fetch_all_pages():
    titles = get_titles()

def main():
    fetch_all_pages()

if __name__ == '__main__':
    main()
