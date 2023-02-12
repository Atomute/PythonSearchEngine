import timeit

# from indexer.index_inverter import *
from spider.spider import spider
from spider.spider_updater import updater

class Runner:
    def __init__(self):
        pass

    def startCrawl(self,root):
        start = timeit.default_timer()
        try:
            for root in roots: 
                atomute = spider()
                atomute.run(root,1)
                atomute.push_exlinkDomain()
                atomute.db.close_conn()
        except KeyboardInterrupt:
            atomute.db.close_conn()

        stop = timeit.default_timer()
        print("finished crawled "+root+"in "+str(stop-start))

if __name__ == "__main__":
    # runner = Runner()
    # roots = ["https://atomute.github.io/","https://yugioh.fandom.com/","https://cardfight.fandom.com/","https://xenoblade.fandom.com/","https://zelda.fandom.com/","https://fireemblem.fandom.com/","https://pokemon.fandom.com/"]
    # runner.startCrawl(roots)

    test = updater()
    test.removeone("https://atomute.github.io/")
    
    
# "https://yugioh.fandom.com/wiki/" "https://cardfight.fandom.com/wiki/" "https://xenoblade.fandom.com/wiki/" "https://zelda.fandom.com/wiki/" "https://fireemblem.fandom.com/wiki/Fire_Emblem_Wiki" "https://pokemon.fandom.com/wiki/"

""" ["https://yugioh.fandom.com/wiki/","https://quotes.toscrape.com/","https://books.toscrape.com/","https://gundam.fandom.com/wiki/","https://www.35mmc.com/","https://www.sqlite.org/",
"https://en.wikipedia.org/wiki/","https://www.detectiveconanworld.com/wiki/","https://cardfight.fandom.com/wiki/Cardfight!!_Vanguard_Wiki"]"""