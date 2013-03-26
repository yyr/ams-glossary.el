#!/usr/bin/env python
'''Define a meteorological title from AMS glossary. By default this program
fetches a page from AMS glossary website. For offline reading you can download
all pages from AMS glossary website.
'''

DATE = "Saturday, February  2 2013"
AUTHOR = "Yagnesh Raghava Yakkala"
WEBSITE = "http://github.com/yyr/ams-glossary.el"
LICENSE ="GPL v3 or later"

import sys
PY3 = (sys.version_info[0] >= 3 )

import inspect, os
import pickle
import urllib2
from bs4 import BeautifulSoup

GL_URL_PREFIX = "http://glossary.ametsoc.org"
file_path = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
DATA_DIR = os.path.join(file_path,'data')
PAGES_DIR = os.path.join(file_path,'pages') # location to keep downloaded html pages.

def get_save_page(url,local_file = None):
    """fetch given url and save it to data directory.
    """
    if not os.path.exists(PAGES_DIR):
        os.makedirs(PAGES_DIR)

    if local_file is None:
        local_file = url.split('/')[-1]

    local_file = os.path.join(PAGES_DIR ,  local_file)

    if os.path.exists(local_file):
        fh = open(local_file, "rb")
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

def get_caseinsensitive_key(d,k):
    return [key for key in d if key.lower() == k.lower()]

class AmsGlossary(object):
    """Ams glossary data class. Pages, Titles, Fetch ala.."""
    def __init__(self):
        self._titles_p = os.path.join(DATA_DIR,"titles.p")
        self._base_url = "http://glossary.ametsoc.org"
        self._index_url = "http://glossary.ametsoc.org/wiki/Special:AllPages"
        self.titles = self.get_titles()

    def get_index_list(self):
        """ Get list of index files."""
        index_urls = []
        page = get_save_page(self._index_url)
        soup = BeautifulSoup(page)
        pages_chunk = soup.find('table', attrs={'class':"allpageslist"})
        links = pages_chunk.findAll('a')
        for link  in links:
            index_urls.append(link.get('href'))

        return set(index_urls)      # uniquify


    def parse_titles(self):
        """ Get titles list. """
        self._index_urls = self.get_index_list()

        titles = {}
        for u  in self.index_urls:
            url = GL_URL_PREFIX + u
            page = get_save_page(url)
            soup = BeautifulSoup(page)
            pages_chunk = soup.find(
                'table', attrs={'class':"mw-allpages-table-chunk"})
            links = pages_chunk.findAll('a')
            for link in links:
                titles[link.get('title')] = link.get('href')
        return titles

    def title_url(self,title):
        return self._base_url + self.titles[title]

    def define_title(self,title,form='text'):
        """return given title. form argument either text or raw
        """
        page = self.fetch_title_page(title)
        soup = BeautifulSoup(page)
        page_chunk = soup.find(
            'div', attrs={'class':"termentry"})
        if form=='html':
            return page_chunk
        else:
            return page_chunk.getText()

    def update_titles_list(self,force):
        if not os.path.exists(self._titles_p):
            titles = self.parse_titles()
            pickle.dump(titles, open(self._titles_p,"wb"))
        return

    def get_titles(self):
        return pickle.load(open(self._titles_p,"rb"))

    def fetch_title_page(self,title):
        return get_save_page(self.title_url(title))

    def fetch_all_title_pages(self):
        for title in self.titles.keys():
            self.fetch_title_page(title)
        return

    def build_database(self,force=False):
        self.ams_db_html = {}
        db_html = os.path.join(DATA_DIR,"ams_db_html")
        if force or not os.path.exists(db_html):
            for i, title in enumerate(self.titles.keys()):
                self.fetch_title_page(title)
                self.ams_db_html[title] = get_save_page(self.title_url(title))
            pickle.dump(self.ams_db_html, open(db_html,"wb"))
        else:
            print('Seems, there is already database available,'+
                  'Give --force option to build it from scratch.')
        return


def arg_parse(title=None, search=None,
              build_database=False,
              form=None,
              force=False):
    glossary = AmsGlossary()

    def title_search(ks,title):
        searchedKeys = [key for key in ks
                        if title.lower() in key.lower()]
        print('  ' + '\n  '.join(searchedKeys))

    if title is not None:
        key = get_caseinsensitive_key(glossary.titles,title)
        if len(key) == 1:
            print('Entry found as: ' +  ' '.join(key))
            print(glossary.define_title(key[0],form=form))
        else:
            print('No exact entry found, continue to look title..')
            title_search(glossary.titles.keys(),title)

    elif search is not None:
        title_search(glossary.titles.keys(),search)

    elif build_database:
        glossary.build_database(force)


def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=__doc__)
    parser.add_argument('title',nargs='?')

    parser.add_argument('-f','--format',dest='form',
                        default='text', choices=['html','text'])
    parser.add_argument('-s','--search')
    parser.add_argument('-bd','--build-database',action="store_true")
    parser.add_argument('--force',action="store_true")

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        arg_parse(**vars(parser.parse_args(args)))


if __name__ == '__main__':
    main()
