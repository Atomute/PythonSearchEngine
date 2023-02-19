import sqlite3
import sys
sys.path.insert(1,"./")
from indexer.index_cleaner import Cleaning
from database.DB_sqlite3 import DB

import time

class InvertedIndex:
    def __init__(self):
        self.start_time = time.time()
        self.db = DB("testt.sqlite3")

    def index_websites(self):
        self.db.cursor.execute("SELECT websiteID, title, content FROM websites")
        websites = self.db.cursor.fetchall()
        try:
            for website in websites:
                website_id = website[0]
                title = website[1]
                content = website[2]
                words = self.get_words(title, content)
                word_freq = self.get_word_freq(words)
                index_ids = self.add_words_to_index(word_freq)
                self.add_website_index_relation(website_id, index_ids)
            self.db.commit()
        except KeyboardInterrupt:
            self.db.commit()
        print('finished')
        print("--- %s seconds ---" % (time.time() - self.start_time))

    def get_words(self, title, content):
        words = []
        if title:
            title_words = Cleaning()
            words += title_words.process_text(title)
        if content:
            content_words = Cleaning()
            words += content_words.process_text(content)
        return words

    def get_word_freq(self, words):
        word_freq = {}
        counter = 0
        for word in words:
            counter += 1 
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        return word_freq

    def add_words_to_index(self, word_freq):
        index_ids = []
        for word, frequency in word_freq.items():
            self.db.cursor.execute("INSERT INTO Keyword (word, frequency) VALUES (?, ?)", (word, frequency))
            index_ids.append(self.db.cursor.lastrowid)
        self.db.commit()
        return index_ids

    def add_website_index_relation(self, website_id, index_ids):
        for index_id in index_ids:
            self.db.cursor.execute("INSERT INTO website_Keyword (websiteID, index_id) VALUES (?, ?)", (website_id, index_id))
        self.db.commit()

    def search(self, query):
        word_cleaner = Cleaning()
        words = word_cleaner.process_text(query)
        sql_query = """
        SELECT SUM(Keyword.frequency) as score, 
            websites.websiteID, 
            websites.URL, 
            websites.title, 
            website_inverted_index.index_id, 
            Keyword.word 
        FROM Keyword 
        JOIN website_inverted_index ON website_inverted_index.index_id = Keyword.index_id 
        JOIN websites ON websites.websiteID = website_inverted_index.websiteID 
        WHERE Keyword.word IN ({})
        GROUP BY websites.websiteID, Keyword.index_id
        ORDER BY score ASC
    """.format(','.join(['?'] * len(words)))

        self.db.cursor.execute(sql_query, words)
        results = self.db.cursor.fetchall()

        for result in results:
            score = result[0]
            website_id = result[1]
            url = result[2]
            title = result[3]
            index_id = result[4]
            word = result[5]

            print(f"Website ID: {website_id},Index ID: {index_id}, Word: {word}, Frequency: {score}")


        print(f"Found {len(results)} results for query: {query}")

a=InvertedIndex()
# print(a.get_words("Hello World","This is a sample content."))
a.index_websites()
a.search('card') 