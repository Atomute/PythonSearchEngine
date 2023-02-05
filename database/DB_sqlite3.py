import sqlite3

class DB():
    def __init__(self):
        self.conn = sqlite3.connect("testt.sl3")

        self.cursor = self.conn.cursor()

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

    def update_domain(self,value):
        query = "UPDATE domain SET domainName = ?, count = count+1 WHERE domainName = ? "
        self.cursor.execute(query, value)

    def insert_keywords(self,value):
        # insert keywords to keywords table
        query = "INSERT INTO keywords VALUES (?, ?, ?)"
        self.cursor.execute(query, value)

    def remove(self,table,row_ID):
        pass

    def get_column(self,table,column):
        # get all item from "name" table
        self.cursor.execute("SELECT {}.{} FROM {}".format(table,column,table))
        rows = self.cursor.fetchall()
        ans = [row[0] for row in rows]

        return ans

    def close_conn(self):
        # commit and close database
        self.conn.commit()
        self.conn.close()