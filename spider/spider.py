# this will push data to websites backlinks and Domain of the root 

from urllib.parse import urljoin,urlparse
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import timeit
from robotexclusionrulesparser import RobotExclusionRulesParser
import socket
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.distance import distance
from collections import Counter

from database.DB_sqlite3 import *

class spider:
    def __init__(self):
        self.root = ""
        self.urltovisit = []
        self.visitedURL = []
        self.exlinks = []
        self.currentDepth = 0

        self.db = DB("testt.sqlite3")
        self.robot = RobotExclusionRulesParser()

    def get_contents(self,html):
        # get all contents under body tag
        soup = BeautifulSoup(html,'html.parser')
        ps = soup.find_all('body')    # this will get every text under HTML tags
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

    def get_title(self,html):
        # get content from title tag
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('title')

        if title == None: return
        
        if title.text.isspace() or title.text == '': return

        return title.text.strip()

    def get_links(self,html):
        # find links in each webpages and add to urltovisit list
        self.currentDepth += 1

        soup = BeautifulSoup(html,'html.parser')
        links = soup.find_all('a')

        for link in links:
            path = link.get('href')
            fullpath = urljoin(self.currentURL,path)

            if not self.rootDomain in fullpath:
                # external link in this page
                self.exlinks.append(fullpath)
                continue
            if  path == None or "#" in path:
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
            
        self.run(url,1)
        self.push_exlinkDomain()
        self.domain_counter()

    def updateall(self):
        # simply delete all entry and scrape it all again
        urls = self.db.get_column("websites","URL")
        self.db.dump_table()
        for url in urls:
            self.run(url,0)

        self.push_exlinkDomain()

    def onelink(self,url):
        self.currentURL = url
        html = requests.get(url).text
        content = self.get_contents(html)
        title = self.get_title(html)
        value = (url,title,content,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if self.depth == None or self.depth[0]>self.currentDepth:
            self.get_links(html)

        self.push_websites(value,self.currentURL)
        return html
    
    def removeone(self,url):
        websiteID = self.db.get_ID("websites","URL",url)
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

    def run(self,root,*depth):
        # scrape one root at choosen depth

        # initial setup
        self.depth = depth
        if not depth: self.depth=None

        self.urltovisit.append(root)
        self.exlinks.append(root)

        self.rootDomain = self.extractDomain(root)
        if not self.rootDomain in self.db.get_column("domain","domainName"): 
            self.push_domain(self.rootDomain)
        
        self.robot.fetch(root+"robots.txt")
        
        # loop to visit the choosen link and scraped them
        while self.urltovisit:
            self.currentURL = self.urltovisit.pop()

            allow = self.robot.is_allowed("*",self.currentURL)
            if not allow: continue
            if self.currentURL in self.visitedURL: continue

            startTimer = timeit.default_timer() # timer

            self.onelink(self.currentURL)
            self.push_backlinks(self.exlinks)

            self.visitedURL.append(self.currentURL)

            stopTimer = timeit.default_timer()
            print("crawled "+self.currentURL+" in ",stopTimer-startTimer)
        self.currentDepth = 0
