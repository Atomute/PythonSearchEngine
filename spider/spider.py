# this will push data to websites backlinks and Domain of the root 

from urllib.parse import urljoin,urlparse
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
from datetime import datetime
import timeit
from robotexclusionrulesparser import RobotExclusionRulesParser
import socket
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.distance import distance
from collections import Counter
from time import sleep

from database.DB_sqlite3 import *
from indexer.index_inverter import InvertedIndex
from indexer.index_Country import Getcountry

class spider:
    def __init__(self):
        self.is_pause = False

        self.root = ""
        self.urltovisit = []
        self.visitedURL = []
        self.exlinks = []
        self.currentDepth = 0

        self.indexer = InvertedIndex()
        self.country = Getcountry()
        self.db = DB("testt.sqlite3")
        self.robot = RobotExclusionRulesParser()

    def tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def get_contents(self,body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)  
        answer = u" ".join(t.strip() for t in visible_texts).strip()

        if answer.isspace() or answer == '': return
        
        return answer

    def get_title(self,html):
        # get content from title tag
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('title')

        if title == None: return
        
        if title.text.isspace() or title.text == '': return

        return title.text.strip()

    def get_links(self,html):
        # find links in each webpages and add to urltovisit list
        self.currentDepth -= 1
        print(self.currentDepth)

        soup = BeautifulSoup(html,'html.parser')
        links = soup.find_all('a')

        for link in links:
            path = link.get('href')
            fullpath = urljoin(self.currentURL,path)

            if not fullpath.startswith("https") or not fullpath.startswith("http"):
                continue

            if self.extractDomain(fullpath) != self.rootDomain:
                # external link in this page
                self.exlinks.append(fullpath)
                continue
            if  path == None or "#" in path or "?" in path:
                continue
            
            self.urltovisit.append(fullpath)
        return self.urltovisit
    
    def get_location(self,domain):
        try:
            ip = socket.gethostbyname(domain)
            res = DbIpCity.get(ip, api_key="free")
            return "{}, {}, {}".format(res.city,res.region,res.country)
        except socket.gaierror:
            try:
                domain = "www."+domain
                ip = socket.gethostbyname(domain)
                res = DbIpCity.get(ip, api_key="free")
                return ["{}, {}, {}".format(res.city,res.region,res.country),domain]
            except socket.gaierror:
                return "-"
    
    def push_domain(self,domain,*count):
        if not count: count=[1]
        if "{}".format(domain) in self.db.get_column("domain","domainName"):
            self.db.update_domain(domain,count[0])
        else: 
            self.db.insert_domain(domain)
        self.db.commit()
        return domain

    def push_websites(self,value,url):
        # push data into websites table
        if "{}".format(url) in self.db.get_column("websites","URL"):
            self.db.update_websites(value)
        else:
            self.db.insert_websites(value)
        self.db.commit()

    def push_backlinks(self,urls):
        # push all exlink in a page to databse and clear it
        websiteID = self.db.get_ID("websites","URL",self.currentURL)
        if websiteID in self.db.get_column("backlinks","websiteID"): 
            self.exlinks = []
            return
        for url in urls:
            self.db.insert_exlink(websiteID,url)
        self.db.commit()

        self.exlinks = []

    def push_exlinkDomain(self):
        # push external link domain to database
        print("pushing external link to domain table")
        backlinks = self.db.get_table("backlinks")
        lastWebID = self.db.get_column("Websites_Domain","websiteID")
        if lastWebID == []: lastWebID=[0]
        lastWebID = lastWebID[-1]

        progresscounter = 0
        for row in backlinks:
            websiteID = row[0]
            url = row[1]
            progresscounter += 1
            print(f"{progresscounter}/{len(backlinks)}",end="\r")
            if websiteID<lastWebID: continue

            domain = self.extractDomain(url)
            self.push_domain(domain)
            domainID = self.db.get_ID("domain","domainName",domain)
            self.db.insert_Websites_Domain(websiteID,domainID)

    def extractDomain(self,url):
        # extract domain from url
        domain = urlparse(url).hostname
        if domain != None and domain.startswith("www."):
            return domain[4:]
        else:
            return domain
        
    def updateone(self,url):
        # simply delete one entry and scrape it again or if the url is not in table, will scrape it 
        if url in self.db.get_column("websites","URL"):
            self.removeone(url)
            
        for url in self.run(url,0):
            pass
        self.indexer.indexOneWebsite(url)
        self.country.find_c_websites()
        self.push_exlinkDomain()
        self.counter()

    def updateall(self):
        # simply delete all entry and scrape it all again
        urls = self.db.get_column("websites","URL")

        for url in urls:
            self.updateone(url)

    def onelink(self,url):
        if not url.startswith("http"): return
        self.currentURL = url
        html = requests.get(url).text
        content = self.get_contents(html)
        title = self.get_title(html)
        value = (url,title,content,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if self.depth == None or self.currentDepth != 0:
            self.get_links(html)

        self.push_websites(value,self.currentURL)
        return html
    
    def removeone(self,url):
        websiteID = self.db.get_ID("websites","URL",url)
        if websiteID == None:
            print("This URL not in database yet")
            return None
        
        self.db.dump_record("websites","websiteID",websiteID)

        domain = self.extractDomain(url)
        if domain in self.db.get_column("domain","domainName"): 
            count = self.db.get_column_specific("domain","count",domain,"domainName")[0]
            if count-1 == 0: 
                domainID = self.db.get_ID("domain","domainName",domain)
                self.db.dump_record("domain","domainID",domainID)
            else: 
                self.push_domain(domain,count-1)

        self.domain_counter()
        self.index_counter()
        self.country_counter()

        self.db.commit()

    def removeall(self):
        self.db.dump_table()

    def domain_counter(self):
        domains = self.db.get_column("Websites_Domain","domainID")
        counter = dict(Counter(domains))
        oriDomain = self.db.get_column("domain","domainID")

        for domainID in oriDomain:
            if domainID in counter:
                self.db.cursor.execute("UPDATE domain SET count = {} WHERE domainID = {}".format(counter[domainID],domainID))
            else:
                self.db.dump_record("domain","domainID",domainID)
        self.db.commit()

    def index_counter(self):
        indexes = self.db.get_column("website_inverted_index","index_id")
        counter = dict(Counter(indexes))
        oriIndex = self.db.get_column("keyword","index_id")

        for IndexID in oriIndex:
            if IndexID not in counter:
                self.db.dump_record("keyword","index_id",IndexID)
        self.db.commit()

    def country_counter(self):
        countries = self.db.get_column("Website_country","wc_id")
        counter = dict(Counter(countries))
        oriCountry = self.db.get_column("Country","country_id")

        for CountryID in oriCountry:
            if CountryID not in counter:
                self.db.dump_record("Country","country_id",CountryID)
        self.db.commit()

    def counter(self):
        self.domain_counter()
        self.index_counter()
        self.country_counter()

# UI related function --------------------------------------------------------------------------------------------------------------------------------------------
    def start_stop(self):
        self.is_pause = not self.is_pause

    def kill(self):
        self.is_kill = True
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def run(self,root,*depth):
        parsed_uri = urlparse(root)
        self.root = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        # scrape one root at choosen depth
        self.is_kill = False
        self.is_pause = False
        # initial setup
        self.depth = depth
        print(depth)
        if not depth or depth == (None,): self.depth=None
        else: self.currentDepth = self.depth[0]

        self.urltovisit.append(root)
        self.exlinks.append(root)

        self.rootDomain = self.extractDomain(root)
        if not self.rootDomain in self.db.get_column("domain","domainName"): 
            self.push_domain(self.rootDomain)

        print(root)
        self.robot.fetch(self.root+"robots.txt")
        
        # loop to visit the choosen link and scraped them
        while self.urltovisit:
            self.currentURL = self.urltovisit.pop()

            allow = self.robot.is_allowed("*",self.currentURL)
            if not allow: 
                print("can't crawl")
                continue
            if self.currentURL in self.visitedURL: continue

            startTimer = timeit.default_timer() # timer

            self.onelink(self.currentURL)
            self.push_backlinks(self.exlinks)

            self.visitedURL.append(self.currentURL)

            stopTimer = timeit.default_timer()
            print("crawled "+self.currentURL+" in ",stopTimer-startTimer)

            if self.is_kill:
                self.urltovisit = []
                break

            while self.is_pause:
                sleep(0)

            yield self.currentURL

