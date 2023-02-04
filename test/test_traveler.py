import unittest
from unittest.mock import patch
import sys
sys.path.insert(1,"./")
from spider.spider_webTraveler import webTraveler

class test_find_links(unittest.TestCase):
    def setUp(self):
        self.traveler = webTraveler()

    @patch('spider_webTraveler.webTraveler.download_url')
    def test_normal(self,mock_download_url):
        mock_download_url.return_value = "something"
        tester = self.traveler.find_links("url")

        self.assertIsInstance(tester,list)

    @patch('spider_webTraveler.webTraveler.download_url')
    def test_one_link(self,mock_download_url):
        mock_download_url.return_value = "<html> <body> <a href='https://www.something.com/firstpage'>something</a> </body> </html>"
        tester = self.traveler.find_links("https://www.something.com/")

        self.assertEqual(tester,['https://www.something.com/firstpage'])

    @patch('spider_webTraveler.webTraveler.download_url')
    def test_multiple_link(self, mock_download_url):
        mock_download_url.return_value = "<html> <body> <a href='https://www.something.com/firstpage'>something</a> <a href='https://www.something.com/secondpage'>something</a> </body> </html>"
        tester = self.traveler.find_links("https://www.something.com/")

        self.assertEqual(tester,['https://www.something.com/firstpage','https://www.something.com/secondpage'])

    @patch('spider_webTraveler.webTraveler.download_url')
    def test_numbersign(self,mock_download_url):
        mock_download_url.return_value = "<a href='#numbersign'>something</a>"
        tester = self.traveler.find_links("url")

        self.assertEqual(tester,[])

    @patch('spider_webTraveler.webTraveler.download_url')
    def test_notinroot(self,mock_download_url):
        self.traveler.rooturl = "https://www.root.com/"
        mock_download_url.return_value = "<a href='https://www.something.com/'>something</a>"
        tester = self.traveler.find_links("url")

        self.assertEqual(tester,[])

    @patch('spider_webTraveler.webTraveler.download_url')
    def test_no_link(self,mock_download_url):
        mock_download_url.return_value = "no link here"
        tester = self.traveler.find_links("url")

        self.assertEqual(tester,[])

class test_download_url(unittest.TestCase):
    def setUp(self):
        self.traveler = webTraveler()
    
    @patch('spider_webTraveler.requests')
    def test_normal(self,mock_requests):
        # test that download_url called with correct parameter
        self.traveler.download_url("url")
        mock_requests.get.assert_called_with("url")

class test_exLink(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_normal(self):
        pass

    

if __name__ == '__main__':
    unittest.main()  