import unittest
from unittest.mock import MagicMock,patch
import sys
sys.path.insert(1,"./")
from spider.spider_updater import updater

class test_update(unittest.TestCase):
    def setUp(self):
        self.updater = updater()
    
    def test_normal(self):
        tester = self.updater.update()

class test_get_webToupdate(unittest.TestCase):
    def setUp(self):
        self.updater = updater()

    def test_normal(self):
        tester = self.updater.get_webToupdate()
        self.assertIsInstance(tester,list)

class test_update_backlinks(unittest.TestCase):
    def setUp(self):
        self.updater = updater()

    def test_normal(self):
        tester = self.updater.update_backlinks([])

if __name__ == '__main__':
    unittest.main()  
