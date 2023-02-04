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
    
    def extractDomain(self,url):
        # extract domain from url
        domain = urlparse(url).hostname
        return domain

    def pushtoDB(self,value,url):
        # push data in to database
        if ("{}".format(url),) in self.db.get_column("URL","websites"):
            self.db.update_websites(value)
        else:
            self.db.insert_websites(value)

    def push_domain(self,domain):
        if ("{}".format(domain),) in self.db.get_column("domainName","domain"):
            value = (domain,domain)
            self.db.update_domain(value)
        else:
            value = (domain,1)
            self.db.insert_domain(value)

    def run(self,rooturl,*depth):
        # main function to execute the program
        # get html and url from crawler to extract contents from website and push to db
        if not depth: depth=[None]

        # push domain to domain db
        # self.push_domain(self.extractDomain(rooturl))

        for html,url in self.crawler.run(rooturl,depth[0]):
            title = self.get_title(html)
            content = self.get_contents(html)

            value = (url,title,content,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # print(value)
            self.pushtoDB(value,url)

            stop = timeit.default_timer()
            print("crawled "+url+" in ",stop-self.crawler.start)
        # for domain in self.crawler.externalLink:
        #     self.push_domain(self.extractDomain(domain))

        self.db.close_conn()
    