from urllib.parse import urljoin,urlparse
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import timeit
from robotexclusionrulesparser import RobotExclusionRulesParser

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

        titleText = title.text
        
        if title.text.isspace() or titleText == '': return

        return titleText.strip()

    def get_links(self,html):
        # find links in each webpages and add to urltovisit list
        self.currentDepth += 1

        soup = BeautifulSoup(html,'html.parser')
        links = soup.find_all('a')

        for link in links:
            path = link.get('href')
            fullpath = urljoin(self.currentURL,path)

            if not self.root[:len(self.root)-1] in fullpath:
                # external link in this page
                self.exlinks.append(fullpath)
                continue
            if  path == None or "#" in path:
                continue
            
            self.urltovisit.append(fullpath)
        return self.urltovisit
    
    def push_domain(self,domain):
        if "{}".format(domain) in self.db.get_column("domain","domainName"):
            value = (domain,domain)
            self.db.update_domain(value)
        else: 
            value = (domain,1)
            self.db.insert_domain(value)
        self.db.commit()

    def push_websites(self,value):
        # push data into websites table
        if "{}".format(self.currentURL) in self.db.get_column("websites","URL"):
            self.db.update_websites(value)
        else:
            self.db.insert_websites(value)
        self.db.commit()

    def push_backlinks(self,urls):
        # push all exlink in a page to databse and clear it
        websiteID = self.db.get_specElement("websites","URL",self.currentURL)
        if websiteID in self.db.get_column("backlinks","websiteID"): 
            self.exlinks = []
            return
        for url in urls:
            self.db.insert_exlink(websiteID,url)
        self.db.commit()

        self.exlinks = []

    def push_exlinkDomain(self,urls):
        # push external link domain to database
        for url in urls:
            cleanurl = self.cleanURL(url)
            domain = self.extractDomain(cleanurl)
            self.push_domain(domain)

    def cleanURL(self,url):
        if url.startswith("https"):
            domain = self.extractDomain(url)
            if domain.startswith("www."):
                return "https://"+domain[4:]
            else:
                return "https://"+domain
        else:
            domain = self.extractDomain(url)
            if domain.startswith("www."):
                return "http://"+domain[4:]
            else:
                return "http://"+domain

    def extractDomain(self,url):
        # extract domain from url
        domain = urlparse(url).hostname
        return domain
        
    def onelink(self,html):
        content = self.get_contents(html)
        title = self.get_title(html)
        value = (self.currentURL,title,content,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if self.depth == None or self.depth[0]>self.currentDepth:
            self.get_links(html)

        self.push_websites(value)
        # self.push_exlinkDomain(self.exlinks)
        self.push_backlinks(self.exlinks)

    def run(self,root,*depth):
        # scrape one root at choosen depth

        # initial setup
        self.depth = depth
        if not depth: self.depth=None

        self.root = self.cleanURL(root)
        self.urltovisit.append(root)
        if not self.root in self.db.get_column("domain","domainName"): 
            rootDomain = self.extractDomain(self.root)
            self.push_domain(rootDomain)
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

            self.visitedURL.append(self.currentURL)

            stopTimer = timeit.default_timer()
            print("crawled "+self.currentURL+" in ",stopTimer-startTimer)