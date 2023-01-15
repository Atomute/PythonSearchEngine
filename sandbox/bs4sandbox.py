from bs4 import BeautifulSoup
import requests

html = requests.get("https://learnpython.com/blog/").text

soup = BeautifulSoup(html,'html.parser')

ps = soup.find_all('a')
p = [p.text for p in ps]

print(p)