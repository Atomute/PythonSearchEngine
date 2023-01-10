import requests
from bs4 import BeautifulSoup

html = requests.get("https://www.sciencedirect.com/topics/agricultural-and-biological-sciences").text

soup = BeautifulSoup(html,'html.parser')

link = soup.find('a')
print(link.text)