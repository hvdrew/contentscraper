# version 0.1
from bs4 import BeautifulSoup as bs
from urllib import urlopen
import sys
import re

class ContentScraper():
    url = None
    html = None
    soup = None
    file = "test.txt"
    file_obj = None
    text = None
    links = []
    pages = set()

    def __init__(self, url):
        self.url = url
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
            self.pages.add(items['href'])
        
        self.pages.remove('#')

    def _kill_extra_whitespace(self):
        self.text = re.sub(r'\n\s*\n', r'\n\n', self.soup.get_text().strip(), flags=re.M)

    def _page_crawler(self):
        for page in self.pages:
            temphtml = urlopen(page).read()
            tempsoup = bs(temphtml, 'lxml')
            temptitle = tempsoup.find_all('title')
            print temptitle

    def _output_result(self):
        print "Possible pages:\n"
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


    # Need to use the pages list to crawl each page