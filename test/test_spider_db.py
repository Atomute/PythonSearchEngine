import unittest
from unittest.mock import patch
import os
import sys
from datetime import datetime
sys.path.insert(1,"./")
from spider.spider import spider
from database.DB_sqlite3 import DB

class test_push_domain(unittest.TestCase):
    def setUp(self) -> None:
        self.dbName = "unittesting.sqlite3"
        self.spider = spider()
        self.spider.db = DB(self.dbName)

    @patch('database.DB_sqlite3.DB.update_domain')
    @patch('database.DB_sqlite3.DB.get_column')
    def test_domain_already_in_database(self,mock_get_column,mock_update_domain):
        domain = "something.com"
        mock_get_column.return_value = ["something.com","wowwee.com"]
        self.spider.push_domain(domain)
        mock_update_domain.assert_called_with(domain,1)

    @patch('database.DB_sqlite3.DB.insert_domain')
    @patch('database.DB_sqlite3.DB.get_column')
    def test_domain_already_not_in_database(self,mock_get_column,mock_insert_domain):
        domain = "sample.com"
        mock_get_column.return_value = ["something.com","wowwee.com"]
        self.spider.push_domain(domain)
        mock_insert_domain.assert_called_with(domain)

    def tearDown(self):
        self.spider.db.close_conn()
        os.remove(self.dbName)

class test_push_websites(unittest.TestCase):
    def setUp(self) -> None:
        self.dbName = "unittesting.sqlite3"
        self.spider = spider()
        self.spider.db = DB(self.dbName)
        self.value = ("url","title","content",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @patch('database.DB_sqlite3.DB.update_websites')
    @patch('database.DB_sqlite3.DB.get_column')
    def test_websites_already_in_database(self,mock_get_column,mock_update_websites):
        url = "https://www.something.com"
        mock_get_column.return_value = ["https://www.something.com","https://wowwee.com"]
        self.spider.push_websites(self.value,url)
        mock_update_websites.assert_called_with(self.value)

    @patch('database.DB_sqlite3.DB.insert_websites')
    @patch('database.DB_sqlite3.DB.get_column')
    def test_domain_already_not_in_database(self,mock_get_column,mock_insert_websites):
        url = "https://www.nothing.com"
        mock_get_column.return_value = ["https://something.com","https://wowwee.com"]
        self.spider.push_websites(self.value,url)
        mock_insert_websites.assert_called_with(self.value)

    def tearDown(self) -> None:
        self.spider.db.close_conn()
        os.remove(self.dbName)

class test_push_backlinks(unittest.TestCase):
    def setUp(self):
        self.dbName = "unittesting.sqlite3"
        self.spider = spider()
        self.spider.db = DB(self.dbName)
        self.spider.currentURL = "currentURL"

    @patch('database.DB_sqlite3.DB.get_column')
    @patch('database.DB_sqlite3.DB.get_ID')
    def test_website_is_in_backlinks(self,mock_get_ID,mock_get_column):
        self.spider.exlinks = ["something"]
        mock_get_ID.return_value = 1
        mock_get_column.return_value = [1,2,3]
        self.spider.push_backlinks(self.spider.exlinks)
        self.assertEqual(self.spider.exlinks,[])

    @patch('database.DB_sqlite3.DB.insert_exlink')
    @patch('database.DB_sqlite3.DB.get_column')
    @patch('database.DB_sqlite3.DB.get_ID')
    def test_website_is_not_in_backlinks(self,mock_get_ID,mock_get_column,mock_insert_exlink):
        self.spider.exlinks = ["something"]
        mock_get_ID.return_value = 1
        mock_get_column.return_value = [2,3]
        self.spider.push_backlinks(self.spider.exlinks)
        mock_insert_exlink.assert_called_with(1,"something")

    def tearDown(self):
        self.spider.db.close_conn()
        os.remove(self.dbName)

class test_domain_counter(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = spider()

    @patch('database.DB_sqlite3.DB.get_column')
    def test_normal(self,mock_get_column):
        mock_get_column.return_value = []

    def test_(self):
        pass

    def test_something(self):
        pass