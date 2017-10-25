from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import simplejson as json
import time
from datetime import datetime
from dateutil import tz
from dateutil.tz import tzlocal

from configparser import ConfigParser

from twitteres.ElasticSearchWrapper import ElasticSearchWrapper

class MyStreamListener(StreamListener):
    def __init__(self, tweet_handle):
        StreamListener.__init__(self)
        self.tweet_handle = tweet_handle

    def on_status(self, status):
        try:     
            if status.coordinates is not None:         
                coords = status.coordinates["coordinates"]	
                tweet = {
	                'name': status.author.screen_name,
                    'text': status.text,
                    'time': status.created_at.strftime("%Y-%m-%d %H:%M:%S"),
	                'location': {'lat': coords[1], 'lon': coords[0]},                   
                    'profile_image_url': status.author.profile_image_url
	            }
                #print(status.created_at.strftime("%Y-%m-%d %H:%M:%S"))
                self.tweet_handle.add_tweet(tweet)
                return True

        except BaseException as e:
            print("Error on_status: %s" % str(e))

class TweetStream():
    def __init__(self):
        self.stream = None
        self.tweet_handle = None

    def set_handle(self, tweet_handle):
        self.tweet_handle = tweet_handle

    def start_stream(self):
        config = ConfigParser()
        config.read("twitteres/config.cfg")

        consumer_key = config['twitter']['twitter_consumer_key']
        consumer_secret = config.get('twitter', 'twitter_consumer_secret')
        access_token = config.get('twitter','twitter_access_token')
        access_token_secret = config.get('twitter','twitter_access_token_secret')

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.stream = Stream(auth, MyStreamListener(self.tweet_handle))

        while True:
            try:
                self.stream.filter(locations=[-180,-90,180,90])
            except:
                continue

    def stop_stream(self):
        self.stream.disconnect()

class MyTwitterHandler():
    def __init__(self,elasticsearch):
        self.tweet_list = []
        self.es = elasticsearch
        self.id = self.es.count()
    
    def add_tweet(self,tweet):
        self.id += 1
        response = self.es.upload(tweet,self.id)


        

    

