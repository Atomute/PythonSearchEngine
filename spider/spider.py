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
    
    def push_domain(self,domain):
        if "{}".format(domain) in self.db.get_column("domain","domainName"):
            self.db.update_domain(domain)
        else: 
            # location = self.get_location(domain)
            location = "-"
            if type(location) == list: domain = location[1];location = location[0]
            value = (domain,location,1)
            self.db.insert_domain(value)
        self.db.commit()
        return domain

    def push_websites(self,value):
        # push data into websites table
        if "{}".format(self.currentURL) in self.db.get_column("websites","URL"):
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
        progresscounter = 0
        for row in backlinks:
            websiteID = row[0]
            url = row[1]
            progresscounter += 1
            print(f"{progresscounter}/{len(backlinks)}",end="\r")

            domain = self.extractDomain(url)
            realdomain = self.push_domain(domain)
            domainID = self.db.get_ID("domain","domainName",realdomain)
            self.push_DomainLink(websiteID,domainID)

    def push_DomainLink(self,websiteID,domainID):
        self.db.insert_domainlink(websiteID,domainID)

    def extractDomain(self,url):
        # extract domain from url
        domain = urlparse(url).hostname
        if domain != None and domain.startswith("www."):
            return domain[4:]
        else:
            return domain
        
    def onelink(self,html):
        content = self.get_contents(html)
        title = self.get_title(html)
        value = (self.currentURL,title,content,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if self.depth == None or self.depth[0]>self.currentDepth:
            self.get_links(html)

        self.push_websites(value)

    def run(self,root,*depth):
        # scrape one root at choosen depth

        # initial setup
        self.depth = depth
        if not depth: self.depth=None

        self.urltovisit.append(root)

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

            html = requests.get(self.currentURL).text
            self.onelink(html)
            self.push_backlinks(self.exlinks)

            self.visitedURL.append(self.currentURL)

            stopTimer = timeit.default_timer()
            print("crawled "+self.currentURL+" in ",stopTimer-startTimer)