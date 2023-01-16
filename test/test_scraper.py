import unittest
import sys
sys.path.insert(1,"/work/PythonSearchEngine/")
from spider_scrapper import scraper

class test_get_title(unittest.TestCase):
    def test_normal(self):
        self.testSpider = scraper("https://www.blank.org/")
        self.assertEqual(self.testSpider.get_title("<title>This is title</title>"),"This is title")

    def test_notitle(self):
        self.testSpider = scraper("https://www.blank.org/")
        self.assertEqual(self.testSpider.get_title(""),None)

class test_get_p(unittest.TestCase):
    def test_normal(self):
        self.testSpider = scraper("https://www.blank.org/")
        self.assertEqual(self.testSpider.get_p("<p>This is p</p>"),["This is p"])

    def test_nop(self):
        self.testSpider = scraper("https://www.blank.org/")
        self.assertEqual(self.testSpider.get_p(""),[])

# class test_pushtoDB(unittest.TestCase):
#     def normalTest():
#         pass

#     def wrongtableTest():
#         pass

#     def wrongValueTest():
#         pass

if __name__ == '__main__':
    unittest.main()  