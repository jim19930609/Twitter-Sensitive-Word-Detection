import numpy as np
import pandas as pd
import re, string
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem.lancaster import LancasterStemmer
import nltk


rawdata=pd.read_csv('labeled_data .csv')
data=rawdata[['class','tweet']]

hb=data.loc[data['class'].isin([0,2])] #hb means hate and benigh
ob=data.loc[data['class'].isin([1,2])] #ob means offensive and benigh
#give new labels to two data set
hb['class'] = hb['class'].replace(0, 1)
hb['class'] = hb['class'].replace(2, 0)
ob['class'] = ob['class'].replace(2, 0)

#fix index
hb["index"] = range(len(hb))
hb = hb.set_index(["index"])
ob["index"] = range(len(ob))
ob = ob.set_index(["index"])
#train_hb.head()
#lens = train_hb.tweet.str.len()
#lens.mean(), lens.std(), lens.max()

english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','–','’','"','”','“','=','…','/','>','<',"'",'-','..','...','•','★']
english_stopwords = stopwords.words('english')
pattern=re.compile(r'http\S+')

pre-processing the data
comment=[document.lower() for document in comment]
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','–','’','"','”','“']
comment=[w for w in comment if not w in english_punctuations]
english_stopwords = stopwords.words('english')
comment=[w for w in comment if not w in english_stopwords]
pattern=re.compile(r'http\S+')
comment=[w for w in comment if not w in pattern.findall(w)]

for i in range(len(hb['tweet'])):
    tknzr = TweetTokenizer(strip_handles=True,reduce_len=True)
    hb['tweet'][i]= tknzr.tokenize(hb['tweet'][i])
    hb['tweet'][i]=[document.lower() for document in hb['tweet'][i]]
    hb['tweet'][i]=[w for w in hb['tweet'][i] if not w in english_punctuations]
    hb['tweet'][i]=[w for w in hb['tweet'][i] if not w in english_stopwords]
    hb['tweet'][i]=[w for w in hb['tweet'][i] if not w in pattern.findall(w)]

for i in range(len(ob['tweet'])):
    tknzr = TweetTokenizer(strip_handles=True,reduce_len=True)
    ob['tweet'][i]= tknzr.tokenize(ob['tweet'][i])
    ob['tweet'][i]=[document.lower() for document in ob['tweet'][i]]
    ob['tweet'][i]=[w for w in ob['tweet'][i] if not w in english_punctuations]
    ob['tweet'][i]=[w for w in ob['tweet'][i] if not w in english_stopwords]
    ob['tweet'][i]=[w for w in ob['tweet'][i] if not w in pattern.findall(w)]

ob.to_csv('ob.csv', index = False)
hb.to_csv('hb.csv', index = False)




