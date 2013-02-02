#!/usr/bin/env python
'''
This script parses AMS glossary mediawiki site for list of title pages.
'''

DATE = "Saturday, February  2 2013"
AUTHOR = "Yagnesh Raghava Yakkala"
WEBSITE = "http://"
LICENSE ="GPL v3 or later"

GL_URL_LIST_PREFIX= "http://glossary.ametsoc.org/index.php?title=Special:AllPages"

import string
import re
import urllib2
from HTMLParser import HTMLParser

class TitleHTMLParser(HTMLParser):
    titles_list = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "title":
                    self.titles_list.append(value)

def main():
    letters = string.ascii_uppercase
    # p = 'test.html'
    # page = open(p)
    # parser = TitleHTMLParser()
    # parser.feed(page.read())

    all_titles = []
    for l in letters:
        gl_url =  GL_URL_LIST_PREFIX + "/%s" % l
        print("Fetching.. " + gl_url)
        r = urllib2.Request(url=gl_url)
        page = urllib2.urlopen(r).read()

        parser = TitleHTMLParser()
        parser.feed(page)
        all_titles = all_titles + parser.titles_list

    print(all_titles)

if __name__ == '__main__':
    main()
