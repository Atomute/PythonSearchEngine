import pyodbc

class DB():
    def __init__(self):
        self.conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=localhost,1433;"
                      "Database=myDB;"
                      "UID=sa;"
                      "PWD=yourStrong(!)Password;")

        self.cursor = self.conn.cursor()
    
    def insert_websites(self,value):
        # take table name and tuple of value
        query = "INSERT INTO websites (ID, URL, title, content, last_crawl) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, value)

    def insert_keywords(self,value):
        query = "INSERT INTO keywords VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, value)

    def remove(self,table,row_ID):
        pass

    def get_table(self,name):
        self.cursor.execute("SELECT * FROM {}".format(name))
        return self.cursor.fetchall()

    def close_conn(self):
        self.conn.commit()
        self.conn.close()

# test = DB()

# test.update("websites",(3,'www','bonjour','wooh waaak','today'))
# test.close_conn()