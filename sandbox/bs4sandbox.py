from bs4 import BeautifulSoup
import requests

html = requests.get("https://atomute.github.io/linux_howto/#5-set-up-your-linux").text

soup = BeautifulSoup(html,'html.parser')

ps = soup.find_all('p')
p = [p.text for p in ps]

print(p)