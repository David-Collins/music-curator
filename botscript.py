import tweepy
import time
import random

CONSUMER_KEY = '2PyQIHvWYtz6PpBxLRL7WH4zX'
CONSUMER_SECRET = 'v0y04fv6shyYF6E45M5CAf41NQwRa0Lad4rDo51c1dQgaaQVdI'
ACCESS_KEY = '1012414359891599361-L2bkcMnM0GM0JXspjXKVYRhjm1nSUc'
ACCESS_SECRET = 'X72w9TEY72oWJqqtNHbYAFnh4uVBE8LP4ekqIW1a9zl0U'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

msg = str(random.randint(1,100001))

while True:
    api.update_status(msg)
    time.sleep(300)
