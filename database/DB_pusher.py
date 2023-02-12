# This will push domain of the backlink to database and anythings that can't be push in spider
from spider.spider import spider
from DB_sqlite3 import DB
class pusher:
    def __init__(self):
        self.db = DB()
      
    def push_domain(self,domain):
        if "{}".format(domain) in self.db.get_column("domain","domainName"):
            self.db.update_domain(domain)
        else: 
            location = self.get_location(domain)
            value = (domain,location,1)
            self.db.insert_domain(value)
        self.db.commit()

    def push_exlinkDomain(self):
            # push external link domain to database
            urls = self.db.get_column("backlinks","backlink")
            for url in urls:
                cleanurl = self.cleanURL(url)
                domain = self.extractDomain(cleanurl)
                self.push_domain(domain)
    
    def push(self):
        self.push_exlinkDomain()