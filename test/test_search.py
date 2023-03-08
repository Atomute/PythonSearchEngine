import unittest
from unittest.mock import MagicMock,patch
import sys
sys.path.insert(1,"./")
from spider.spider import spider
from database.DB_sqlite3 import DB
from search.main import searcher

class test_searcher(unittest.TestCase):
    def setUp(self):
        self.searcher = searcher()

    def test_type(self):
        # return type should be list
        test_query = "search query"
        tester = self.searcher.search(test_query)

        self.assertIsInstance(tester,list)

    # def test_normal(self):
    #     # return list should contain website ID integer
    #     test_query = "something"
    #     tester = self.searcher.search(test_query)

    #     self.assertEqual(tester,[])

if __name__ == "__main__":
    unittest.main()