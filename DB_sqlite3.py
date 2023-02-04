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

    def insert_keywords(self,value):
        # insert keywords to keywords table
        query = "INSERT INTO keywords VALUES (?, ?, ?)"
        self.cursor.execute(query, value)

    def remove(self,table,row_ID):
        pass

    def get_column(self,table,column):
        # get all item from "name" table
        self.cursor.execute("SELECT websites.URL FROM websites")
        return self.cursor.fetchall()

    def close_conn(self):
        # commit and close database
        self.conn.commit()
        self.conn.close()

# test = DB()

# test.update("websites",(3,'www','bonjour','wooh waaak','today'))
# test.close_conn()