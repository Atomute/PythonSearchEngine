import pycountry
import time
import sqlite3
from geopy.geocoders import Nominatim

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
                    geolocator = Nominatim(user_agent="my_app")

                    location = geolocator.geocode(word)
                    latitude = location.latitude
                    longitude = location.longitude

                    self.cursor.execute("INSERT OR IGNORE INTO Country (country,latitude,longtitude) VALUES (?,?,?)", (word,latitude,longitude,))
                    self.cursor.execute("SELECT country_id FROM Country WHERE country=?", (word,))
                    country_id = self.cursor.fetchone()[0]
                    self.cursor.execute("INSERT INTO Website_country (website_id, wc_id) VALUES (?, ?)", (website_id, country_id))
                    print(website_id, word)
            self.conn.commit()
        except KeyboardInterrupt:
            self.conn.commit()