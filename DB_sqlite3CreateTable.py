import sqlite3

conn = sqlite3.connect("test.sqlite")

cursor = conn.cursor()        
createWebsites = """CREATE TABLE IF NOT EXISTS websites (
                    websiteID INTEGER PRIMARY KEY AUTOINCREMENT,
                    URL text,
                    title text,
                    content text,
                    last_crawl DATETIME)"""

cursor.execute(createWebsites)

createkeywords = """CREATE TABLE IF NOT EXISTS keywords (
                    keywordID INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword text,
                    URL text,
                    count int)"""

cursor.execute(createkeywords)

conn.commit()
conn.close()