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

    def get_all_links(self,depth,*urls):
        print("Depth = "+str(depth))
        if depth == 0:
            return self.urltovisit
        
        newURL = []

        if type(urls[0]) != str: urls = urls[0]

        for url in urls:
            html = requests.get(url).text
            soup = BeautifulSoup(html,'html.parser')
            links = soup.find_all('a')

            for link in links:
                path = link.get('href')
                fullpath = urljoin(self.currentURL,path)
                if fullpath.endswith("/"):
                    fullpath = fullpath[:-1]

                if not fullpath.startswith("https") or not fullpath.startswith("http"):
                    continue

                if fullpath in newURL or fullpath in self.urltovisit or fullpath in self.visitedurl:
                    continue

                if self.extractDomain(fullpath) != self.rootDomain:
                    continue

                if  path == None or "#" in path or "File:" in path:
                    continue
                
                self.urltovisit.append(fullpath)
                newURL.append(fullpath)
        depth -= 1
        return self.get_all_links(depth,newURL)

    def get_links(self,html):
        # find links in each webpages and add to urltovisit list

        soup = BeautifulSoup(html,'html.parser')
        links = soup.find_all('a')

        for link in links:
            path = link.get('href')
            fullpath = urljoin(self.currentURL,path)
            if fullpath.endswith("/"):
                fullpath = fullpath[:-1]

            if not fullpath.startswith("https") or not fullpath.startswith("http"):
                continue

            if fullpath in self.visitedurl or fullpath in self.urltovisit:
                continue

            if self.extractDomain(fullpath) != self.rootDomain:
                # external link in this page
                self.exlinks.append(fullpath)
                continue
            if  path == None or "#" in path:
                continue
            
            if self.depth == None or self.depth>= 0:
                self.urltovisit.append(fullpath)

        return self.urltovisit
    
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
        if urls == []:
            return
        websiteID = self.db.get_ID("websites","URL",self.currentURL)
        if websiteID in self.db.get_column("externalDomain","websiteID"): 
            self.exlinks = []
            return
        for url in urls:
            domain = self.extractDomain(url)
            self.db.insert_exlink(websiteID,domain)
        self.db.commit()

        self.exlinks = []

    def push_exlinkDomain(self):
        # push external link domain to database
        # print("pushing external link to domain table")
        self.db.cursor.execute("DELETE FROM Websites_Domain")
        backlinks = self.db.get_table("backlinks")

        progresscounter = 0
        for row in backlinks:
            websiteID = row[0]
            url = row[1]
            progresscounter += 1
            # print(f"{progresscounter}/{len(backlinks)}",end="\r")

            domain = self.extractDomain(url)
            self.push_domain(domain)
            domainID = self.db.get_ID("domain","domainName",domain)
            self.db.insert_Websites_Domain(websiteID,domainID)

    def push_log(self,remaining,withDepth):
        root = self.db.get_column("log","root")
        is_in = self.root in root
        if root == [] and is_in:
            id = self.db.get_ID("log","root",self.root)
            self.db.dump_record("log","log_id",id)
            return
        
        strremaining = ",".join(remaining)
        if is_in:
            self.db.cursor.execute("UPDATE log SET remaining = ? WHERE root = ?",(strremaining,self.root))
        else:
            self.db.cursor.execute("INSERT INTO log (root,remaining,withDepth) VALUES (?, ?, ?)",(self.root,strremaining,withDepth))

        self.db.commit()

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
            self.rootDomain = self.extractDomain(url)
            self.depth = -1
            self.visitedurl = self.db.get_visited_url("websites","URL",self.root[:-1])
            self.onelink(url)
            self.indexer.indexOneWebsite(url)
            self.country.find_c_websites_one(url)
            self.push_backlinks(self.exlinks)
            
            self.urltovisit = []
            
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

        self.get_links(html)

        self.push_websites(value,self.currentURL)
        self.push_backlinks(self.exlinks)

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
        domains = self.db.get_column("externalDomain","exDomain")
        counter = dict(Counter(domains))
        oriDomain = self.db.get_column("domain","domainName")

        for domain in oriDomain:
            if domain in counter:
                self.db.cursor.execute("UPDATE domain SET count = {} WHERE domainName = '{}'".format(counter[domain],domain))
            # else:
            #     self.db.dump_record("domain","domainID",domainID)
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

    def log_counter(self):
        self.db.cursor.execute("SELECT root, remaining FROM log")
        results = self.db.cursor.fetchall()
        for result in results:
            root = result[0]
            remaining = result[1]
            if remaining == '':
                self.db.dump_record("log","root",root)

    def counter(self):
        self.domain_counter()
        self.index_counter()
        self.country_counter()
        self.log_counter()

# UI related function --------------------------------------------------------------------------------------------------------------------------------------------
    def start_stop(self):
        self.is_pause = not self.is_pause

    def kill(self):
        self.is_kill = True
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def run(self,root,*depth):
        parsed_uri = urlparse(root)
        self.root = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        # UI control
        self.is_kill = False
        self.is_pause = False

        if root.endswith("/"):
            root = root[:-1]
        self.urltovisit.append(root)
        
        # initial setup
        self.rootDomain = self.extractDomain(root)
        if not self.rootDomain in self.db.get_column("domain","domainName"): 
            self.push_domain(self.rootDomain)

        self.withDepth = None
        if not depth or depth == (None,): 
            self.depth=None
            self.withDepth = "False"
        elif depth: 
            print("find all the link")
            self.currentURL = root
            self.visitedurl = self.db.get_visited_url("websites","URL",self.root[:-1])
            self.visitedurl.append(root)
            self.get_all_links(depth[0],root)
            self.depth = -1
            self.withDepth ="True"
        
        if self.depth != 0:
            self.push_log(self.urltovisit,self.withDepth)

        self.robot.fetch(self.root+"robots.txt")
        
        # loop to visit the choosen link and scraped them
        while self.urltovisit:
            try:
                startTimer = timeit.default_timer() # timer

                self.visitedurl = self.db.get_visited_url("websites","URL",self.root[:-1])
                self.visitedurl.append(root)

                self.currentURL = self.urltovisit.pop(0)
                if not urlparse(self.currentURL).scheme or not urlparse(self.currentURL).netloc:
                    continue

                # check robots.txt
                allow = self.robot.is_allowed("*",self.currentURL)
                if not allow: 
                    print("can't crawl")
                    continue

                self.onelink(self.currentURL)
                
                stopTimer = timeit.default_timer()
                print("crawled "+self.currentURL+" in ",stopTimer-startTimer)

                if self.is_kill:
                    self.counter()
                    return self.currentURL

                while self.is_pause:
                    sleep(0)

                yield self.currentURL
            except Exception as e:
                print(e)
                pass
        self.counter()
        # self.push_exlinkDomain()