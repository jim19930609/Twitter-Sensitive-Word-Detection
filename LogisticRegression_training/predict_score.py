import numpy as np
import pandas as pd
import re, string
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem.lancaster import LancasterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','–','’','"','”','“','=','…','/','>','<',"'",'-','..','...','•','★']
english_stopwords = stopwords.words('english')
pattern=re.compile(r'http\S+')

hb=pd.read_csv('hb.csv',encoding="ISO-8859-1")
ob=pd.read_csv('ob.csv',encoding="ISO-8859-1")

train_hb, test_hb = train_test_split(hb, test_size=0.2)#split into train&test set ratio:0.2
train_ob, test_ob = train_test_split(ob, test_size=0.2)#split into train&test set ratio:0.2

#fix index
train_hb["index"] = range(len(train_hb))
train_hb = train_hb.set_index(["index"])
test_hb["index"] = range(len(test_hb))
test_hb = test_hb.set_index(["index"])
train_ob["index"] = range(len(train_ob))
train_ob = train_ob.set_index(["index"])
test_ob["index"] = range(len(test_ob))
test_ob = test_ob.set_index(["index"])

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf1 = TfidfVectorizer(lowercase=False)
tfidf_train_hb = tfidf1.fit_transform(train_hb['tweet'])
tfidf_test_hb=tfidf1.transform(test_hb['tweet'])

tfidf2 = TfidfVectorizer(lowercase=False)
tfidf_train_ob = tfidf2.fit_transform(train_ob['tweet'])
tfidf_test_ob=tfidf2.transform(test_ob['tweet'])

tfidf_train_hb,tfidf_test_hb

tfidf_train_ob,tfidf_test_ob

def pr(y_i, y):
    p = x[y==y_i].sum(0)
    return (p+1) / ((y==y_i).sum()+1)

x=tfidf_train_ob

def get_mdl(y):
    y = y.values
    r = np.log(pr(1,y) / pr(0,y))
    m = LogisticRegression(C=4, dual=True)
    x_nb = x.multiply(r)
    return m.fit(x_nb, y), r

m_ob,r_ob = get_mdl(train_ob['class'])

x=tfidf_train_hb
m_hb,r_hb = get_mdl(train_hb['class'])

test_x_ob=tfidf_test_ob
test_x_hb=tfidf_test_hb

preds_ob = np.zeros((len(test_ob['tweet']), 1))
preds_ob[:,0] = m_ob.predict_proba(test_x_ob.multiply(r_ob))[:,1]
preds_hb = np.zeros((len(test_hb['tweet']), 1))
preds_hb[:,0] = m_hb.predict_proba(test_x_hb.multiply(r_hb))[:,1]

for i in range(len(preds_ob)):
    if preds_ob[i] >=0.5:
        preds_ob[i]=1
    else:
        preds_ob[i]=0
for i in range(len(preds_hb)):
    if preds_hb[i] >=0.5:
        preds_hb[i]=1
    else:
        preds_hb[i]=0

error=0
for i in range(len(preds_ob)):
    if preds_ob[i]!= test_ob['class'][i]:
        error=error+1
accuracy_ob= error/len(preds_ob)
print('The accuracy of offensive language',accuracy_ob)
error=0
for i in range(len(preds_hb)):
    if preds_hb[i]!= test_hb['class'][i]:
        error=error+1
accuracy_hb= error/len(preds_hb)
print('The accuracy of hateful language',accuracy_hb)

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











