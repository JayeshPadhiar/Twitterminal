import tweepy
from pprint import pprint

class Engine:

    def __init__(self, keys):

        self.keys = dict(keys)


        pprint(self.keys)
        

        self.auth = tweepy.OAuthHandler(self.keys['apiKey'], self.keys['apiSecret'])
        self.auth.set_access_token(self.keys['token'], self.keys['tokenSecret'])

        self.engine = tweepy.API(self.auth)