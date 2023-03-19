from database.DB_sqlite3 import DB
from indexer.index_cleaner import Cleaning
from spider.spider import spider
import timeit

class searcher:
    def __init__(self):
        self.db = DB("testt.sqlite3")
        self.cleaner = Cleaning()
        self.spider = spider()

    def cleanQuery(self,query):
        return self.cleaner.process_text(query)

    def scoreWord(self,termIDs):
        # Take term ID and Calculate according to Lucene Scoring Method
        ans = {}
        self.db.cursor.execute("""SELECT websiteID, COUNT(websiteID), SUM(tfidf)FROM website_inverted_index 
                                WHERE index_id IN ({}) 
                                GROUP BY websiteID """.format(",".join(str(i) for i in termIDs)))
        results = self.db.cursor.fetchall()
        for result in results:
            websiteID = result[0]
            coord = result[1]
            sumtfidf = result[2]
            score = coord*sumtfidf
            ans[websiteID] = score
        return ans
    
    def scoreDoc(self,scoreDict):
        for webID in scoreDict:
            self.db.cursor.execute("SELECT URL FROM websites WHERE websiteID={}".format(webID))
            url = self.db.cursor.fetchone()[0]

            domain = self.spider.extractDomain(url)
            self.db.cursor.execute("SELECT count FROM domain WHERE domainName='{}'".format(domain))

            domainCount = self.db.cursor.fetchone()[0]
            scoreDict[webID] += domainCount

        return scoreDict

    def search(self,query):
        startTimer = timeit.default_timer() # timer

        validTermID = []
        terms = self.cleanQuery(query)
        print(terms)

        existWord = self.db.get_column("keyword","word")
        for term in terms:
            if term in existWord:
                termID = self.db.get_ID("keyword","word",term)
                validTermID.append(termID)

        wordScore = self.scoreWord(validTermID)

        docScore = self.scoreDoc(wordScore)

        docScore = sorted(docScore.items(), key=lambda x:x[1],reverse=True)
        stopTimer = timeit.default_timer()
        print(docScore,stopTimer-startTimer)

        return docScore