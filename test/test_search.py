import unittest
from unittest.mock import MagicMock,patch
import sys
sys.path.insert(1,"./")
from spider.spider import spider
from database.DB_sqlite3 import DB
from search.searcher import searcher

class test_scoreWord(unittest.TestCase):
    def setUp(self):
        self.searcher = searcher()

    @patch('database.DB_sqlite3.DB.connect.cursor.fetchall')
    def test_normal(self,mock_cursor):
        mock_cursor.return_value = [(1,3,3.5),(2,2,0),(3,1,5)]
        tester = self.searcher.scoreWord([1,2,3])

        self.assertEqual(tester,{})
        


    # def test_normal(self):
    #     # return list should contain website ID integer
    #     test_query = "something"
    #     tester = self.searcher.search(test_query)

    #     self.assertEqual(tester,[])

if __name__ == "__main__":
    unittest.main()