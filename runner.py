from index_inverter import InvertedIndex
from spider_scrapper import scraper

# inv=InvertedIndex()
# inv.index_websites()

test = scraper()

print(test.get_contents("<body> <Div>Menu</div> <p>       This is paragraph      </p> <span>    this is span        </span> </body>"))