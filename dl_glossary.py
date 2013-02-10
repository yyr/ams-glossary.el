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


def get_titles(index_urls):
    """ Get titles list.
    """
    # from bs4 import BeautifulSoup
    titls_list = []

    for u  in index_urls:
        url = GL_URL_PREFIX + u
        page = get_save_page(url)
        reg = re.compile('<a href="([^"]*)" title="([^"]*)">.*</a></td>')
        matches = re.findall(reg,page)
        titls_list = matches + titls_list
        # soup = BeautifulSoup(page)
        # soup.prettify()
        # tbody = soup.tbody
        # title="46deg lateral arcs" href="/wiki/46deg_lateral_arcs">

    return titls_list

def fetch_all_pages():
    titles_p = os.path.join(DATA_DIR,"titles.p")

    if not os.path.exists:
        print("camehere")
        l = get_index_list()
        titles = get_titles(l)
        pickle.dump(titles, open(titles_p,"wb"))
    titles = pickle.load(open(titles_p,"rb"))

    # for val in reversed(titles):
    #     print(val)

def main():
    fetch_all_pages()

if __name__ == '__main__':
    main()
