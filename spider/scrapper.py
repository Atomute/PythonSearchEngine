# execute all scraping here

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import spider.crawler as crawler
import database.sqlite3_db as sqlite3_db

class scrapper():

    def __init__(self,url):
        self.url = url
        self.visited_url = []

    def get_html(self,url):
        spider = crawler(url)
        return 

    def get_title(self,html):
        pass

    def get_p(self,html):
        pass

    def pushtoDB(self):
        pass

    def run(self):
        pass

        