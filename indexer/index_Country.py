import pycountry
import time
import sqlite3

class Getcountry:
    def __init__(self):
        self.all_c=[]
        self.start_time = time.time()
        self.conn = sqlite3.connect('testt.sqlite3')
        self.cursor = self.conn.cursor()

    def find_c_websites(self):
        country_list = [country.name.lower() for country in pycountry.countries]
        self.cursor.execute("SELECT keyword.index_id, website_inverted_index.websiteID, word FROM keyword JOIN website_inverted_index ON website_inverted_index.index_id = keyword.index_id JOIN websites ON websites.websiteID = website_inverted_index.websiteID")
        websites = self.cursor.fetchall()
        try:
            for website in websites:
                index_id = website[0]
                website_id = website[1]
                word = website[2].lower()
                if word in country_list:
                    country_code = pycountry.countries.search_fuzzy(word)[0].alpha_3
                    self.cursor.execute("INSERT OR IGNORE INTO Country (country, countryISO) VALUES (?,?)", (word,country_code))
                    self.cursor.execute("SELECT country_id FROM Country WHERE countryISO=?", (country_code,))
                    country_id = self.cursor.fetchone()[0]
                    self.cursor.execute("INSERT INTO Website_country (website_id, wc_id) VALUES (?, ?)", (website_id, country_id))
                    # print(website_id, word)
            self.conn.commit()
        except KeyboardInterrupt:
            self.conn.commit()

    def find_c_websites_one(self, website_url):
        country_list = [country.name.lower() for country in pycountry.countries]
        self.cursor.execute("SELECT websiteID FROM websites WHERE URL = ?", (website_url,))
        website_id = self.cursor.fetchone()
        if website_id is None:
            print("Error: website not found in database.")
            return
        website_id = website_id[0]
        self.cursor.execute("SELECT website_inverted_index.index_id, word FROM keyword JOIN website_inverted_index ON website_inverted_index.index_id = keyword.index_id WHERE website_inverted_index.websiteID = ?", (website_id,))
        website_keywords = self.cursor.fetchall()
        country_freq = {}
        try:
            for keyword in website_keywords:
                word = keyword[1].lower()
                if word in country_list:
                    country_code = pycountry.countries.search_fuzzy(word)[0].alpha_3
                    self.cursor.execute("INSERT OR IGNORE INTO Country (country,countryISO) VALUES (?, ?)", (word,country_code))

                    self.cursor.execute("SELECT country_id FROM Country WHERE countryISO=?", (country_code,))
                    country_id = self.cursor.fetchone()[0]
                    if country_id in country_freq:
                        country_freq[country_id] += 1
                    else:
                        country_freq[country_id] = 1
                    self.cursor.execute("INSERT INTO Website_country (website_id, wc_id) VALUES (?, ?)", (website_id, country_id))
            for country_id, freq in country_freq.items():
                self.cursor.execute("UPDATE Website_country SET frequency = ? WHERE website_id = ? AND wc_id = ?", (freq, website_id, country_id))
            self.conn.commit()
        except KeyboardInterrupt:
            self.conn.commit()
