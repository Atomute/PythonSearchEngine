import unittest
from unittest.mock import MagicMock,patch
import sys
sys.path.insert(1,"./")
from spider.spider import spider

class test_get_title(unittest.TestCase):
    def setUp(self) -> None:
        self.test_scraper = spider()

    def test_normal(self):
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

class test_get_exlink(unittest.TestCase):
    def setUp(self):
        self.spider = spider()

    def test_normal(self):
        tester = self.spider.get_links("url")

        self.assertIsInstance(tester,list)

    def test_one_link(self):
        self.spider.currentURL = "https://www.something.com/"
        tester = self.spider.get_links("<html> <body> <a href='https://www.something.com/firstpage'>something</a> </body> </html>")

        self.assertEqual(tester,['https://www.something.com/firstpage'])

    def test_multiple_link(self):
        self.spider.currentURL = "https://www.something.com/"
        tester = self.spider.get_links("<html> <body> <a href='https://www.something.com/firstpage'>something</a> <a href='https://www.something.com/secondpage'>something</a> </body> </html>")

        self.assertEqual(tester,['https://www.something.com/firstpage','https://www.something.com/secondpage'])

    def test_numbersign(self):
        self.spider.currentURL = "https://www.something.com/"
        tester = self.spider.get_links("<a href='#numbersign'>something</a>")

        self.assertEqual(tester,[])

    def test_notinroot(self):
        self.spider.root = "https://www.root.com/"
        self.spider.currentURL = "https://www.root.com/test"
        tester = self.spider.get_links("<a href='https://www.something.com/'>something</a>")

        self.assertEqual(tester,[])

    def test_no_link(self):
        self.spider.currentURL = "https://www.something.com/"
        tester = self.spider.get_links("no link here")

        self.assertEqual(tester,[])

    def test_exlinks(self):
        self.spider.root = "https://www.root.com/"
        self.spider.currentURL = "https://www.root.com/test"
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

class test_cleanURL(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = spider()

    def test_normal(self):
        tester = self.spider.cleanURL("https://something.com")
        self.assertIsInstance(tester,str)

    def test_https(self):
        tester = self.spider.cleanURL("https://something.com/wow")
        self.assertEqual(tester,"https://something.com")

    def test_http(self):
        tester = self.spider.cleanURL("http://something.com/wow")
        self.assertEqual(tester,"http://something.com")

    def test_httpsWWW(self):
        tester = self.spider.cleanURL("https://www.something.com/wow/wee")
        self.assertEqual(tester,"https://something.com")

    def test_httpWWW(self):
        tester = self.spider.cleanURL("http://www.something.com/wow/woo")
        self.assertEqual(tester,"http://something.com")

# class test_pushtoDB(unittest.TestCase):
#     def setUp(self):
#         self.test_scraper = scraper()
    
#     def normalTest(self):
#         tester = self.test_scraper.pushtoDB()

#     def wrongtableTest():
#         pass

#     def wrongValueTest():
#         pass

if __name__ == '__main__':
    unittest.main()  