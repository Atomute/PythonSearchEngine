import unittest
from unittest.mock import MagicMock, patch
import sys
sys.path.insert(1,"./")
from indexer.index_inverter import InvertedIndex
import sqlite3
import unittest

class testGetWords(unittest.TestCase):
    def setUp(self):
        self.index = InvertedIndex()

    def test_normal(self):
        title = "Hello World"
        content = "This is a sample content."
        tester = self.index.get_words(title,content)
        self.assertIsInstance(tester,list)

    def test_get_words_with_title(self):
        # Arrange
        title = "Hello World."
        content = "This is a sample content."
        result = self.index.get_words(title, content)
        self.assertEqual(result, ['hello', 'world', 'content', 'sample'])

    def test_get_words_without_title(self):
        # Arrange
        title = None
        content = "This is a sample content."
        result = self.index.get_words(title, content)
        self.assertEqual(result, ["content", "sample"])

    def test_get_words_without_content(self):
        # Arrange
        title = "Hello World !, This is me"
        content = None
        result = self.index.get_words(title, content)
        self.assertEqual(result, ["hello", "world"])

    def test_get_words_without_title_and_content(self):
        title = None
        content = None
        result = self.index.get_words(title, content)
        self.assertEqual(result, [])

class test_get_word_freq(unittest.TestCase):
    def setUp(self):
        self.index = InvertedIndex()

    def test_normal(self):
        doc = ['hello', 'world', 'content', 'sample']
        tester = self.index.get_word_freq(doc)
        self.assertIsInstance(tester,dict)

    def test_get_words_freq_nondupe(self):
        doc =['hello', 'world', 'content', 'sample']
        result = self.index.get_word_freq(doc)
        self.assertDictEqual(result, {'hello':1, 'world':1, 'content':1, 'sample':1})

    def test_get_words_freq_dupe(self):
        words = ['apple', 'banana', 'cherry', 'banana', 'apple', 'apple']
        expected_result = {'apple': 3, 'banana': 2, 'cherry': 1}
        result = self.index.get_word_freq(words)
        self.assertDictEqual(result, expected_result)

    def test_get_words_freq_none(self):
        words = []
        result = self.index.get_word_freq(words)
        self.assertDictEqual(result,{})

if __name__ == '__main__':
    unittest.main()