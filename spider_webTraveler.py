import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import timeit
from robotexclusionrulesparser import RobotExclusionRulesParser

class webTraveler():
    def __init__(self,url):
        self.rooturl = url

        self.allurl = []
        self.urltovisit = [url]
        self.visitedurl = {}

        # tell the crawler to obey the robot.txt
        self.robot = RobotExclusionRulesParser()
        self.robot.fetch(self.rooturl+"robots.txt")

    def download_url(self,url):
        return requests.get(url).text

    def find_links(self,url):
        # find links in each webpages and add to urltovisit list
        html = self.download_url(url)
        soup = BeautifulSoup(html,'html.parser')
        links = soup.find_all('a')

        for link in links:
            path = link.get('href')
            if path == None or path.startswith("#"):
                continue
            fullpath = urljoin(url,path)
            if not fullpath.startswith(self.rooturl):
                continue
            
            self.urltovisit.append(fullpath)

    def find_link_duplicate(self,url):
        self.visitedurl[url] += 1

    def crawl(self,url):
        # crawl to each webpages and download its HTML doc

        print("I'm in "+url)
        self.visitedurl[url] = 1
        self.find_links(url)   

        return self.download_url(url)

    def run(self):
        # main function to execute the program
        # it will lead the bot to crawl through the appropiate url

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
            