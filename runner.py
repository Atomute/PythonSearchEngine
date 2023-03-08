import timeit

# from indexer.index_inverter import *
from spider.spider import spider
from database.DB_sqlite3 import DB
from indexer.index_inverter import InvertedIndex
from indexer.index_Country import Getcountry
from search.main import searcher

class Runner:
    def __init__(self):
        self.spider = spider()
        self.db = DB("testt.sqlite3")
        self.indexer = InvertedIndex()
        self.country = Getcountry()

    def startCrawl(self,roots):
        start = timeit.default_timer()
        try:
            for root in roots: 
                self.spider.run(root,1)
                self.spider.push_exlinkDomain()
                self.spider.domain_counter()
            self.spider.db.close_conn()
        except KeyboardInterrupt:
            self.spider.db.close_conn()

        stop = timeit.default_timer()
        print("finished crawled "+root+"in "+str(stop-start))

    def updateall(self):
        self.spider.updateall()
        self.spider.db.close_conn()

    def updateone(self,url):
        self.spider.updateone(url)
        self.db.close_conn()
        self.indexer.indexOneWebsite(url)

    def index(self):
        self.indexer.index_websites()
        self.country.find_c_websites()

if __name__ == "__main__":
    test = searcher()
    test.search("something free love")
    # runner = Runner()

    # roots = ["https://en.wikipedia.org/wiki/","https://atomute.github.io/","https://www.detectiveconanworld.com/wiki/","https://atomute.github.io/","https://yugioh.fandom.com/","https://cardfight.fandom.com/","https://xenoblade.fandom.com/","https://zelda.fandom.com/","https://fireemblem.fandom.com/","https://pokemon.fandom.com/"]
    # runner.startCrawl(roots)
    # runner.index()

    # runner.spider.updateone("https://atomute.github.io/")
    
# "https://yugioh.fandom.com/wiki/" "https://cardfight.fandom.com/wiki/" "https://xenoblade.fandom.com/wiki/" "https://zelda.fandom.com/wiki/" "https://fireemblem.fandom.com/wiki/Fire_Emblem_Wiki" "https://pokemon.fandom.com/wiki/"

""" ["https://yugioh.fandom.com/wiki/","https://quotes.toscrape.com/","https://books.toscrape.com/","https://gundam.fandom.com/wiki/","https://www.35mmc.com/","https://www.sqlite.org/",
"https://en.wikipedia.org/wiki/","https://www.detectiveconanworld.com/wiki/","https://cardfight.fandom.com/wiki/Cardfight!!_Vanguard_Wiki"]"""