import sqlite3

class DB():
    def __init__(self,dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def create_table(self,name):
        self.cursor.execute("""CREATE TABLE {} (
                                ID integer,
                                url text,
                                title text,
                                p text
                                )""".format(name))

    def update(self,name,value):
        # take table name and tuple of value
        self.cursor.execute("INSERT INTO {} VALUES {}".format(name,value))

    def get_table(self,name):
        self.cursor.execute("SELECT * FROM {}".format(name))
        return self.cursor.fetchall()

    def close_conn(self):
        self.conn.commit()
        self.conn.close()
