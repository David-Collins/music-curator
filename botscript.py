import tweepy
import praw
import os
import time

CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_KEY = os.environ['TWITTER_OAUTH_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']
REDDIT_CONSUMER_KEY = os.environ['REDDIT_PERSONAL']
REDDIT_CONSUMER_SECRET = os.environ['REDDIT_SECRET']
user = os.environ['REDDIT_USER']
password = os.environ['REDDIT_PASS']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
reddit_access = praw.Reddit(client_id = REDDIT_CONSUMER_KEY, client_secret = REDDIT_CONSUMER_SECRET, user_agent = 'DC-EDM', un = user, pw = password)

sub = reddit_access.subreddit('trap')

f = open("LinkLog.txt", "a")

for submission in sub.top('hour'):
    if "soundcloud.com" in submission.url:
        if submission.url not in open("LinkLog.txt").read() :
            msg = submission.title + "\n" + submission.url
            f.write(submission.url + "\n")
            break

f.close()

try:
    api.update_status(msg)
except tweepy.TweepError as error:
    if error.api_code == 187:
        # Do something special
        msg  = "this bot tried to tweet the same thing too quickly" + str(random.randint(1,100001))
        api.update_status(msg)
        print('yikes')
    else:
        raise error
