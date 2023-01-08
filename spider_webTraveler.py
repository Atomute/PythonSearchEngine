import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import timeit

class webTraveler():
    def __init__(self,url):
        self.rooturl = url

        self.allurl = []
        self.urltovisit = [url]
        self.visitedurl = []
        self.dupeLinkCount = []
    
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
            
            self.urltovisit.append(fullpath)

    def find_link_duplicate(self,url):
        index = self.visitedurl.index(url)

        while index+1 > len(self.dupeLinkCount):
            self.dupeLinkCount.append(1)

        self.dupeLinkCount[index] += 1

        return self.dupeLinkCount


    def crawl(self,url):
        # crawl to each webpages and download its HTML doc
        self.visitedurl.append(url)
        self.find_links(url)

        return self.download_url(url)

    def run(self):
        # main function to execute the program
        # it will lead the bot to crawl through the appropiate url

        while self.urltovisit:
            self.start = timeit.default_timer()
            
            url = self.urltovisit.pop(0)

            if not url.startswith(self.rooturl):
                continue
            self.allurl.append(url)
            if url in self.visitedurl:
                self.find_link_duplicate(url)
                continue
            
            yield self.crawl(url),url
