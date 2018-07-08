import tweepy
import random
import os

print(os.environ)
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_KEY = os.environ['TWITTER_OAUTH_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

msg = str(random.randint(1,100001)) + " yuh"

try:
    api.update_status(msg)
except tweepy.TweepError as error:
    if error.api_code == 187:
        # Do something special
        msg  = "this bot is stupid and tried to tweet the same thing too quickly" + str(random.randint(1,100001))
        api.update_status(msg)
        print('duplicate message')
    else:
       raise error
