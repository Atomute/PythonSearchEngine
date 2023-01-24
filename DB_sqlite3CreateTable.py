import sqlite3

conn = sqlite3.connect("testt.sqlite")

cursor = conn.cursor()        
createWebsites = """CREATE TABLE IF NOT EXISTS websites (
                    URL text NOT NULL,
                    title text,
                    content text,
                    last_crawl DATETIME,
                    PRIMARY KEY (URL))"""

cursor.execute(createWebsites)

createwebID = """CREATE TABLE IF NOT EXISTS webID (
                    websiteID INTEGER PRIMARY KEY AUTOINCREMENT,
                    URL text NOT NULL)"""

cursor.execute(createwebID)

createkeywords = """CREATE TABLE IF NOT EXISTS keywords (
                    keywordID INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword text,
                    URL text,
                    count int)"""

cursor.execute(createkeywords)

conn.commit()
conn.close()