import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_links(links):
    ans = []
    for link in links:
        path = link.get('href')
        fullPath = urljoin(url,path)
        if fullPath in ans:
            continue
        
        ans.append(fullPath)
    return ans

def find_p(ps):
    ans = []
    for p in ps:
        strp = p.string
        if strp == None:
            continue
        ans.append(strp)

    return ans

def find_title(titles):
    ans = []
    for title in titles:
        strtitle = title.string
        if strtitle == None:
            continue
        ans.append(strtitle)

    return ans

ans = []
visited_url = []
url = 'https://en.wikipedia.org/wiki/Battle_of_Van_Buren'
html = requests.get(url).text

soup = BeautifulSoup(html,'html.parser')
links = soup.find_all('a')
title = soup.find_all('title')
p = soup.find_all('p')

print(find_links(links))