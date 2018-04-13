import numpy as np
import os
import re
import nltk
import lda
from nltk.corpus import stopwords
from nltk import word_tokenize
from gensim import corpora, models

def Remove_Symbols(name):
  rule = re.compile(r"[^a-zA-Z0-9 ]")
  new_name = rule.sub('', name)
  
  return new_name

  
def ReadArticle(path, num_train):
  text = []
  with open(path, "rb") as f:
    index = 0
    for lines in f:
      line = lines.strip().decode('ascii', 'ignore').encode('utf-8', 'ignore')
      line = line.split(',')[5:]
      line = " ".join(line)
      line = Remove_Symbols(line)
      
      index += 1
      if index > num_train:
        break
      
      text.append(line)
  return text   

def collect_topics(lda_model):
  f = open("topics.txt", "a")
  for topics in lda_model.print_topics(num_topics):
    star_sp = topics[1].split("*")
    for i in range(1, len(star_sp)):
      tp_word = star_sp[i].split("\"")[1]
      f.write(tp_word + " ")
    f.write("\n")

  f.close()

if __name__ == "__main__":
  num_train = 10000
  num_topics = 20
  text_raw = ReadArticle("database/lda_training.csv", num_train)
  print "Total Number of ", len(text_raw), " Training Data Loaded"

  # Load stop words
  words_stop = stopwords.words('english')
  
  text_split = []
  for i in range(len(text_raw)):
    word_nonstop = []
    for word in word_tokenize(text_raw[i]):
      if word not in words_stop:
        if len(word) <= 3:
          continue
        
        word_nonstop.append(word)
    
    if len(word_nonstop) > 0:
      text_split.append(word_nonstop)

  # Word Dictionary
  dic = corpora.Dictionary(text_split)

  # Generate Corpus
  corpus = [dic.doc2bow(text) for text in text_split]

  # LDA Model
  model_path = "lda_model/model"
  if not os.path.exists(model_path):
    print "Training LDA Model From Original"
    lda_model = models.ldamodel.LdaModel(corpus, id2word=dic, num_topics=num_topics)
    lda_model.save("lda_model/model")
  else:
    print "Load Existing LDA Model"
    lda_model = models.ldamodel.LdaModel.load("lda_model/model")

  # Make Predictions: 
  newdoc_count = corpus[0]
  doc_lda = lda_model[newdoc_count]
  
  collect_topics(lda_model)

