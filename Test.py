import json
import tweepy
from pprint import pprint

print(4*'-' , 'Twitterminal', 4*'-', end='\n\n')

with open('keys.json', 'r') as creds:
    keys = json.load(creds)

auth = tweepy.OAuthHandler(keys['apiKey'], keys['apiSecret'])
auth.set_access_token(keys['token'], keys['tokenSecret'])
api = tweepy.API(auth)

x = api.get_user('jayeshpadhiar')

pprint(x._json)