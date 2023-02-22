import unittest
from unittest.mock import MagicMock,patch
import os
import sys
from datetime import datetime
sys.path.insert(1,"./")
from spider.spider import spider
from database.DB_sqlite3 import DB

class test_get_title(unittest.TestCase):
    def setUp(self):
        self.test_scraper = spider()

    def test_normal(self,):
        self.assertIsInstance(self.test_scraper.get_title("<html> <title>This is title</title> </html>"),str)

    def test_notitle(self):
        self.assertEqual(self.test_scraper.get_title(""),None)

    def test_empty_title(self):
        self.assertEqual(self.test_scraper.get_title("<title></title>"),None)

    def test_space_title(self):
        self.assertEqual(self.test_scraper.get_title("<title> </title>"),None)

    def test_wrong_title(self):
        self.assertEqual(self.test_scraper.get_title("</title>"),None)
    
    def test_exact(self):
        self.assertEqual(self.test_scraper.get_title("<title>   This is title </title>"),"This is title")

class test_get_contents(unittest.TestCase):
    def setUp(self):
        self.test_scraper = spider()

    def test_normal(self):
        tester = self.test_scraper.get_contents("<body> <p>Hi</p>   <div>Hello</div> <span>Bonjour</span> </body>")

        self.assertIsInstance(tester,str)

    def test_noContent(self):
        tester = self.test_scraper.get_contents("")

        self.assertEqual(tester,None)

    def test_empty_body(self):
        tester = self.test_scraper.get_contents("<body></body>")

        self.assertEqual(tester,None)

    def test_space_body(self):
        tester = self.test_scraper.get_contents("<body>      </body>")

        self.assertEqual(tester,None)

    def test_wrong_body(self):
        tester = self.test_scraper.get_contents("<body>")

        self.assertEqual(tester,None)

    def test_empty_obj_in_body(self):
        tester = self.test_scraper.get_contents("<body> <Div></div> <p></p> <span></span> </body>")

        self.assertEqual(tester,None)    

    def test_exact(self):
        tester = self.test_scraper.get_contents("<body>      <Div>Menu</div>            <p>This is paragraph</p> <span>This is span</span>     </body>")

        self.assertEqual(tester,"Menu This is paragraph This is span")    

class test_get_links(unittest.TestCase):
    def setUp(self):
        self.spider = spider()
        self.spider.rootDomain = "root.com"
        self.spider.currentURL = "https://www.root.com/"

    def test_normal(self):
        tester = self.spider.get_links("url")

        self.assertIsInstance(tester,list)

    def test_one_link(self):
        tester = self.spider.get_links("<html> <body> <a href='https://www.root.com/firstpage'>something</a> </body> </html>")

        self.assertEqual(tester,['https://www.root.com/firstpage'])

    def test_multiple_link(self):
        tester = self.spider.get_links("<html> <body> <a href='https://www.root.com/firstpage'>something</a> <a href='https://www.root.com/secondpage'>something</a> </body> </html>")

        self.assertEqual(tester,['https://www.root.com/firstpage','https://www.root.com/secondpage'])

    def test_numbersign(self):
        tester = self.spider.get_links("<a href='#numbersign'>something</a>")

        self.assertEqual(tester,[])

    def test_notinroot(self):
        tester = self.spider.get_links("<a href='https://www.something.com/'>something</a>")

        self.assertEqual(tester,[])

    def test_no_link(self):
        tester = self.spider.get_links("no link here")

        self.assertEqual(tester,[])

    def test_exlinks(self):
        self.spider.get_links("<a href='https://www.something.com/'>something</a>")
        tester = self.spider.exlinks

        self.assertEqual(tester,['https://www.something.com/'])

class test_extractDomain(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = spider()

    def test_normal(self):
        tester = self.spider.extractDomain("https://www.something.com/")

        self.assertIsInstance(tester,str)

    def test_noLink(self):
        tester = self.spider.extractDomain("not a link")

        self.assertEqual(tester,None)

    def test_wrongLink(self):
        tester = self.spider.extractDomain("https:/www.something.com/")

        self.assertEqual(tester,None)

    def test_https(self):
        tester = self.spider.extractDomain("https://something.com/wow")
        self.assertEqual(tester,"something.com")

    def test_http(self):
        tester = self.spider.extractDomain("http://something.com/wow")
        self.assertEqual(tester,"something.com")

    def test_httpsWWW(self):
        tester = self.spider.extractDomain("https://www.something.com/wow/wee")
        self.assertEqual(tester,"something.com")

    def test_httpWWW(self):
        tester = self.spider.extractDomain("http://www.something.com/wow/woo")
        self.assertEqual(tester,"something.com")

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

if __name__ == '__main__':
    unittest.main()  