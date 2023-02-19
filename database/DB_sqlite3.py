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
        query = "REPLACE INTO domain (domainName, count) VALUES (?, ?)"
        self.cursor.execute(query, value)

    def update_domain(self,domain,count):
        value = (domain,count,domain)
        query = " UPDATE domain SET domainName = ?, count = ? WHERE domainName = ? "
        self.cursor.execute(query, value)

    def insert_exlink(self,websiteID,exlink):
        # insert keywords to keywords table
        value = (websiteID,exlink)
        query = "INSERT INTO backlinks VALUES (?, ?)"
        self.cursor.execute(query, value)

    def insert_Websites_Domain(self,websitID,domainID):
        query = """INSERT INTO Websites_Domain VALUES (?, ?)"""
        value = (websitID,domainID)

        self.cursor.execute(query,value)

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
        # get all item from "name" table
        self.cursor.execute("SELECT {}.{} FROM {} ORDER BY {}".format(table,column,table,column))
        rows = self.cursor.fetchall()
        ans = [row[0] for row in rows]

        return ans
    
    def get_column_specific(self,table,column,value,*sec_column):
        if not sec_column: sec_column = [column]
        self.cursor.execute("SELECT {}.{} FROM {} WHERE {}='{}'".format(table,column,table,sec_column[0],value))
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
        query = "SELECT * FROM {} WHERE {} = '{}'".format(table,column,url)
        self.cursor.execute(query)
        id = self.cursor.fetchall()
        ans = id[0][0]

        return ans
    
    def get_domainCount():
        pass
    
    def dump_record(self,table,column,value):
        query = "DELETE FROM {} WHERE {}={}".format(table,column,value)
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
