# execute all scraping here

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime
import timeit

from spider_webTraveler import *
from DB_sqlite3 import *

class scraper():
    websiteID_counter = 0

    def __init__(self,url):
        self.ans = " "
        self.rooturl = url

        self.crawler = webTraveler(url)

        self.db = DB()

    def get_title(self,html):
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('title')
        return title.string

    def get_p(self,html):
        soup = BeautifulSoup(html,'html.parser')
        ps = soup.find_all('p')

        if ps == None:
            return 
        p = [p.text for p in ps]

        return p

    def pushtoDB(self,table,value):
        # push data in to database

        match table:
            case "websites":
                self.db.insert_websites(value,)
            case "keywords":
                self.db.insert_keywords(value)
        
        scraper.websiteID_counter += 1

    def run(self):
        # main function to execute the program
        try:
            for html,url in self.crawler.run():
                title = self.get_title(html)
                p = self.get_p(html)

                value = (scraper.websiteID_counter,url,title,'|'.join(p),datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # print(value)
                self.pushtoDB("websites",value)

                stop = timeit.default_timer()
                print("crawled "+url+" in ",stop-self.crawler.start)

            self.db.close_conn()
        except KeyboardInterrupt:
            self.db.close_conn()
        

atomute = scraper("https://atomute.github.io/")
atomute.run()

booktoScrape = scraper("https://books.toscrape.com/")
booktoScrape.run()
        