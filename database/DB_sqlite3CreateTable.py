import sqlite3

def create_database(dbName):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()  

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

    createbacklinks = """CREATE TABLE IF NOT EXISTS externalDomain (
                        websiteID INTEGER,
                        exDomain text,
                        FOREIGN KEY (websiteID) REFERENCES websites(websiteID) ON DELETE CASCADE )"""
    cursor.execute(createbacklinks)

    # telling what domain are in this website
    # createDomainLink = """CREATE TABLE IF NOT EXISTS Websites_Domain (
    #                     websiteID INTEGER,
    #                     domainID INTEGER,
    #                     FOREIGN KEY (websiteID) REFERENCES websites(websiteID) ON DELETE CASCADE,
    #                     FOREIGN KEY (domainID) REFERENCES domain(domainID) ON DELETE CASCADE )"""
    # cursor.execute(createDomainLink)

    createCountry = """CREATE TABLE IF NOT EXISTS Country (
                    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country TEXT UNIQUE NOT NULL,
                    countryISO TEXT,
                    frequency INTEGER NOT NULL
                      )"""
    cursor.execute(createCountry)

    createWebsite_country = """CREATE TABLE IF NOT EXISTS Website_country (
                                website_id INTEGER NOT NULL,
                                wc_id INTEGER NOT NULL,
                                FOREIGN KEY (website_id) REFERENCES Websites (websiteID) ON DELETE CASCADE,
                                FOREIGN KEY (wc_id) REFERENCES Country (country_id))"""
    cursor.execute(createWebsite_country)

    createWebsite_inverted_index = """CREATE TABLE IF NOT EXISTS website_inverted_index (
                                    websiteID INTEGER NOT NULL,
                                    index_id INTEGER NOT NULL,
                                    frequency INTEGER NOT NULL,
                                    tfidf REAL,
                                    FOREIGN KEY(websiteID) REFERENCES websites(websiteID) ON DELETE CASCADE,
                                    FOREIGN KEY(index_id) REFERENCES keyword(index_id))"""
    cursor.execute(createWebsite_inverted_index)

    createKeyword = """CREATE TABLE IF NOT EXISTS keyword (
                    index_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT UNIQUE NOT NULL)"""
    cursor.execute(createKeyword)

    createLog = """CREATE TABLE IF NOT EXISTS log (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    root TEXT,
                    remaining TEXT,
                    withDepth TEXT)"""
    cursor.execute(createLog)

    conn.commit()
    conn.close()