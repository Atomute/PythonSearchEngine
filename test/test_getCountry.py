import unittest
from unittest.mock import MagicMock,patch,call
import sys
sys.path.insert(1,"./")
from database.DB_sqlite3 import DB
from indexer.index_Country import Getcountry

class test_find_c_website_one(unittest.TestCase):
    def setUp(self):
        self.country = Getcountry()

    @patch('database.DB_sqlite3.DB.insert_website_country')
    @patch('database.DB_sqlite3.DB.insert_country')
    @patch('database.DB_sqlite3.DB.get_website_keywords')
    @patch('database.DB_sqlite3.DB.get_ID')
    def test_normal(self,mock_get_id,mock_get_website_keywords,mock_insert_country,mock_insert_website_country):
        mock_get_id.side_effect = [1,1]
        mock_get_website_keywords.return_value = [[1,"thailand"]]

        tester = self.country.find_c_websites_one("https://test")
        
        mock_insert_country.assert_called_with("thailand","THA")
        mock_insert_website_country.assert_called_with(1,1)

    @patch('database.DB_sqlite3.DB.insert_website_country')
    @patch('database.DB_sqlite3.DB.insert_country')
    @patch('database.DB_sqlite3.DB.get_website_keywords')
    @patch('database.DB_sqlite3.DB.get_ID')
    def test_webID_not_in_database(self,mock_get_id,mock_get_website_keywords,mock_insert_country,mock_insert_website_country):
        mock_get_id.side_effect = [None]

        tester = self.country.find_c_websites_one("https://test")
        self.assertEqual(tester,None)

    @patch('database.DB_sqlite3.DB.insert_website_country')
    @patch('database.DB_sqlite3.DB.insert_country')
    @patch('database.DB_sqlite3.DB.get_website_keywords')
    @patch('database.DB_sqlite3.DB.get_ID')
    def test_multiple_country(self,mock_get_id,mock_get_website_keywords,mock_insert_country,mock_insert_website_country):
        mock_get_id.side_effect = [1,1,2]
        mock_get_website_keywords.return_value = [[1,"thailand"],[2,"FRance"]]

        tester = self.country.find_c_websites_one("https://test")
        
        mock_insert_country.assert_has_calls([call("thailand","THA"),call("france","FRA")])
        mock_insert_website_country.assert_has_calls([call(1,1),call(1,2)])

    @patch('database.DB_sqlite3.DB.insert_website_country')
    @patch('database.DB_sqlite3.DB.insert_country')
    @patch('database.DB_sqlite3.DB.get_website_keywords')
    @patch('database.DB_sqlite3.DB.get_ID')
    def test_not_country(self,mock_get_id,mock_get_website_keywords,mock_insert_country,mock_insert_website_country):
        mock_get_id.side_effect = [1,1,2]
        mock_get_website_keywords.return_value = [[1,"car"],[2,"plane"]]

        tester = self.country.find_c_websites_one("https://test")
        
        mock_insert_country.assert_not_called()
        mock_insert_website_country.assert_not_called()

    @patch('database.DB_sqlite3.DB.insert_website_country')
    @patch('database.DB_sqlite3.DB.insert_country')
    @patch('database.DB_sqlite3.DB.get_website_keywords')
    @patch('database.DB_sqlite3.DB.get_ID')
    def test_have_country_and_notCountry(self,mock_get_id,mock_get_website_keywords,mock_insert_country,mock_insert_website_country):
        mock_get_id.side_effect = [1,1,3]
        mock_get_website_keywords.return_value = [[1,"germany"],[2,"car"],[3,"FRance"],[4,"plane"]]

        tester = self.country.find_c_websites_one("https://test")
        
        mock_insert_country.assert_has_calls([call("germany","DEU"),call("france","FRA")])
        mock_insert_website_country.assert_has_calls([call(1,1),call(1,3)])

if __name__ == "__main__":
    unittest.main() 