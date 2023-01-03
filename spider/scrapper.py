# execute all scraping here

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from crawler import *
from sqlite3_db import *

class scraper():

    def __init__(self,url,websiteName):
        self.ans = ""
        self.rooturl = url

        self.crawler = crawler(url)
        self.id_counter = 0

        self.tableName = websiteName
        self.db = DB('test.db')
        self.db.create_table(websiteName)

    def get_title(self,html):
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('title')
        return title.string

    def get_p(self,html):
        arrp = []
        soup = BeautifulSoup(html,'html.parser')
        ps = soup.find('p')
        if ps == None:
            return
        for p in ps:
            arrp.append(p.string)
        return arrp

    def pushtoDB(self,url,title,p):
        self.db.update(self.tableName,(self.id_counter,url,title,p))
        self.id_counter+=1

    def run(self):
        # main function to execute the program
        for html in self.crawler.run():
            title = self.get_title(html)
            p = self.get_p(html)
            self.pushtoDB(self.crawler.urltovisit[0],str(title),str(p))
        self.db.close_conn()

atomute = scraper("https://atomute.github.io/","atomute")
atomute.run()

booktoScrape = scraper("https://books.toscrape.com/","booktoScrape")
booktoScrape.run()
        