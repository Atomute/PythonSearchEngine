import sqlite3

conn = sqlite3.connect("testt.sl3")

cursor = conn.cursor()  

# cursor.execute("DROP TABLE domain")

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

createDomain = """CREATE TABLE IF NOT EXISTS domain (
                    domainID INTEGER PRIMARY KEY AUTOINCREMENT,
                    domainName text,
                    count INTEGER )"""

cursor.execute(createDomain)

conn.commit()
conn.close()