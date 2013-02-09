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

import os
import string
import re
import urllib2

GL_URL_PREFIX = "http://glossary.ametsoc.org/w"

def get_save_page(url,local_file = ''):
    """fetch given url and save it to data directory.
    """
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
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
        except URLError, e:
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
    return index_urls

def get_titles(index_urls):
    pass

def fetch_all_pages():
    pass

def main():
    print(get_index_list())

if __name__ == '__main__':
    main()
