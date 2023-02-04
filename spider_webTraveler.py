import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import timeit
from robotexclusionrulesparser import RobotExclusionRulesParser

class webTraveler():
    def __init__(self):
        self.rooturl = ""

        self.allurl = []
        self.urltovisit = []
        self.visitedurl = {}
        self.externalLink = []

        self.depth = None
        self.depthcounter = 0

        # tell the crawler to obey the robot.txt
        self.robot = RobotExclusionRulesParser()

    def download_url(self,url):
        return requests.get(url).text

    def find_links(self,url):
        # find links in each webpages and add to urltovisit list
        self.depthcounter += 1
        html = self.download_url(url)
        soup = BeautifulSoup(html,'html.parser')
        links = soup.find_all('a')

        for link in links:
            path = link.get('href')
            fullpath = urljoin(url,path)

            if not fullpath.startswith(self.rooturl):
                # external link in this page
                self.externalLink.append(fullpath)
                continue
            if  path == None or "#" in path:
                continue
            
            self.urltovisit.append(fullpath)
        return self.urltovisit

    def find_link_duplicate(self,url):
        self.visitedurl[url] += 1

    def exLink(self,url):
        # find all external link in this webpage
        
        pass

    def crawl(self,url):
        # crawl to each webpages and download its HTML doc
        print("I'm in "+url)
        self.visitedurl[url] = 1
        html = self.download_url(url)
        if self.depth == None or self.depth > self.depthcounter:
            self.find_links(url)   

        return html

    def run(self,rooturl,*depth):
        # main function to execute the program
        # it will lead the bot to crawl through the appropiate url
        if depth:
            self.depth = depth[0]
        self.rooturl = rooturl
        self.urltovisit.append(rooturl)
        self.robot.fetch(self.rooturl+"robots.txt")
        
        while self.urltovisit:
            self.start = timeit.default_timer()
            
            url = self.urltovisit.pop(0)
            allow = self.robot.is_allowed("*",url)
            # print(allow)
            # print(self.visitedurl)
            # print(self.urltovisit)

            if not allow:
                print("can't crawl "+url)
                continue
            self.allurl.append(url)

            if url in self.visitedurl:
                self.find_link_duplicate(url)
                continue

            yield self.crawl(url),url
            