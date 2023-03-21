import unittest
from unittest.mock import MagicMock,patch
import sys
sys.path.insert(1,"./")
from indexer.index_cleaner import Cleaning

class test_remove_Uni(unittest.TestCase):
    def setUp(self):
        self.cleaner = Cleaning()

    def test_normal(self):
        doc = "This is a sample content."
        tester = self.cleaner.Remove_uni(doc)
        self.assertIsInstance(tester,str)

    def test_normalSentence(self):
        doc = "This is a sample content."
        tester = self.cleaner.Remove_uni(doc)
        self.assertEqual(tester,"This is a sample content")

    def test_noText(self):
        doc = "."
        tester = self.cleaner.Remove_uni(doc)
        self.assertEqual(tester,"")

    def test_number(self):
        doc = "10"
        tester = self.cleaner.Remove_uni(doc)
        self.assertEqual(tester,"10")

    def test_numberwithuni(self):
        doc = "123345???7843874%7"
        tester = self.cleaner.Remove_uni(doc)
        self.assertEqual(tester,"123345 7843874 7")

    def test_someuni(self):
        doc = "Hi?"
        tester = self.cleaner.Remove_uni(doc)
        self.assertEqual(tester,"Hi")

    def test_allUni(self):
        doc = "?<><$)(@#!"
        tester = self.cleaner.Remove_uni(doc)
        self.assertEqual(tester,"")

    def test_exact(self):
        doc = "Hello Hi 7 #$ 5"
        tester = self.cleaner.Remove_uni(doc)
        self.assertEqual(tester,"Hello Hi 7 5")

    def test_thai_word(self):
        doc = "ทิว คิว /*-+.+++*/*-ถุย"
        tester = self.cleaner.Remove_uni(doc)
        self.assertEqual(tester,"ทิว คิว ถุย")

    def test_thai_eng(self):
        doc = "ทิว -*+eat ไอติม+++++"
        tester = self.cleaner.Remove_uni(doc)
        self.assertEqual(tester,"ทิว eat ไอติม")


class test_remove_stop_word(unittest.TestCase):
    def setUp(self) :
        self.cleaner=Cleaning()

    def test_normal(self):
        doc = "something"
        tester = self.cleaner.Remove_stopw(doc)
        self.assertIsInstance(tester,str)
        
    def test_normalSentence(self):
        doc = "something went wrong"
        tester = self.cleaner.Remove_stopw(doc)
        self.assertEqual(tester,"something went wrong")

    def test_sentenceWithStopW(self):
        doc = "a wild fox run in the field"
        tester = self.cleaner.Remove_stopw(doc)
        self.assertEqual(tester,"wild fox run field")

    def test_sensitive(self):
        doc = "louis vuitton is the most popular luxury bag"
        tester = self.cleaner.Remove_stopw(doc)
        self.assertEqual(tester,"louis vuitton popular luxury bag")

    def test_empty(self):
        doc = ""
        tester = self.cleaner.Remove_stopw(doc)
        self.assertEqual(tester, "")

    def test_onlyStopWords(self):
        doc = "the and of"
        tester = self.cleaner.Remove_stopw(doc)
        self.assertEqual(tester, "")

    def test_punctuation(self):
        doc = "this is a test, with some punctuations! i hope it works."
        tester = self.cleaner.Remove_stopw(doc)
        self.assertEqual(tester, "test punctuations hope works")
        
class test_Lemma(unittest.TestCase):
    def setUp(self) :
        self.cleaner=Cleaning()

    def test_normal(self):
        doc = "something"
        tester = self.cleaner.Lemma(doc)
        self.assertIsInstance(tester,list)

    def test_normalword(self):
        doc='eat'
        tester = self.cleaner.Lemma(doc)
        self.assertEqual(tester,['eat'])

    def test_normalword(self):
        doc='stays walks eats'
        tester = self.cleaner.Lemma(doc)
        self.assertEqual(tester,['eat', 'stay', 'walk'])

    def test_sim_es_word(self):
        doc='goes misses wishes watches'
        tester = self.cleaner.Lemma(doc)
        self.assertEqual(tester,['go', 'miss', 'watch', 'wish'])

    def test_past_vocab(self):
        doc='ate'
        tester = self.cleaner.Lemma(doc)
        self.assertEqual(tester,['eat'])

    def test_future_vocab(self):
        doc='eaten'
        tester = self.cleaner.Lemma(doc)
        self.assertEqual(tester,['eat'])

    def test_gerunds(self):
        doc='hunting'
        tester = self.cleaner.Lemma(doc)
        self.assertEqual(tester,['hunt'])

    def test_noun(self):
        doc='hunter'
        tester = self.cleaner.Lemma(doc)
        self.assertEqual(tester,['hunter'])

    def test_normalSentence(self):
        doc = "he run so fast"
        tester = self.cleaner.Lemma(doc)

        self.assertEqual(tester,["fast",'he','run','so'])

    def test_noLemma(self):
        doc = "this cannot be legalize"
        tester = self.cleaner.Lemma(doc)
        self.assertEqual(tester, ['be', 'can', 'legalize', 'not', 'this'])

    def test_punctuations(self):
        doc = "test, with some runs!"
        tester = self.cleaner.Lemma(doc)
        self.assertEqual(tester, ['!', ',', 'run', 'some', 'test', 'with'])

if __name__ == "__main__":
    unittest.main()