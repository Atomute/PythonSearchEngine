import sqlite3
import re
import nltk
from nltk.tokenize import word_tokenize
from indexer.index_cleaner import Cleaning

class InvertedIndex:
    def __init__(self):
        self.conn = sqlite3.connect('testt.sl3')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inverted_index (
                index_id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                frequency INTEGER NOT NULL,
                websiteID INTEGER NOT NULL,
                FOREIGN KEY(websiteID) REFERENCES websites(websiteID)
            )
        """)
        
    def index_websites(self):
        self.cursor.execute("SELECT websiteID, title, content FROM websites")
        websites = self.cursor.fetchall()

        try:
            for website in websites:
                website_id = website[0]
                print("Id = "+ str(website_id))
                title = website[1]
                content = website[2]
                # Tokenize
                words = []
                if title:
                    title_words = Cleaning(title)
                    words += title_words.Lemma()
                if content:
                    content_words = Cleaning(content)
                    words += content_words.Lemma()

                word_freq = {}
                counter = 0
                for word in words:
                    counter += 1 
                    if word in word_freq:
                        word_freq[word] += 1
                    else:
                        word_freq[word] = 1
                for word, frequency in word_freq.items():
                    self.cursor.execute("INSERT INTO inverted_index (word, websiteID, frequency) VALUES (?, ?, ?)", (word, website_id, frequency))
            self.conn.commit()
        except KeyboardInterrupt:
            self.conn.commit()
        print('finished')