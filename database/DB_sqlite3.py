import sqlite3
import database.DB_sqlite3CreateTable as DB_sqlite3CreateTable

class DB():
    def __init__(self,database):
        DB_sqlite3CreateTable.create_database(database)
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

        self.cursor.execute("PRAGMA foreign_keys = ON")

    def insert_websites(self,value):
        query = "REPLACE INTO websites (URL, title, content, last_crawl) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, value)

    def update_websites(self,value):
        val = list(value)
        val.append(val[0])
        query = "UPDATE websites SET URL = ?, title = ?, content = ?, last_crawl = ? WHERE URL = ? "
        self.cursor.execute(query, tuple(val))

    def insert_domain(self,domain):
        value = (domain,1)
        query = "REPLACE INTO domain (domainName, count) VALUES (?, ?)"
        self.cursor.execute(query, value)

    def update_domain(self,domain,count):
        value = (domain,count,domain)
        query = " UPDATE domain SET domainName = ?, count = ? WHERE domainName = ? "
        self.cursor.execute(query, value)

    def insert_exlink(self,websiteID,exlink):
        # insert keywords to keywords table
        value = (websiteID,exlink)
        query = "INSERT INTO externalDomain VALUES (?, ?)"
        self.cursor.execute(query, value)

    def insert_Websites_Domain(self,websitID,domainID):
        query = """INSERT INTO Websites_Domain VALUES (?, ?)"""
        value = (websitID,domainID)

        self.cursor.execute(query,value)

    def insert_country(self,word,country_code):
        self.cursor.execute("INSERT OR IGNORE INTO Country (country,countryISO) VALUES (?, ?)", (word,country_code))
        self.commit()

    def insert_website_country(self,website_id,country_id):
        self.cursor.execute("INSERT INTO Website_country (website_id, wc_id) VALUES (?, ?)", (website_id, country_id))
        self.commit()

    def remove(self,table,row_ID):
        pass

    def get_lastrowID_websites(self):
        query = "SELECT sqlite_sequence.seq FROM sqlite_sequence WHERE name='websites'"
        self.cursor.execute(query)
        ID = self.cursor.fetchone()
        return ID[0]

    def get_table(self,table):
        # get all item in table
        self.cursor.execute("SELECT * FROM {}".format(table))
        rows = self.cursor.fetchall()
        ans = [row for row in rows]

        return ans

    def get_column(self,table,column):
        # get all item from one specify column and specify table
        self.cursor.execute("SELECT {}.{} FROM {} ORDER BY {}".format(table,column,table,column))
        rows = self.cursor.fetchall()
        ans = [row[0] for row in rows]
        if ans == [""]:
            return []

        return ans
    
    def get_column_specific(self,table,column,value,*sec_column):
        if not sec_column: sec_column = [column]
        if type(value) != str:
            self.cursor.execute("SELECT {}.{} FROM {} WHERE {}={}".format(table,column,table,sec_column[0],value))
            rows = self.cursor.fetchall()
            ans = [row[0] for row in rows]

            return ans
        self.cursor.execute("SELECT {}.{} FROM {} WHERE {}='{}'".format(table,column,table,sec_column[0],value))
        rows = self.cursor.fetchall()
        ans = [row[0] for row in rows]

        return ans
    
    def get_visited_url(self,table,column,value,*sec_column):
        if not sec_column: sec_column = [column]
        self.cursor.execute("SELECT {}.{} FROM {} WHERE {} LIKE '{}%' OR {}='{}'".format(table,column,table,sec_column[0],value,sec_column[0],value))
        rows = self.cursor.fetchall()
        ans = [row[0] for row in rows]

        return ans
    
    def get_oldBacklink(self,ID):
        query = "SELECT backlinks.backlink FROM backlinks WHERE websiteID = {}".format(ID)
        self.cursor.execute(query)
        id = self.cursor.fetchone()
        ans = id[0]

        return ans
    
    def get_ID(self,table,column,url):
        query = "SELECT * FROM {} WHERE {} LIKE '%{}%'".format(table,column,url)
        self.cursor.execute(query)
        id = self.cursor.fetchall()
        if id == []: return None
        ans = id[0][0]

        return ans
    
    def get_website_keywords(self,website_id):
        self.cursor.execute("SELECT website_inverted_index.index_id, word FROM keyword JOIN website_inverted_index ON website_inverted_index.index_id = keyword.index_id WHERE website_inverted_index.websiteID = ?", (website_id,))
        website_keywords = self.cursor.fetchall()
        return website_keywords
    
    def get_word_for_search(self,terms):
        self.cursor.execute("""SELECT websiteID, COUNT(websiteID)*SUM(tfidf) AS score 
                                FROM website_inverted_index 
                                WHERE index_id IN ({}) 
                                GROUP BY websiteID 
                                ORDER BY score DESC""".format(",".join(str(i) for i in terms)))
        results = self.cursor.fetchall()
        return results
    
    def get_MaxMin_Domain(self):
        self.cursor.execute("SELECT MAX(count), MIN(count) FROM domain")
        result = self.cursor.fetchall()[0]
        return result
    
    def get_domainCount():
        pass

    def get(self,website_url):
        self.cursor.execute("SELECT websiteID FROM websites WHERE URL = ?", (website_url,))
        website_id = self.cursor.fetchone()
        return website_id
    
    def dump_record(self,table,column,value):
        if type(value) == int:
            query = "DELETE FROM {} WHERE {}={}".format(table,column,value)
        else:
            query = "DELETE FROM {} WHERE {}='{}'".format(table,column,value)
        self.cursor.execute(query)

    def dump_table(self):
        query = "DELETE FROM websites"
        self.cursor.execute(query)

    def commit(self):
        # only commit
        self.conn.commit()

    def close_conn(self):
        # commit and close database
        self.conn.commit()
        self.conn.close()

    def for_test():
        pass
