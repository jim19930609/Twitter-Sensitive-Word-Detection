import numpy as np
import pandas as pd
import re, string
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem.lancaster import LancasterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

f = open('my_pred.pickle', 'rb')
m_ob = pickle.load(f)
r_ob = pickle.load(f)
m_hb = pickle.load(f)
r_hb = pickle.load(f)
tfidf1 = pickle.load(f)
tfidf2 = pickle.load(f)
f.close()

english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','–','’','"','”','“','=','…','/','>','<',"'",'-','..','...','•','★']
english_stopwords = stopwords.words('english')
pattern=re.compile(r'http\S+')

def get_score(comment):
    df = pd.DataFrame([comment],columns=['tweet'])
    tknzr = TweetTokenizer(strip_handles=True,reduce_len=True)
    df['tweet'][0]= tknzr.tokenize(df['tweet'][0])
    df['tweet'][0]=[document.lower() for document in df['tweet'][0]]
    df['tweet'][0]=[w for w in df['tweet'][0] if not w in english_punctuations]
    df['tweet'][0]=[w for w in df['tweet'][0] if not w in english_stopwords]
    df['tweet'][0]=[w for w in df['tweet'][0] if not w in pattern.findall(w)]
    df['tweet'][0]=str(df['tweet'][0])
    tfidf_test_hb=tfidf1.transform(df['tweet'])
    tfidf_test_ob=tfidf2.transform(df['tweet'])
    preds1 = m_hb.predict_proba(tfidf_test_hb.multiply(r_hb))[:,1]
    preds2 = m_ob.predict_proba(tfidf_test_ob.multiply(r_ob))[:,1]
    return preds1, preds2


comment="from now on, I will only go on dates with girls who show me their transcripts first"
# input("new tweet?")

hate_score,offensive_score=get_score(comment)
print(hate_score,offensive_score)