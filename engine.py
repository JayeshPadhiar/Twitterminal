import tweepy
from pprint import pprint

class Engine:

    def __init__(self, keys):

        self.keys = dict(keys)

        print(4*'-' , 'Twitterminal', 4*'-', end='\n\n')

        pprint(self.keys)
        

        self.auth = tweepy.OAuthHandler(self.keys['apiKey'], self.keys['apiSecret'])
        self.auth.set_access_token(self.keys['token'], self.keys['tokenSecret'])

        self.engine = tweepy.API(self.auth)