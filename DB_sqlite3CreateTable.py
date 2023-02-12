import sqlite3

conn = sqlite3.connect("testt.sqlite3")

cursor = conn.cursor()  

# cursor.execute("DROP TABLE domain")

createWebsites = """CREATE TABLE IF NOT EXISTS websites (
                    websiteID INTEGER PRIMARY KEY AUTOINCREMENT,
                    URL text,
                    title text,
                    content text,
                    last_crawl DATETIME)"""

cursor.execute(createWebsites)

createDomain = """CREATE TABLE IF NOT EXISTS domain (
                    domainID INTEGER PRIMARY KEY AUTOINCREMENT,
                    domainName text,
                    domainLocation text,
                    count INTEGER )"""

cursor.execute(createDomain)

createDomain = """CREATE TABLE IF NOT EXISTS backlinks (
                    websiteID INTEGER,
                    backlink text,
                    FOREIGN KEY (websiteID) REFERENCES websites(websiteID) ON DELETE CASCADE )"""

cursor.execute(createDomain)

createDomainLink = """CREATE TABLE IF NOT EXISTS DomainLink (
                    domainID INTEGER,
                    websiteID INTEGER,
                    FOREIGN KEY (websiteID) REFERENCES websites(websiteID) ON DELETE CASCADE,
                    FOREIGN KEY (domainID) REFERENCES domain(domainID) ON DELETE CASCADE )"""

cursor.execute(createDomainLink)

conn.commit()
conn.close()