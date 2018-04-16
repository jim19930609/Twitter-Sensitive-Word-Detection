import shutil
import argparse
import re
import os
import time
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from gensim import corpora, models
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext

# External Input Flags
parser = argparse.ArgumentParser()
parser.add_argument('--interval', type=int, default=1,
                    help='Spark Streaming Interval in seconds')
parser.add_argument('--windslide', type=int, default=1,
                    help='Interval of Window Slide')
parser.add_argument('--windsize', type=int, default=1,
                    help='Window Size')
args = parser.parse_args()

def Output_Function(rdd):
  def Write2File(content):
    with open("result/" + str(int(time.time())) + ".txt", "a") as f:
      f.write(content)

  rdd.foreach(Write2File)
  
def Keywords_Filtering(stream):
  '''
  Split sentences into words, Then replace sensitive words with ***** according to the dictionary
  
  sensitive_set: A set that stores all sensitive words
  clean_word(): Transfer word into all lower case letters, and remove all weird symbols (like: &*%$#@!()?....)
  filtering(): Main function to perform sentence filtering
  '''
  # Load Sensitive Words From File
  sensitive_set = set()
  for filename in os.listdir("sensitive_words"):
    with open("sensitive_words/" + filename, "rb") as f:
      for line in f:
        line = line.strip().decode('utf-8')
        sensitive_set.add(line)

  def clean_word(word):
    word_lowercase = word.lower()
    rule = re.compile(r"[^a-zA-Z0-9]")
    new_word = rule.sub('', word_lowercase)
    return new_word

  def filtering(x):
    word_list = x.split(" ")
    keywords_list = []
    for i in range(len(word_list)):
      word_clean = clean_word(word_list[i])
      if word_clean in sensitive_set:
        word_list[i] = "*****"
        keywords_list.append(word_clean)

    message_recovered = " ".join(word_list)
    if len(keywords_list) != 0:
      message_recovered += "|||" + "|||".join(keywords_list)
    else:
      message_recovered += "|||None"
    return message_recovered
  
  # Perform filtering for each RDD in a Dstream window
  m = stream.map(filtering)
  return m


def TopicModel_Filtering(stream):
  def clean_word(word):
    word_lowercase = word.lower()
    rule = re.compile(r"[^a-zA-Z0-9]")
    new_word = rule.sub('', word_lowercase)
    return new_word
  
  tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
  words_stop = stopwords.words('english')
  stop_set = set()
  
  for i in range(len(words_stop)):
    stop_set.add(clean_word(words_stop[i]))

  def LDAFiltering(x):
    # Load stop words, then remove first number(ID)
    x = x.strip()
    x = x[x.find("RT ") + 1:]

    text_split = []
    for word in tknzr.tokenize(x):
      if word not in stop_set:
        if len(word) <= 3:
          continue
          
        text_split.append(clean_word(word))
    text_split = [text_split]

    # Word Dictionary
    dic = corpora.Dictionary(text_split)

    # Generate Corpus
    corpus = [dic.doc2bow(text) for text in text_split]
    
    # Load LDA Model
    lda_model = models.ldamodel.LdaModel.load("lda_model/model")

    # Make Predictions: 
    tmp = corpus[0]
    prediction = lda_model[tmp]

    max_p = -1
    max_topic = -1
    for topics in prediction:
      p = float(topics[1])
      if p >= max_p:
        max_p = p
        max_topic = topics[0]
    
    return x + "|||" + str(max_topic)
  
  m = stream.map(LDAFiltering)
  
  return m


def Streaming_main(root):
    # Pyspark Streaming Settings
    conf = SparkConf().setAppName("origin").setMaster("local")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("OFF")
    ssc = StreamingContext(sc, args.interval)

    # Streaming Interface
    messages = ssc.textFileStream(root)
    messages_window = messages.window(args.windsize, args.windslide)
    
    # Filtering
    messages_TPFilt = TopicModel_Filtering(messages_window)
    messages_KWFilt = Keywords_Filtering(messages_TPFilt)

    # Output
    messages_KWFilt.foreachRDD(Output_Function)
    messages_KWFilt.pprint()
    
    return ssc


if __name__ == "__main__":
  # Irrelevent Parameters Setting
  check_point = "check_point"
  root = "data"
  try:
    shutil.rmtree(check_point)
  except:
    pass

  # Major Entrance of streaming definations
  ssc = StreamingContext.getOrCreate(check_point, lambda: Streaming_main(root))

  # Start Streaming
  ssc.start()
  ssc.awaitTermination()
