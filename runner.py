from spider.spider_scrapper import *
from spider.spider_webTraveler import *
from indexer.index_inverter import *

class Runner:
    def __init__(self):
        pass

    def startCrawl(self,root):
        try:
            for root in roots: 
                atomute = scraper()
                atomute.run(root,1)
        except KeyboardInterrupt:
            # for domain in atomute.crawler.externalLink:
            #     atomute.push_domain(atomute.extractDomain(domain))
            atomute.db.close_conn()

    def startIndex(self):
        II = InvertedIndex()
        II.index_websites()


if __name__ == "__main__":
    runner = Runner()
    # runner.startIndex()
    roots = ["https://yugioh.fandom.com/wiki/","https://cardfight.fandom.com/wiki/","https://xenoblade.fandom.com/wiki/","https://zelda.fandom.com/wiki/","https://fireemblem.fandom.com/wiki/","https://pokemon.fandom.com/wiki/"]
    runner.startCrawl(roots)
    
    
# "https://yugioh.fandom.com/wiki/" "https://cardfight.fandom.com/wiki/" "https://xenoblade.fandom.com/wiki/" "https://zelda.fandom.com/wiki/" "https://fireemblem.fandom.com/wiki/Fire_Emblem_Wiki" "https://pokemon.fandom.com/wiki/"

""" ["https://yugioh.fandom.com/wiki/","https://quotes.toscrape.com/","https://books.toscrape.com/","https://gundam.fandom.com/wiki/","https://www.35mmc.com/","https://www.sqlite.org/",
"https://en.wikipedia.org/wiki/","https://www.detectiveconanworld.com/wiki/","https://cardfight.fandom.com/wiki/Cardfight!!_Vanguard_Wiki"]"""