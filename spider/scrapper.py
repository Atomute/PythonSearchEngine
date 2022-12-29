# execute all scraping here

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from crawler import *
from sqlite3_db import *

class scraper():

    def __init__(self,url):
        self.rooturl = url

        self.crawler = crawler(url)
        self.id_counter = 0

        self.db = DB('test.db')
        self.db.create_table("atomuteBlog")

    def get_title(self,html):
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('title')
        return title.string

    def get_p(self,html):
        soup = BeautifulSoup(html,'html.parser')
        p = soup.find('p')
        return p.string

    def pushtoDB(self,url,title,ps):
        self.db.update("atomuteBlog",(self.id_counter,url,title,ps))
        self.id_counter+=1

    def run(self):
        # main function to execute the program
        for html in self.crawler.run():
            title = self.get_title(html)
            p = self.get_p(html)
            self.pushtoDB(self.crawler.urltovisit[0],str(title),str(p))
        self.db.close_conn()

atomute = scraper("https://atomute.github.io/")
atomute.run()

        