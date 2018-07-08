import tweepy
import random
import os

CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

msg = str(random.randint(1,100001)) + " yuh"

try:
    api.update_status(msg)
except tweepy.TweepError as error:
    if error.api_code == 187:
        # Do something special
        print('duplicate message')
    else:
       raise error
