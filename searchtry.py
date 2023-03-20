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

    def scoreWord(self,terms):
        ans = {}
        self.db.cursor.execute("""SELECT websiteID, COUNT(websiteID)*SUM(tfidf) AS score 
                                FROM website_inverted_index 
                                WHERE index_id IN ({}) 
                                GROUP BY websiteID 
                                ORDER BY score DESC""".format(",".join(str(i) for i in terms)))
        results = self.db.cursor.fetchall()

        maxScore = results[0][1]
        minScore = results[-1][1]
        scoreRange = maxScore-minScore
        if scoreRange == 0: scoreRange = 1
        for result in results:
            websiteID = result[0]
            score = result[1]
            ans[websiteID] = (score-minScore)*7/scoreRange

        return ans
    
    def scoreDoc(self,scoreDict):
        # domainScore = {}
        self.db.cursor.execute("SELECT MAX(count), MIN(count) FROM domain")
        result = self.db.cursor.fetchall()[0]
        max = result[0]
        min = result[1]
        scoreRange = max-min
        if scoreRange == 0: scoreRange=1

        for webID in scoreDict:
            self.db.cursor.execute("SELECT URL FROM websites WHERE websiteID={}".format(webID))
            url = self.db.cursor.fetchone()[0]

            domain = self.spider.extractDomain(url)
            self.db.cursor.execute("SELECT count FROM domain WHERE domainName='{}'".format(domain))
            count = self.db.cursor.fetchone()[0]
            # domainScore[webID] = (count-min)*3/scoreRange
            scoreDict[webID] += (count-min)*3/scoreRange
        return scoreDict

    def domainNorm(self):
        self.db.cursor.execute("SELECT MAX(count), MIN(count) FROM domain")
        max = self.db.cursor.fetchone()[0][0]
        min = self.db.cursor.fetchone()[0][1]
        scoreRange = max-min
        if scoreRange == 0: scoreRange=1

        return min,scoreRange
        
    def search(self,query):
        startTimer = timeit.default_timer() # timer

        validTermID = []
        terms = self.cleanQuery(query)

        existWord = self.db.get_column("keyword","word")
        for term in terms:
            if term in existWord:
                termID = self.db.get_ID("keyword","word",term)
                validTermID.append(termID)

        wordScore = self.scoreWord(validTermID)

        docScore = self.scoreDoc(wordScore)

        stopTimer = timeit.default_timer()

        return docScore,stopTimer-startTimer
    





        

