import os
import time
import json
import tweepy
import dateutil.parser
from tweepy.streaming import StreamListener
from tweepy import Stream

class MyListener(StreamListener):
    # Overide of tweepy's StreamListener Class, detailed process of received Json message from Twitter is defined in on_data()
    def __init__(self):
        self.number = 0

    def on_data(self, data):
        # Receive Twitter Message -> Parse Message -> Write Message to File
        try:
            # Controls Receiving Rate
            time.sleep(3)
            with open('data/python' + str(self.number) + '.txt', 'a') as f:
                self.number += 1
                parsed_dict = parse_tweet(data)
                if parsed_dict is not None:
                  print "Received Twitter Message"
                  text = str(parsed_dict['user_id']) + '|' + parsed_dict['text']
                  f.write(text)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 

def parse_tweet(tweet_in, encoding  = 'utf-8'):
    # Extract Effective Information from Twitter Message (In json form) by key
    parsed_dict = {}
    tweet_in = json.loads(tweet_in)
    if tweet_in and 'delete' not in tweet_in:
        parsed_dict['id']           = tweet_in['id']
        parsed_dict['geo']          = tweet_in['geo']['coordinates'] if tweet_in['geo'] else None
        parsed_dict['text']         = tweet_in['text'].encode(encoding)
        parsed_dict['user_id']      = tweet_in['user']['id'] 
        parsed_dict['hashtags']     = [x['text'].encode(encoding) for x in tweet_in['entities']['hashtags']]
        parsed_dict['timestamp']    = dateutil.parser.parse(tweet_in[u'created_at']).replace(tzinfo=None).isoformat()
        parsed_dict['screen_name']  = tweet_in['user']['screen_name'].encode(encoding)
    else:
        parsed_dict = None

    return parsed_dict


def connect_twitter():
    # This is my(Zhanlue Yang) personal key and token, should be replace by your own app's key and token
    consumer_key = 'lKQbO2qAfcyLT0pyLTLW0Iu1I'
    consumer_secret = 'oUO6jCmyNkl2laYMJRhYQKpyNpcfvbV1VXbRbyZKbKtazSrHDQ'
    access_token = '983503290934677504-WdU9iViN1Ht9fLEQdTVQP87nfgMSRvE'
    access_secret = '6S5k0JznN6Si5aQPgGhCm9BWrRrnUNrVfDffvZdTtmybQ'
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    return tweepy.Stream(auth=auth, listener=MyListener())

if __name__ == "__main__":
  # Create Twitter Session
	twitter_stream = connect_twitter()

  # Filtering of Received Message
	twitter_stream.filter(track=['trump'])
	

