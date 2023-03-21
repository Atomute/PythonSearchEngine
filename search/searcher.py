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
        results = self.db.get_word_for_search(terms)

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
        result = self.db.get_MaxMin_Domain()
        max = result[0]
        min = result[1]
        scoreRange = max-min
        if scoreRange == 0: scoreRange=1

        for webID in scoreDict:
            url = self.db.get_column_specific("websites","URL",webID,"websiteID")[0]

            domain = self.spider.extractDomain(url)
            count = self.db.get_column_specific("domain","count",domain,"domainName")
            if not count: count = [min]
            count = count[0]
            scoreDict[webID] += (count-min)*3/scoreRange
        return scoreDict
        
    def search(self,terms):
        # try:
        startTimer = timeit.default_timer() # timer

        validTermID = []
        existWord = self.db.get_column("keyword","word")
        for term in terms:
            if term in existWord:
                termID = self.db.get_ID("keyword","word",term)
                validTermID.append(termID)
 
        wordScore = self.scoreWord(validTermID)

        docScore = self.scoreDoc(wordScore)

        stopTimer = timeit.default_timer()

        return docScore,stopTimer-startTimer
        # except Exception as e:
        #     print(e)
        #     return {},0
    





        
