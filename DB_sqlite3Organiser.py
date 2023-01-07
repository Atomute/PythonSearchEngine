import sqlite3

conn = sqlite3.connect("test.db")

cursor = conn.cursor()        
createWebsites = """CREATE TABLE websites (
                    ID int,
                    URL text,
                    title text,
                    content text,
                    last_crawl DATETIME)"""

cursor.execute(createWebsites)

createkeywords = """CREATE TABLE keywords (
                    keywordID int,
                    keyword text,
                    URL text,
                    count int)"""

cursor.execute(createkeywords)

conn.commit()
conn.close()