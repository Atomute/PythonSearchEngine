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
        html = self.download_url(url)
        soup = BeautifulSoup(html,'html.parser')
        links = soup.find_all('a')

        for link in links:
            path = link.get('href')
            fullpath = urljoin(url,path)
            
            self.urltovisit.append(fullpath)

    def crawl(self,url):
        print("I'm in "+url)
        self.find_links(url)

    def run(self):
        while self.urltovisit:
            url = self.urltovisit.pop(0)
            if url in self.visitedurl or not url.startswith(self.rooturl):
                continue
            self.crawl(url)
            self.visitedurl.append(url)
        return self.visitedurl

atomute = crawler("https://atomute.github.io/")

themoviedb = crawler("https://www.themoviedb.org/movie")

wikipedia = crawler("https://en.wikipedia.org/wiki/")
# wikipedia.run()

tft = crawler("https://tftactics.gg/")
tft.run()
