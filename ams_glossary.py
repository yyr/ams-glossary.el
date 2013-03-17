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
from bs4 import BeautifulSoup

GL_URL_PREFIX = "http://glossary.ametsoc.org"
file_path = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
DATA_DIR = os.path.join(file_path,'data')


def get_save_page(url,local_file = None):
    """fetch given url and save it to data directory.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if local_file is None:
        local_file = url.split('/')[-1]

    local_file = os.path.join(DATA_DIR ,  local_file)

    if os.path.exists(local_file):
        fh = open(local_file, "rb")
        print(local_file + " is already exists, skipping ..")
        page = fh.read()
        return page

    else:
        print("Fetching.. '" + url + "' saving as " + local_file)
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


class AmsGlossary(object):
    """ """
    def __init__(self):
        self.base_url = "http://glossary.ametsoc.org"
        self.index_url = "http://glossary.ametsoc.org/wiki/Special:AllPages"
        self.titles = self.get_titles()

    def get_index_list(self):
        """ Get list of index files."""
        index_urls = []
        page = get_save_page(self.index_url)
        soup = BeautifulSoup(page)
        pages_chunk = soup.find('table', attrs={'class':"allpageslist"})
        links = pages_chunk.findAll('a')
        for link  in links:
            index_urls.append(link.get('href'))

        return set(index_urls)      # uniquify


    def parse_titles(self):
        """ Get titles list. """
        self.index_urls = self.get_index_list()

        titles = {}
        for u  in self.index_urls:
            url = GL_URL_PREFIX + u
            page = get_save_page(url)
            soup = BeautifulSoup(page)
            pages_chunk = soup.find('table', attrs={'class':"mw-allpages-table-chunk"})
            links = pages_chunk.findAll('a')
            for link in links:
                titles[link.get('title')] = link.get('href')

        return titles


    def get_titles(self):
        titles_p = os.path.join(DATA_DIR,"titles.p")

        if not os.path.exists(titles_p):
            titles = self.parse_titles()
            pickle.dump(titles, open(titles_p,"wb"))

        titles = pickle.load(open(titles_p,"rb"))
        return titles

    def fetch_all_pages(self):
        for key in self.titles:
            print(key)


def get_caseinsensitive_key(d,k):
    return [key for key in d if key.lower() == k.lower()]

def title_search(ks,word):
    searchedKeys = [key for key in ks
                    if word.lower() in key.lower()]
    print('  ' + '\n  '.join(searchedKeys))



def arg_parse(word=None,
              search=None):
    glossary = AmsGlossary()

    if word is not None:
        key = get_caseinsensitive_key(glossary.titles,word)
        if len(key) == 1:
            print('Entry found as: ' +  ' '.join(key))
            print(glossary.titles[key[0]])
        else:
            print('No exact entry found, continue to look title..')
            title_search(glossary.titles.keys(),word)

    elif search is not None:
        title_search(glossary.titles.keys(),search)


def main(args=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('word',nargs='?')
    parser.add_argument('-s','--search')
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        arg_parse(**vars(parser.parse_args(args)))


if __name__ == '__main__':
    main()
