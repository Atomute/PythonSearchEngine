from database.DB_sqlite3 import *


class updater:
    def __init__(self):
        self.db = DB()

    def update(self):
        pass

    def get_webToupdate(self):
        print(self.db.get_column("websites","URL"))

test = updater()
test.get_webToupdate()