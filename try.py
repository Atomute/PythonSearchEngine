from spider.spider import spider

a = spider()
a.currentURL = "https://www.fandom.com/"
a.rootDomain = a.extractDomain("https://www.fandom.com/")
a.get_all_links(2,'https://www.fandom.com/')

print(a)
