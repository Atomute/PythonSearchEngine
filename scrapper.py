# execute all scraping here

import csv
import requests
import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from crawler import *

class scrapper():

    def __init__(self,url):
        self.url = url
        self.visited_url = []

    def download_url(self):
        return requests.get(self.url).text

    def get_url(self):
        html = self.download_url()
        soup = BeautifulSoup(html,'html.parser')
        links = soup.find_all('a')

        return links

    def visit_url(self):
        pass

    def get_p(self,html):
        # get all content from html p tag
        ans = []
        soup = BeautifulSoup(html,'html.parser')
        ps = soup.find_all('p')
        for p in ps:
            strp = p.string
            if strp == None:
                continue
            ans.append(strp)

        return ans

    def get_title(self,html):
        # get content from html title tag
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('title')

        return title.string

    def write_csv(self,link,title,p):
        pass

    def run(self):
        # main function to start running the program
        # run through all the link  
        for link in crawler(self.url).find_links:
            if link in self.visited_url:
                continue
            html = self.download_url(link)
            self.visited_url.append(link)
            self.write_csv()

            





