import shutil
import re
import os
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext


def Keywords_Filtering(stream):
  '''
  Split sentences into words, Then replace sensitive words with ***** according to the dictionary
  
  sensitive_set: A set that stores all sensitive words
  clean_word(): Transfer word into all lower case letters, and remove all weird symbols (like: &*%$#@!()?....)
  filtering(): Main function to perform sentence filtering
  '''
  sensitive_set = {'trump'}

  def clean_word(word):
    word_lowercase = word.lower()
    rule = re.compile(r"[^a-zA-Z0-9]")
    new_word = rule.sub('', word_lowercase)
    return new_word

  def filtering(x):
    word_list = x.split(" ")
    for i in range(len(word_list)):
      word_clean = clean_word(word_list[i])
      if word_clean in sensitive_set:
        word_list[i] = "*****"

    message_recovered = " ".join(word_list)
    return message_recovered
  
  # Perform filtering for each RDD in a Dstream window
  m = stream.map(filtering)
  return m

def TopicModel_Filtering(stream):
  raise NotImplementedError

def Result_Visualization(stream):
  raise NotImplementedError

def Streaming_main(root):
    # Pyspark Streaming Settings
    conf = SparkConf().setAppName("origin").setMaster("local")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("OFF")
    ssc = StreamingContext(sc, 5)

    # Streaming Interface
    messages = ssc.textFileStream(root)
    messages_window = messages.window(5, 5)
    
    # Filtering
    messages_KWFilt = Keywords_Filtering(messages_window)

    # Output 
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
  shutil.rmtree(root)
  os.mkdir(root)

  # Major Entrance of streaming definations
  ssc = StreamingContext.getOrCreate(check_point, lambda: Streaming_main(root))

  # Start Streaming
  ssc.start()
  ssc.awaitTermination()
