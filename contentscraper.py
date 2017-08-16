# version 0.2
from bs4 import BeautifulSoup as bs
from urllib import urlopen
from urlparse import urljoin
from urlparse import urlparse
import sys
import re

class ContentScraper():
    url = None
    html = None
    soup = None
    text = None
    urlstring = None
    links = []
    pages = set()

    def __init__(self, url):
        self.url = url
        self.urlstring = urlparse(self.url).netloc
        self._connect_to_url()
    
    def _connect_to_url(self):
        self.html = urlopen(self.url).read()

    def _scrape_html(self):
        self.soup = bs(self.html, 'lxml')

    def _filter_html(self): # Removes styles and scripts
        for script in self.soup(['head', 'script', 'style']):
            script.extract()
        
        self.links = self.soup.find_all(href=True)

        for items in self.links:
            if items['href'].find(self.urlstring) == -1 and 'http' in items['href']:
                pass
            elif items['href'].find('mailto:') >=0:
                pass
            elif items['href'].find(self.urlstring) >= 0:
                self.pages.add(items['href'])
            else:
                temp = items['href']
                self.pages.add(urljoin(self.url, temp))

    def _cleanup_pages(self):
        templist = list(self.pages)
        for page in templist:
            if '#' in page:
                templist.remove(page)

        self.pages = set(templist)

    def _kill_extra_whitespace(self):
        self.text = re.sub(r'\n\s*\n', r'\n\n', self.soup.get_text().strip(), flags=re.M)

    def _page_crawler(self):
        self._cleanup_pages()
        for page in self.pages:
            temphtml = urlopen(page).read()
            tempsoup = bs(temphtml, 'lxml')
            temptitle = tempsoup.find_all('title')
            print temptitle

    def _output_result(self):
        print "\n\nPossible pages:\n"
        for items in self.pages:
            print items
        
    def run(self):
        self._scrape_html()
        self._filter_html()
        self._kill_extra_whitespace()
        self._page_crawler()
        self._output_result()

if __name__ == '__main__':
    scrape_content = ContentScraper(sys.argv[1])
    scrape_content.run()