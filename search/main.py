from spider.spider import spider
from indexer.index_cleaner import Cleaning
from database.DB_sqlite3 import DB

class searcher:
    # ranking by two factor (keyword freq and domain count)
    def __init__(self):
        self.cleaner = Cleaning()
        self.spider = spider()
        self.db = DB("testt.sqlite3")

    def cleanQuery(self,text):
        # Tested in indexing part
        cleanedQuery = self.cleaner.process_text(text)
        return cleanedQuery

    def scoreKeyword(self,hitweb,lenquery,allwordfreq):
        # score for one keyword
        # websiteID : score
        
        rank = 0
        sorthitweb = {k: v for k, v in sorted(hitweb.items(), key=lambda item: item[1])}
        for web in sorthitweb:
            sorthitweb[web] += 7*rank/((len(hitweb)-1)*lenquery)
            counter += 1

        return sorthitweb

    def scoreDomain(self,kerywordscore):
        urls = []
        for web in kerywordscore:
            self.db.cursor.execute("SELECT URL FROM websites WHERE websiteID={}".format(web))
            url = self.db.cursor.fetchone()[0]
            domain = self.spider.extractDomain(url)
            if domain not in self.db.get_column("domain","domainName"): continue
            urls.append(domain)

        self.db.cursor.execute("SELECT SUM(count) FROM domain")
        alldomaincount = self.db.cursor.fetchone()[0]

        for web in kerywordscore:
            self.db.cursor.execute("SELECT URL FROM websites WHERE websiteID={}".format(web))
            url = self.db.cursor.fetchone()[0]
            domain = self.spider.extractDomain(url)
            if domain not in self.db.get_column("domain","domainName"): continue
            domaincount = self.db.get_column_specific("domain","count",domain,"domainName")[0]
            kerywordscore[web] += 3*domaincount/(alldomaincount*len(kerywordscore))

        return kerywordscore

    def get_all_keyword(self):
        pass

    def search(self,query):
        # will return list of websiteID integer
        ans = []
        cleanQuery = self.cleanQuery(query)
        keywords = self.db.get_column("keyword","word")

        index_ids = []

        for query in cleanQuery:
            if query not in keywords: continue
            wordID = self.db.get_ID("keyword","word",query)
            index_ids.append(wordID)

        self.db.cursor.execute("SELECT websiteID, SUM(frequency) FROM website_inverted_index WHERE index_id IN ({}) GROUP BY websiteID ORDER BY SUM(frequency) DESC".format(",".join(str(i) for i in index_ids)))
        results = self.db.cursor.fetchall()

        self.scoreKeyword()

        print(results)
        
        return ans
    

