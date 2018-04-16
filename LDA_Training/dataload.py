import random
import os
import numpy as np
import re

def find_swear_sentence(text_raw, num_dirty):
  sensitive_set = set()
  for filename in os.listdir("sensitive_words"):
    with open("sensitive_words/" + filename, "rb") as f:
      for line in f:
        line = line.strip().decode('ascii', 'ignore')
        sensitive_set.add(line)
  
  def clean_word(word):
    word_lowercase = word.lower()
    rule = re.compile(r"[^a-zA-Z0-9]")
    new_word = rule.sub('', word_lowercase)
    return new_word

  def finding(x, num_dirty):
    word_list = x.split(" ")
    count = 0
    for i in range(len(word_list)):
      word_clean = clean_word(word_list[i])
      if word_clean in sensitive_set:
        count += 1

    if count >= num_dirty:
      return True
    else:
      return False
  
  swear_tweet = []
  for sentence in text_raw:
    if finding(sentence, num_dirty):
      swear_tweet.append(sentence)

  swear_tweet = np.array(swear_tweet)

  return swear_tweet

  
def insert_swear_words(text_raw, num_dirty):
  sensitive_set = []
  for filename in os.listdir("sensitive_words"):
    with open("sensitive_words/" + filename, "rb") as f:
      for line in f:
        line = line.strip().decode('ascii', 'ignore').encode('utf-8', 'ignore')
        sensitive_set.append(line)
  sensitive_set = np.array(sensitive_set)

  swear_append = []
  for i in range(text_raw.shape[0]):
    rand_swear = np.random.choice(sensitive_set.shape[0], num_dirty)
    sentence_swear = " ".join(sensitive_set[rand_swear])
    text_raw[i] += " " + sentence_swear

  return text_raw

def generate_real_tweet(num_train, path):
  def Remove_Symbols(name):
    rule = re.compile(r"[^a-zA-Z0-9 ]")
    new_name = rule.sub('', name)
    new_name = new_name.lower()
    
    return new_name

  text_raw = []
  with open(path, "rb") as f:
    for lines in f:
      try:
        line = lines.strip().decode('ascii')
      except:
        continue
      line = line.split(',')[5:]
      line = " ".join(line)
      line = Remove_Symbols(line)    
      text_raw.append(line)
    print ( len(text_raw) )

  # Random Sampling
  text_raw = random.sample(text_raw, num_train)
  text_raw = np.array(text_raw)
  
  return text_raw

def generate_training(num_train, num_add, path):
  text_raw = generate_real_tweet(num_train, path)
  
  # Add Dirty Sentence
  if num_add != 0:
    dirty_sent = []
    with open("database/dirty_sentence.txt", "rb") as f:
      for line in f:
        line = line.strip()
        try:
          line = lines.decode('ascii')
        except:
          continue
        dirty_sent.append(line)

    rand_sam = random.sample(dirty_sent, num_add)
    rand_sam = np.array(rand_sam)
    text_raw = np.append(text_raw, rand_sam)
  return text_raw

if __name__ == "__main__":
  path = "database/lda_training.csv"
  text_raw = generate_real_tweet(1600000, path)
  num_dirty = 2
  
  swear_sentence = find_swear_sentence(text_raw, num_dirty)
  #swear_sentence = insert_swear_words(swear_sentence, 2)

  with open("database/dirty_sentence.txt", "a") as f:
    for sentence in swear_sentence:
      f.write(sentence + "\n")
    


