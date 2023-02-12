import requests
from bs4 import BeautifulSoup

from database.DB_sqlite3 import DB
from spider.spider import spider


class updater:
    def __init__(self):
        self.db = DB("testt.sqlite3")
        self.spider = spider()

    def get_webToupdate(self):
        print(self.db.get_column("websites","URL"))

    def update_backlinks(self,urls):
        oldlinks = self.db.something()
        if oldlinks == urls:
            pass
        else:
            self.db.dumb()

    def update_domain(self):
        pass

    def updateone(self,url):
        html = requests.get(url).text
        self.spider.onelink(html)
        self.update_backlinks(self.spider.exlinks)

    def updateall(self):
        pass

    def removeone(self,url):
        websiteID = self.db.get_specElement("websites","URL",url)
        self.db.dump_record("websites","websiteID",websiteID)
        # self.db.dump_record("backlinks","websiteID",websiteID)

        self.db.close_conn()

