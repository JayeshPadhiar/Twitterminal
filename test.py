import json
import tweepy
from pprint import pprint

import os

print(4*'-' , 'Twitterminal', 4*'-', end='\n\n')

with open('keys.json', 'r') as creds:
    keys = json.load(creds)

auth = tweepy.OAuthHandler(keys['apiKey'], keys['apiSecret'])
auth.set_access_token(keys['token'], keys['tokenSecret'])
api = tweepy.API(auth)

tweets = api.user_timeline('twitter', count=3)

for x in tweets:
    pprint(x._json)
    print('\n\n\n\n')

os.system('clear')