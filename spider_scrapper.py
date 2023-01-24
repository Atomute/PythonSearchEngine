# execute all scraping here

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime
import timeit

from spider_webTraveler import *
from DB_sqlite3 import *

class scraper():
    def __init__(self):
        self.crawler = webTraveler()
        self.db = DB()

    def get_title(self,html):
        # get content from title tag
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('title')

        if title == None: return

        titleText = title.text
        
        if title.text.isspace() or titleText == '': return

        return titleText.strip()

    def get_contents(self,html):
        # get all contents under the html tag
        soup = BeautifulSoup(html,'html.parser')
        ps = soup.find_all()    # this will get every text under HTML tags
        ans = []

        if ps == []: return 
        for p in ps:
            textp = p.text.strip()
            if textp.isspace(): continue
            listp = textp.splitlines()
            strp = ' '.join(listp)
            ans.append(strp)

        answer = " ".join(ans)
        if answer.isspace() or answer == '': return

        return answer

    def pushtoDB(self,value):
        # push data in to database
        self.db.insert_websites(value)

    def run(self,rooturl):
        # main function to execute the program
        # get html and url from crawler to extract contents from website and push to db
        visited = self.db.get_column("websites","URL")
        try:
            for html,url in self.crawler.run(rooturl):

                title = self.get_title(html)
                p = self.get_contents(html)

                value = (url,title,p,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                # print(value)
                self.pushtoDB(value)

                stop = timeit.default_timer()
                print("crawled "+url+" in ",stop-self.crawler.start)

            self.db.close_conn()
        except KeyboardInterrupt:
            self.db.close_conn()
        
if __name__ == "__main__":
    roots = ["https://gundam.fandom.com/wiki/"]
    for root in roots: 
        atomute = scraper()
        atomute.run(root)

""" ["https://quotes.toscrape.com/","https://books.toscrape.com/","https://gundam.fandom.com/wiki/","https://www.35mmc.com/","https://www.sqlite.org/",
"https://en.wikipedia.org/wiki/","https://www.detectiveconanworld.com/wiki/"]
"""
    