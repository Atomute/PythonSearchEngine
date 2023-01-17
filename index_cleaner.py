import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet 
from nltk.tokenize import word_tokenize

class Cleaning:
    def __init__(self,doc):
        self.contents=doc
        self.content=''
        for word in self.contents:
            self.content += word
        #print(self.content)
    def Normalize(self):
        return self.content.lower()

    def Remove_uni(self):

        self.content = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", self.Normalize())
        return self.content 

    def Remove_stopw(self):
        stop=stopwords.words('english')
        remove_stop=self.content=" "" ".join([word for word in word_tokenize(self.Remove_uni()) if word not in (stop)])
        return remove_stop
        
    def Lemma(self):
        lemmatizer = WordNetLemmatizer()
        dum=[]
        list_of_word=word_tokenize(self.Remove_stopw())
        list_of_word.sort()
        for word in list_of_word:
            if word[-2:]=='ed' or word[-3:]=='ing':
                dum.append(lemmatizer.lemmatize(word,'v'))
            else:
                dum.append(lemmatizer.lemmatize(word))
        return dum