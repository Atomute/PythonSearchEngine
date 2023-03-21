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

    @patch('database.DB_sqlite3.DB.get_word_for_search')
    def test_normal(self,mock_get_word):
        mock_get_word.return_value = [(1,7),(3,5),(2,0)]
        tester = self.searcher.scoreWord([1,2,3])

        self.assertEqual(tester,{1: 7.0, 3: 5.0, 2: 0.0})

    @patch('database.DB_sqlite3.DB.get_word_for_search')
    def test_all_zero_score(self,mock_get_word):
        mock_get_word.return_value = [(1,0),(2,0),(3,0)]
        tester = self.searcher.scoreWord([1,2,3])

        self.assertEqual(tester,{1: 0.0, 2: 0.0, 3: 0.0})

    @patch('database.DB_sqlite3.DB.get_word_for_search')
    def test_all_same_score(self,mock_get_word):
        mock_get_word.return_value = [(1,5),(3,5),(2,5)]
        tester = self.searcher.scoreWord([1,2,3])

        self.assertEqual(tester,{1: 0.0, 3: 0.0, 2: 0.0})

class test_scoreDoc(unittest.TestCase):
    def setUp(self):
        self.searcher = searcher()

    @patch('database.DB_sqlite3.DB.get_column_specific')
    @patch('database.DB_sqlite3.DB.get_MaxMin_Domain')
    def test_normal(self,mock_MaxMin,mock_get_column_specific):
        mock_MaxMin.return_value = [10,0]
        mock_get_column_specific.side_effect = ["https://domain1",[12],"https://domain2",[5]]
        tester = self.searcher.scoreDoc({1:0,2:0})

        self.assertEqual(tester,{1: 3.6, 2: 1.5})

if __name__ == "__main__":
    unittest.main()