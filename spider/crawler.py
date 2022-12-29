import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class crawler():
    def __init__(self,url):
        self.rooturl = url
        self.urltovisit = [url]
        self.visitedurl = []
    
    def download_url(self,url):
        return requests.get(url).text

    def find_links(self,url):
        # find links in each webpages and add to urltovisit list
        html = self.download_url(url)
        soup = BeautifulSoup(html,'html.parser')
        links = soup.find_all('a')

        for link in links:
            path = link.get('href')
            fullpath = urljoin(url,path)
            
            self.urltovisit.append(fullpath)

    def crawl(self,url):
        # crawl to each webpages and download its HTML doc
        print("I'm in "+url)
        self.visitedurl.append(url)
        self.find_links(url)

        return self.download_url(url)

    def run(self):
        # main function to execute the program
        # it will lead the bot to crawl through the appropiate url

        while self.urltovisit:
            url = self.urltovisit.pop(0)
            if url in self.visitedurl or not url.startswith(self.rooturl):
                continue
            yield self.crawl(url)

