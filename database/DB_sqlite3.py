import sqlite3

class DB():
    def __init__(self,database):
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

    def insert_domain(self,value):
        query = "REPLACE INTO domain (domainName, domainLocation, count) VALUES (?, ?, ?)"
        self.cursor.execute(query, value)

    def update_domain(self,domain):
        value = (domain,domain)
        query = "UPDATE domain SET domainName = ?, count = count+1 WHERE domainName = ? "
        self.cursor.execute(query, value)

    def insert_exlink(self,websiteID,exlink):
        # insert keywords to keywords table
        value = (websiteID,exlink)
        query = "INSERT INTO backlinks VALUES (?, ?)"
        self.cursor.execute(query, value)

    def remove(self,table,row_ID):
        pass

    def get_column(self,table,column):
        # get all item from "name" table
        self.cursor.execute("SELECT {}.{} FROM {}".format(table,column,table))
        rows = self.cursor.fetchall()
        ans = [row[0] for row in rows]

        return ans
    
    def get_oldBacklink(self,url):
        query = "SELECT backlinks.backlink FROM backlinks WHERE websiteID = '{}'".format(url)
        self.cursor.execute(query)
        id = self.cursor.fetchone()
        ans = id[0]

        return ans
    
    def get_specElement(self,table,column,url):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(table,column,url)
        self.cursor.execute(query)
        id = self.cursor.fetchall()
        ans = id[0][0]

        return ans
    
    def dump_record(self,table,column,value):
        query = "DELETE FROM {} WHERE {}={}".format(table,column,value)
        self.cursor.execute(query)

    def commit(self):
        # only commit
        self.conn.commit()

    def close_conn(self):
        # commit and close database
        self.conn.commit()
        self.conn.close()