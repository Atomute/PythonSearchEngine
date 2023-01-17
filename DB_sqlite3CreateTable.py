import sqlite3

conn = sqlite3.connect("database.sqlite")

cursor = conn.cursor()        
createWebsites = """CREATE TABLE IF NOT EXISTS websites (
                    websiteID INTEGER NOT NULL,
                    URL text NOT NULL,
                    title text,
                    content text,
                    last_crawl DATETIME,
                    PRIMARY KEY (websiteID,URL))"""

cursor.execute(createWebsites)

createkeywords = """CREATE TABLE IF NOT EXISTS keywords (
                    keywordID INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword text,
                    URL text,
                    count int)"""

cursor.execute(createkeywords)

conn.commit()
conn.close()