import timeit

from indexer.index_inverter import *
from spider.spider import spider

class Runner:
    def __init__(self):
        pass

    def startCrawl(self,root):
        start = timeit.default_timer()
        try:
            for root in roots: 
                atomute = spider()
                atomute.run(root,1)
                atomute.db.close_conn
        except KeyboardInterrupt:
            atomute.db.close_conn()

        stop = timeit.default_timer()
        print("finished crwaled "+root+"in "+str(stop-start))

    def startIndex(self):
        II = InvertedIndex()
        II.index_websites()


if __name__ == "__main__":
    runner = Runner()
    # runner.startIndex()
    roots = ["https://yugioh.fandom.com/","https://cardfight.fandom.com/","https://xenoblade.fandom.com/","https://zelda.fandom.com/","https://fireemblem.fandom.com/","https://pokemon.fandom.com/"]
    runner.startCrawl(roots)
    
    
# "https://yugioh.fandom.com/wiki/" "https://cardfight.fandom.com/wiki/" "https://xenoblade.fandom.com/wiki/" "https://zelda.fandom.com/wiki/" "https://fireemblem.fandom.com/wiki/Fire_Emblem_Wiki" "https://pokemon.fandom.com/wiki/"

""" ["https://yugioh.fandom.com/wiki/","https://quotes.toscrape.com/","https://books.toscrape.com/","https://gundam.fandom.com/wiki/","https://www.35mmc.com/","https://www.sqlite.org/",
"https://en.wikipedia.org/wiki/","https://www.detectiveconanworld.com/wiki/","https://cardfight.fandom.com/wiki/Cardfight!!_Vanguard_Wiki"]"""