import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet 
from nltk.tokenize import word_tokenize
from pythainlp import util
import pythainlp
from pythainlp.util import normalize
from pythainlp.corpus import thai_stopwords

class Cleaning:
    def __init__(self):
        pass
        
    def Normalize(self, doc):
        return doc.lower()

    def Remove_uni(self, doc):
        doc_no_uni = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", " ", doc)
        return doc_no_uni

    def Remove_stopw(self, doc):
        stop = set(stopwords.words('english'))
        remove_stop = " ".join([word for word in word_tokenize(doc) if word not in stop and word not in string.punctuation])
        return remove_stop

    def Remove_stopw_Th(self,doc):
        stopwords = list(thai_stopwords())
        list_word_not_stopwords = [i for i in doc if i not in stopwords]
        return list_word_not_stopwords

    def Lemma(self,doc):
        dum=[]
        list_of_word=word_tokenize(doc)
        list_of_word.sort()
        for word in list_of_word:
            dum.append(WordNetLemmatizer().lemmatize(word,'v'))

        return dum

    def process_text(self, doc):
        du=[]
        list_of_words=word_tokenize(doc)
        for word in list_of_words:
            if util.isthai(word):
                a=normalize(word)
                b=pythainlp.word_tokenize(a)
                c = self.Remove_uni(a)
                d = self.Remove_stopw_Th(b)
                du=du+d
            else :
                a = self.Normalize(word)
                b = self.Remove_uni(a)
                c = self.Remove_stopw(b)
                d = self.Lemma(c)
                for i in d:
                    if i in ['youre', 'im', 'hes', 'shes', 'theyre', 'were']:
                        d.remove(i) 

                du=du+d
        du.sort()
        return du