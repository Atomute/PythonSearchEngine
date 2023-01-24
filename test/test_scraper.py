import unittest
from unittest.mock import MagicMock,patch
import sys
sys.path.insert(1,"./")
from spider_scrapper import scraper

class test_get_title(unittest.TestCase):
    def setUp(self) -> None:
        self.test_scraper = scraper()

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
        self.test_scraper = scraper()

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

class test_pushtoDB(unittest.TestCase):
    def setUp(self):
        self.test_scraper = scraper()
    
    @patch()
    def normalTest(self):
        tester = self.test_scraper.pushtoDB()

    def wrongtableTest():
        pass

    def wrongValueTest():
        pass

if __name__ == '__main__':
    unittest.main()  