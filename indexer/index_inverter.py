import sqlite3
import sys
sys.path.insert(1,"./")
from indexer.index_cleaner import Cleaning
import time
from math import log
import timeit

class InvertedIndex:
    def __init__(self):
        self.start_time = time.time()
        self.conn = sqlite3.connect('testt.sqlite3')
        self.cursor = self.conn.cursor()

    def indexOneWebsite(self,url):
        self.cursor.execute("SELECT websiteID, title, content FROM websites WHERE URL='{}'".format(url))
        websites = self.cursor.fetchall()
        try:
            for website in websites:
                website_id = website[0]
                title = website[1]
                content = website[2]
                words = self.get_words(title, content)
                word_freq = self.get_word_freq(words)
                index_ids = self.add_words_to_index(word_freq)
                self.add_website_index_relation(website_id, index_ids, word_freq)
            self.conn.commit()
        except KeyboardInterrupt:
            self.conn.commit()
        # print('finished')
        # print("--- %s seconds ---" % (time.time() - self.start_time))

    def index_websites(self):
        self.cursor.execute("SELECT websiteID, title, content FROM websites")
        websites = self.cursor.fetchall()
        try:
            for website in websites:
                website_id = website[0]
                title = website[1]
                content = website[2]
                words = self.get_words(title, content)
                word_freq = self.get_word_freq(words)
                index_ids = self.add_words_to_index(word_freq)
                self.add_website_index_relation(website_id, index_ids, word_freq)
            self.conn.commit()
        except KeyboardInterrupt:
            self.conn.commit()
        # print('finished')
        # print("--- %s seconds ---" % (time.time() - self.start_time))

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
        for word in words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        return word_freq

    def add_words_to_index(self, word_freq):
        index_ids = []
        for word in word_freq.keys():
            self.cursor.execute("INSERT OR IGNORE INTO keyword (word) VALUES (?)", (word,))
            self.cursor.execute("SELECT index_id FROM keyword WHERE word=?", (word,))
            index_id = self.cursor.fetchone()[0]
            index_ids.append(index_id)
        self.conn.commit()
        return index_ids

    def add_website_index_relation(self, website_id, index_ids, word_freq):
        for index_id in index_ids:
            frequency = word_freq[self.get_word_from_index_id(index_id, self.cursor)]
            self.cursor.execute("INSERT INTO website_inverted_index (websiteID, index_id, frequency) VALUES (?, ?, ?)", (website_id, index_id, frequency))
        self.conn.commit()

    def get_word_from_index_id(self, index_id, cursor):
        cursor.execute("SELECT word FROM keyword WHERE index_id=?", (index_id,))
        return cursor.fetchone()[0]

    def calculate_tfidf(self):
        # Get the total number of documents
        start = timeit.default_timer()
        self.cursor.execute("SELECT COUNT(*) FROM websites")
        total_docs = self.cursor.fetchone()[0]
        
        # Loop through each word in the inverted index
        self.cursor.execute("SELECT index_id FROM keyword")
        index_ids = [row[0] for row in self.cursor.fetchall()]

        self.cursor.execute("SELECT COUNT(*) FROM website_inverted_index")
        lenght = self.cursor.fetchone()[0]
        counter = 0
        for index_id in index_ids:
            
            # Get the documents that contain the word
            self.cursor.execute("SELECT websiteID, frequency FROM website_inverted_index WHERE index_id=?", (index_id,))
            rows = self.cursor.fetchall()
            
            # Calculate the IDF score for the word
            num_docs_with_word = len(rows)
            idf = log(total_docs / num_docs_with_word)
            
            # Update the TF-IDF score for each document that contains the word
            for row in rows:
                counter += 1

                website_id = row[0]
                tf = row[1]
                tfidf = tf * idf
                self.cursor.execute("UPDATE website_inverted_index SET tfidf=? WHERE websiteID=? AND index_id=?", (tfidf, website_id, index_id))
                self.conn.commit()

                print(f"{counter}",end="\r")
            
            yield counter*100/lenght
        stop = timeit.default_timer()
        print(stop-start)
        
        