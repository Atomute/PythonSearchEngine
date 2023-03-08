import unittest
from unittest.mock import MagicMock,patch
import os
import sys
from datetime import datetime
sys.path.insert(1,"./")
from spider.spider import spider
from database.DB_sqlite3 import DB

class test_domain_counter(unittest.TestCase):
    def setUp(self) -> None:
        self.dbName = "unittesting.sqlite3"
        self.spider = spider()
        self.db = DB(self.dbName)
        self.spider.db = self.db
    
    @patch('database.DB_sqlite3.DB.get_column')
    def test_normal(self,mock_get_column):
        mock_get_column.side_effect = [[],[1,1,1,1,2],[1,2,3]]
        self.spider.push_domain("domain1")

        self.spider.domain_counter()

        self.db.cursor.execute("SELECT count FROM domain WHERE domainID = 1")
        domainCount = self.db.cursor.fetchone()[0]

        self.assertEqual(domainCount,4)

    @patch('database.DB_sqlite3.DB.get_column')
    def test_ori_not_in_counter(self,mock_get_column):
        mock_get_column.side_effect = [[],[1,1,1,1,3,3,3],[2,3]]
        self.spider.push_domain("domain1")

        self.spider.domain_counter()

        self.db.cursor.execute("SELECT count FROM domain WHERE domainID = 3")
        domainCount = self.db.cursor.fetchall()

        self.assertEqual(domainCount,[])

    def tearDown(self) -> None:
        self.spider.db.close_conn()
        os.remove(self.dbName)

class test_removeOne(unittest.TestCase):
    def setUp(self):
        self.dbName = "unittesting.sqlite3"
        self.spider = spider()
        self.db = DB(self.dbName)
        self.spider.db = self.db

    @patch('database.DB_sqlite3.DB.get_column')
    @patch('database.DB_sqlite3.DB.get_ID')
    def test_remove_from_foreign(self,mock_get_ID,mock_get_column):
        mock_get_ID.side_effect = [1,1,2]
        mock_get_column.return_value = []

        self.spider.currentURL = "https://firstdomain"
        value = (None,None,None,None)
        exlinks = ["exlink1","exlink2"]
        self.spider.push_websites(value,"https://firstdomain")
        self.spider.push_websites(value,"https://seconddomain")
        self.spider.push_backlinks(exlinks)

        urltoremove = "https://firstdomain"
        self.spider.removeone(urltoremove)

        self.db.cursor.execute("SELECT websiteID FROM websites")
        websites = self.db.cursor.fetchone()[0]
        self.db.cursor.execute("SELECT websiteID FROM backlinks")
        backlinks = [x[0] for x in self.db.cursor.fetchall()]

        self.assertEqual([websites,backlinks],[2,[]])

    @patch('database.DB_sqlite3.DB.get_column_specific')
    @patch('database.DB_sqlite3.DB.get_column')
    @patch('database.DB_sqlite3.DB.get_ID')
    def test_remove_from_domain(self,mock_get_ID,mock_get_column,mock_get_column_specific):
        # domain is a table with no foreign key
        mock_get_ID.side_effect = [1,1]
        mock_get_column.return_value = []
        mock_get_column_specific.return_value = []



    def test_remove_from_country(self):
        pass

    def test_remove_from_keyword(self):
        pass

    def tearDown(self) -> None:
        self.spider.db.close_conn()
        os.remove(self.dbName)

# class test_updateOne(unittest.TestCase):
#     def setUp(self):
#         self.dbName = "unittesting.sqlite3"
#         self.spider = spider()
#         self.spider.db = DB(self.dbName)
#         self.spider.currentURL = "currentURL"

#     def test_update_to_websites(self):
#         pass

#     def test_update_to_backlinks(self):
#         pass

#     def test_update_to_keyword(self):
#         pass

#     def test_update_to_domain(self):
#         pass

#     def test_update_to_websites_domain(self):
#         pass

#     def test_update_to_website_inverted_index(self):
#         pass

#     def tearDown(self):
#         self.spider.db.close_conn()
#         os.remove(self.dbName)

if __name__ == "__main__":
    unittest.main()