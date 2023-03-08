import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet 
from nltk.tokenize import word_tokenize
import string

class Cleaning:
    def __init__(self):
        pass
        
    def Normalize(self,doc):
        return doc.lower()

    def Remove_uni(self,doc):
        doc_no_uni = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", doc)
        return doc_no_uni

    def Remove_stopw(self,doc):
        stop=stopwords.words('english')
        remove_stop=" ".join([word for word in word_tokenize(doc) if word not in (stop) and word not in string.punctuation])
        return remove_stop
        
    def Lemma(self,doc):
        lemmatizer = WordNetLemmatizer()
        dum=[]
        list_of_word=word_tokenize(doc)
        list_of_word.sort()
        for word in list_of_word:
            dum.append(WordNetLemmatizer().lemmatize(word,'v'))

        return dum

    def process_text(self,doc):
        a=self.Normalize(doc)
        b=self.Remove_uni(a)
        c=self.Remove_stopw(b)
        d=self.Lemma(c)
        for i in d :
            if i =='youre' or i=='im'or i=='hes' or i=='shes' or i=='theyre' or i=='were':
                d.remove(i)     
        return d
# doc = "he ran over some dogs and he going to the vet"
# a=Cleaning()
# ca=a.Lemma(doc)
# print(ca)
# ca=a.cleantext("I'm fine , this is the life . You're hole!!!")
# print(ca)