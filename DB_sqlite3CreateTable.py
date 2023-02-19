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
                    count INTEGER )"""
cursor.execute(createDomain)

createbacklinks = """CREATE TABLE IF NOT EXISTS backlinks (
                    websiteID INTEGER,
                    backlink text,
                    FOREIGN KEY (websiteID) REFERENCES websites(websiteID) ON DELETE CASCADE )"""
cursor.execute(createbacklinks)

# telling what domain are in this website
createDomainLink = """CREATE TABLE IF NOT EXISTS Websites_Domain (
                    websiteID INTEGER,
                    domainID INTEGER,
                    FOREIGN KEY (websiteID) REFERENCES websites(websiteID) ON DELETE CASCADE,
                    FOREIGN KEY (domainID) REFERENCES domain(domainID) ON DELETE CASCADE )"""
cursor.execute(createDomainLink)

createKeyword = """CREATE TABLE IF NOT EXISTS Keyword (
                index_id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                frequency INTEGER NOT NULL)"""
cursor.execute(createKeyword)

createWebsites_Keyword = """CREATE TABLE IF NOT EXISTS website_keyword (
                            invert_index_key INTEGER PRIMARY KEY AUTOINCREMENT,
                            websiteID INTEGER NOT NULL,
                            index_id INTEGER NOT NULL,
                            FOREIGN KEY(websiteID) REFERENCES websites(websiteID),
                            FOREIGN KEY(index_id) REFERENCES inverted_index(index_id))"""
cursor.execute(createWebsites_Keyword)

conn.commit()
conn.close()