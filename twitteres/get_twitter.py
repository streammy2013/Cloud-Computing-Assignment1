import tweepy
import os
import sys
import jsonpickle
from django.http import HttpResponse
from twitter import TweetStreamer
from twitter import TweetHandler

consumer_key = 'SpNnlmp2iFG9C5Tn3O5LcQlNk'
consumer_secret = 'qdmSAK3Qv30fd5OeJzyMFiJurppE88f5kSmPyefeTFuj8isYM0'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)


auth.set_access_token('858519101328605184-MeeGoebZpQun2DelnYfZdnhZGp7TM1x', 'RE965hFV2v02GJ8hnTRZNskgmUOCk1eQyHO3XFcI0iHNV')

#Switching to application authentication
#auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

#Setting up new api wrapper, using authentication only
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

api = tweepy.API(auth)

maxtweets = 200
index = 0
with open('past_twitter.json', 'w') as f:


	for tweet in tweepy.Cursor(api.home_timeline).items(maxtweets):
	    # Process a single status
	    if tweet.coordinates is not None:
		    f.write(jsonpickle.encode(tweet._json, unpicklable = False)+ '\n')
		    index += 1
			#print (tweet.coordinates)
            #lon = tweet.coordinates[0]
            #lat = tweet.coordinates[1]

print ("Downloaded {0} tweets".format(index))

