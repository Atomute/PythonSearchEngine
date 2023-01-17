import unittest
import sys
sys.path.insert(1,"./")
from spider_webTraveler import webTraveler

class test_find_links(unittest.TestCase):
    def setUp(self):
        self.traveler = webTraveler()

    def test_normal(self):
        input = "<a>link1</a>    <a>link2</a>"
        tester = self.traveler.find_links(input)

        self.assertIsInstance(tester,list)

    def test_numbersign(self):
        pass

    def test_notinroot(self):
        pass

if __name__ == '__main__':
    unittest.main()  