#quicksearch
On March 19, 2013 a friend and I challenged ourselves to build out the basic functionality of a search engine - a web crawler, an index and a way of querying the index - in 3 hours. The goal was not to build the most beautiful search engine nor to build the most fully-featured. Instead, we aimed to push the limits of simplicity - to see how much we could pare down what we would 'expect' to need to implement with a search engine while still making something that worked. 

This is what we came up with.

##How it works
### the Crawler
The crawler moves in a breadth-first fashion from its seed page(s) through all of their links (til stopped). Currently, 100 threads are used, with a crawler process allocated to each one.
- a ```to_crawl``` queue is maintained to track position of the crawler
- links are put in the queue when the parent page (page on which the link originally appeared) is indexed
- a ```crawled_or_queued``` set is used to keep track of visited (or soon-to-be-visited) sites
- Requests is used to get page content
- BeautifulSoup is used to parse it

###the Index
The index is a simple inverse index, implemented as a dictionary which is maintained in memory for the duration of the program
- search_index.keys: words found in the pages
- search_index.values: list of urls
- ```to_be_indexed``` queue is used to maintain the (url,data) to be indexed next 
- all content from h1 to h5 tags and p tags is indexed

###the Querying
Because the index is just a dictionary, querying is as simple as getting the values for a given key/word

##Simplifications
* no database is used (the index is not persistent)
* object-orientation is eschewed for simplicity (and, as it turned out, possibly pure functionality)
* any status code from an http requests other than '200' simply results in the get_page_text function returning immediately
* HTMLParseErrors are handled but not investigated
* complex queries are not handled (would simply result in a KeyError being raised)
* all single words in the appropriate tags are indexed in the same way (no matter where they appear on the page)

##How to use it
###Requirements
* BeautifulSoup4
* Requests

From the command line:
```bash
$ python crawler.py 
```

To Query:
* keyboard interrupt and enter a search term

##Contents
* __crawler.py__
* requirements.txt

##Status
This project is not currently being actively developed, but picking up where we left off would entail:

##To-Dos
* improve the UI (there's a lot of junk printed to the screen unnecessarily)
* add persistence to the index (currently it only exists for the duration of the program)

##Bugs
* keyboard interrupting doesn't kill the other threads running, so there is both a lot of visual noise (printed from the other threads used in the crawler) and the search term is not effectively captured for processing
=> Possible fix: in the KeyboardInterrupt exception, either kill the remaining threads or redirect their output away from stdout
