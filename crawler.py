
import requests
import HTMLParser
from bs4 import BeautifulSoup

import threading
from Queue import Queue
import urlparse
from pprint import pprint
import re

crawled_or_queued = set()
to_crawl = Queue()
to_be_indexed = Queue(maxsize=100)

search_index = {}

print '--------'

def normalize(url):
    return url if url.endswith('/') else url + '/'

def crawl():
    while True:
        print "Queue size before {}".format(to_be_indexed.qsize())
        url = to_crawl.get()
        to_be_indexed.put((url,get_page_text(url)))
        print "\033[94m Finished crawling {0} \033[0m \n Queue Size {1}".format(url,to_be_indexed.qsize())
def get_page_text(url):
    try:
        r = requests.get(url,allow_redirects=False)
    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema):
        return
    if r.status_code != 200:
        return
    return r.text

def index(url,text):
    try:
        s = BeautifulSoup(text)
    except HTMLParser.HTMLParseError:
        return
    for link in s.findAll('a'):
        abs_link_url = normalize(urlparse.urljoin(url, link.get('href')))
        if not abs_link_url in crawled_or_queued:
            crawled_or_queued.add(abs_link_url)
            to_crawl.put(abs_link_url)
    words = []
    for tag in s.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'p']):
        words.extend(get_words_from_tag(tag))
    
    for word in set(words):
        search_index.setdefault(word, []).append(url)
    print "Indexing Completed: {0}\n Queue Size {1}".format(url,to_be_indexed.qsize())

    
def get_words_from_tag(tag):
     return [''.join(re.findall(r'[a-zA-Z]', x)).lower() for x in tag.getText().split()]
    



if __name__ == '__main__':
    try:
        crawled_or_queued.add(u'http://www.nytimes.com/')
        to_crawl.put(u'http://www.nytimes.com/')
        for i in range(100):
            t = threading.Thread(target=crawl)
            t.daemon = True
            t.start()

        while True:
            print "Preparing to Index \n Queue Size {}".format(to_be_indexed.qsize())
            url, text = to_be_indexed.get()
            if text:
                index(url,text)
            print "Finished Index Attempt"
    except KeyboardInterrupt:
        pass
        # pprint(search_index)
        # print search_index.keys()

    while True:
        word = raw_input('enter search term!')
        if word in search_index:
            print "\n".join(set(search_index[word]))
        else:
            print 'sorry, no hits'


